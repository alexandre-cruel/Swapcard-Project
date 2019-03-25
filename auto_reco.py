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

arr1 = ['Analyst', 'ingénieur', 'marketing', 'ingénieur']
arr2 = [0, 1, 2, 0]

index = 0
correctIndex = []
correspondingWords = []
tagsTab = []
eventTab = []
connTab = []

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

for x in arr2:
    if x == 0:
        correctIndex.append(index)
    index = index + 1

for x in correctIndex:
    correspondingWords.append(arr1[x])


# Requête la base pour sortir les infos correspondantes :
#   - Tags
#   - Events
#   - What else ?

# df = pd.read_sql("select * from user where job_title like '%" + correspondingWords[0] + "%'", con=db_connection)

swapTags = pd.read_sql("select tags from user where not tags='[]' and job_title like '%" + correspondingWords[0] + "%'", con=db_connection)
swapEvents = pd.read_sql("select user.job_title, planning.categories from user join event_attendee ON event_attendee.user_id=user.id join planning on planning.event_id = event_attendee.event_id where user.job_title like '%" + correspondingWords[0] + "%' and not planning.categories='[]'", con=db_connection)
swapConn = pd.read_sql("select user.job_title, connection.user_id, count(*) as 'count' from connection join user on user.id = connection.user_id where user.job_title like '%" + correspondingWords[0] + "%' group by user_id order by count(*) desc", con=db_connection)

# - - - - - - - - Parse data a little

# TAGS
for tagsRow in swapTags.tags:
    tagsRow = cleanTag(tagsRow)
    tempTab = tagsRow.split(",")
    for tag in tempTab:
        tagsTab.append(tag)

# Event
for eventRow in swapEvents.categories:
    eventRow = cleanTag(eventRow)
    eventTab.append(eventRow)

# Créer une dataframe de tous les tags pour les manipuler

userData = pd.DataFrame({'tags': tagsTab})
userData = userData.join(pd.DataFrame({'events': eventTab}))
userData = userData.join(swapConn['user_id'])
userData = userData.join(swapConn['count'])


temp1 = userData['tags'].value_counts()
temp2 = userData['events'].value_counts()

#tagImpact = calclPart(userData['tags'].sum(), temp1)
#eventImpact = calclPart(userData['events'].sum(), temp2)

userData = userData.join(pd.DataFrame({'tagsRankingName': temp1.index.tolist()}))
userData = userData.join(pd.DataFrame({'tagsRankingVal': fillList(temp1)}))
userData = userData.join(pd.DataFrame({'eventRankingName': temp2.index.tolist()}))
userData = userData.join(pd.DataFrame({'eventRankingVal': fillList(temp2)}))


userData.drop('tags', axis=1, inplace=True)
userData.drop('events', axis=1, inplace=True)

print(userData[0:3])

userData[0:3].to_csv(correspondingWords[0]+'Data.csv')

# - - - - - - - - Ploting datas

# tagsCompte.plot(kind='pie',figsize=(10,10))#, autopct='%1.2f%%') #, subplots=True, x=None, y=None, autopct='%1.2f%%')
# plt.show()
