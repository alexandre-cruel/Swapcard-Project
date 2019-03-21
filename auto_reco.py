# - - - - - - - - - Imports

import pandas as pd
import pymysql as sql
import matplotlib.pyplot as plt


# - - - - - - - - - Var

arr1 = ['CEO', 'ingénieur', 'marketing', 'CEO']
arr2 = [0, 1, 2, 0]

index = 0
correctIndex = []
correspondingWords = []
tagsTab = []

# - - - - - - - - - Core

for x in arr2:
    if x == 0:
        correctIndex.append(index)
    index = index + 1

for x in correctIndex:
    correspondingWords.append(arr1[x])


db_connection = sql.connect(host='localhost', database='swap_card', user='root', password='password')

#df = pd.read_sql("select * from user where job_title like '%" + correspondingWords[0] + "%'", con=db_connection)

df = pd.read_sql("select tags from user where not tags='[]'", con=db_connection)


for tagsRow in df.tags:
    tagsRow = tagsRow.replace("[", "")
    tagsRow = tagsRow.replace("]", "")
    tagsRow = tagsRow.replace("\"", "")
    tagsRow = tagsRow.replace('\\u00e9', "é")
    tempTab = tagsRow.split(",")
    for tag in tempTab:
        tagsTab.append(tag)


dfTags = pd.DataFrame({'col1': tagsTab})


#print(dfTags['col1'].value_counts())

tagsCompte = dfTags['col1'].value_counts()

tagsCompte.drop()

tagsCompte.plot(kind='pie', subplots=True, x=None, y=None, autopct='%1.2f%%')

plt.show()












