# - - - - - - - - - Imports

import pandas as pd
import pymysql as sql
import matplotlib
import matplotlib.pyplot as plt

db_connection = sql.connect(host='localhost', database='swap_card', user='root', password='password')

# - - - - - - - - -  Params plots

font = {'family': 'Helvetica', 'weight': 'bold', 'size': 22}

matplotlib.rc('font', **font)

plt.figure(figsize=(20,20))

# - - - - - - - - - Var

arr1 = ['CEO', 'ingénieur', 'marketing', 'ingénieur']
arr2 = [0, 1, 2, 0]

index = 0
correctIndex = []
correspondingWords = []
tagsTab = []
eventTab = []

# - - - - - - - - - Functions


def cleanTag(a):
    a = a.replace("[", "")
    a = a.replace("]", "")
    a = a.replace("\"", "")
    a = a.replace('\\u00e9', "é")
    a = a.replace('\\u00ea', "ê")
    a = a.replace('\\u00e0', "à")
    a = a.replace('\\u00c9', "É")
    return a


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
swapEvents = pd.read_sql("select user.job_title, planning.categories from user join event_attendee ON event_attendee.user_id=user.id join planning on planning.event_id = event_attendee.event_id where user.job_title like '%" + correspondingWords[0] + "%' and not planning.categories='[]' limit 2000", con=db_connection)

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

temp1 = userData['tags'].value_counts()
print(temp1)
temp2 = userData['events'].value_counts()

userData = userData.join(pd.DataFrame({'tagsRanking': temp1}))
userData = userData.join(pd.DataFrame({'eventRanking': temp2}))


print(userData.head())

# - - - - - - - - Ploting datas

# tagsCompte.plot(kind='pie',figsize=(10,10))#, autopct='%1.2f%%') #, subplots=True, x=None, y=None, autopct='%1.2f%%')
# plt.show()
