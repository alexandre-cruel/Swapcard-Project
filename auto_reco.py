# - - - - - - - - - Imports

import pandas as pd
import pymysql as sql
import matplotlib
import matplotlib.pyplot as plt

db_connection = sql.connect(host='localhost', database='swap_card', user='root', password='password')

pd.set_option('display.max_columns', 500)

# - - - - - - - - -  Params plots

font = {'family': 'Helvetica', 'weight': 'bold', 'size': 22}

matplotlib.rc('font', **font)

plt.figure(figsize=(20,20))

# - - - - - - - - - Var

arr1 = ['chef', 'entrepris', 'marketing', 'ingénieur']
arr2 = [0, 1, 2, 0]
fooTest = [0, 1]

index = 0
correctIndex = []
correspondingWords = []

dfFinale = pd.DataFrame()


# - - - - - - - - - Functions
def fillList(list):
    listRetour = []
    for i in range(0,len(list)):
        listRetour.append(list[i])
    return listRetour



def cleanTag(a):
    a = a.replace("[", "")
    a = a.replace("]", "")
    a = a.replace("\"", "")

    #Unidecode
    a = a.replace('\\u00e9', "é")
    a = a.replace('\\u00ea', "ê")
    a = a.replace('\\u00e0', "à")
    a = a.replace('\\u00c9', "É")
    return a

def calclPart(sum, list):
    tempList = []
    for i in range(0, len(list)):
        tempList.append(list[i]*100/sum)
    return tempList

# - - - - - - - - - Core

# Récupérer les données depuis les clusters

for y in range(0,len(fooTest)):
    for x in arr2:
        if x == y:
            correctIndex.append(y)
    index = index + 1

for x in correctIndex:
    print(x)
    correspondingWords.append(arr1[x])
    print(correspondingWords)


def requests(name):
    tags_tab = []
    event_tab = []
    connTab = []

    swap_tags = pd.read_sql("select tags from user where not tags='[]' and job_title like '%" + name + "%'", con=db_connection)
    swap_events = pd.read_sql("select planning.categories from user join event_attendee ON event_attendee.user_id=user.id join planning on planning.event_id = event_attendee.event_id where user.job_title like '%" + name + "%' and not planning.categories='[]'", con=db_connection)
    swap_conn = pd.read_sql("select connection.user_id, count(*) as 'count' from connection join user on user.id = connection.user_id where user.job_title like '%" + name + "%' group by user_id order by count(*) desc", con=db_connection)

    # - - - - - - - - Parse data a little
    # TAGS
    for tagsRow in swap_tags.tags:
        tagsRow = cleanTag(tagsRow)
        tempTab = tagsRow.split(",")
        for tag in tempTab:
            tags_tab.append(tag)

    # Event
    for eventRow in swap_events.categories:
        eventRow = cleanTag(eventRow)
        event_tab.append(eventRow)

    # Créer une dataframe des datas pour manipuler

    user_data = pd.DataFrame({'tags': tags_tab})
    user_data = user_data.join(pd.DataFrame({'events': event_tab}))
    user_data = user_data.join(swap_conn['user_id'])
    user_data = user_data.join(swap_conn['count'])

    temp1 = user_data['tags'].value_counts()
    temp2 = user_data['events'].value_counts()

    user_data = user_data.join(pd.DataFrame({'tagsRankingName': temp1.index.tolist()}))
    user_data = user_data.join(pd.DataFrame({'tagsRankingVal': fillList(temp1)}))
    user_data = user_data.join(pd.DataFrame({'eventRankingName': temp2.index.tolist()}))
    user_data = user_data.join(pd.DataFrame({'eventRankingVal': fillList(temp2)}))

    user_data.drop('tags', axis=1, inplace=True)
    user_data.drop('events', axis=1, inplace=True)

#    user_data[0:3].to_csv(correspondingWords[0] + 'Data.csv')

    return user_data.iloc[:3]


for jobs in correspondingWords:
    print('Starting new requests ... ')
    frames = [dfFinale,requests(jobs)]
    dfFinale = pd.concat(frames)
    print('Data added to final dataframe')

print('Exporting data to CSV ... ')
dfFinale.to_csv('finale.csv')
print('Export done !')

# - - - - - - - - Ploting datas

# tagsCompte.plot(kind='pie',figsize=(10,10))#, autopct='%1.2f%%') #, subplots=True, x=None, y=None, autopct='%1.2f%%')
# plt.show()
