import matplotlib
import pandas as pd
import pymysql as sql
import matplotlib.pyplot as plt
import sklearn as skt

plt.figure(figsize=(40,40))

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 40}

matplotlib.rc('font', **font)

db_connection = sql.connect(host='localhost', database='swap_card', user='root', password='password')

#dfJobTtl = pd.read_sql("select * from user where job_title is not NULL and not tags='[]' and not companies='[]'", con=db_connection)

dfJobTtl = pd.read_sql("select job_title,companies,tags from user where not tags='[]' and not companies='[]' and job_title='Engineer' or job_title='Ingénieur'", con=db_connection)

dfJobTtl = dfJobTtl.drop(['educations', 'second_job_title'], axis=1)

dfJobTtl = dfJobTtl.replace(["Dirigeant","Futur Dirigeant","CEO","Président","Directeur Général","Directeur"], "Poste de direction")

dfJobTtl = dfJobTtl.replace(["PDG, DG","Gérant","PDG / Gérant / Directeur général","Chef d'entreprise","CEO/Managing Director","Co-Founder"], "Poste de direction")

dfJobTtl = dfJobTtl.replace(["Autre","Autres","Other","","-"], "Autre")

# dfJobTtl = dfJobTtl.replace(["Etudiant","Student"], 2)

dfJobTtl = dfJobTtl.replace(['Law, Economics, Management'], "Law/Eco/management")

dfJobTtl = dfJobTtl.replace(["Engineering & Technology","Technical/Engineering","Data Scientist"],"Ingé")

dfJobTtl = dfJobTtl.replace(["Marketing", "Marketing/Communication"],"Marketing")

dfJobTtl = dfJobTtl.replace(["Sales", "Sales/Business Development", "Vendeur (commerce de détail)", "Acheteur"],"Acheteurs")

orderedJobTitles = dfJobTtl.job_title.value_counts(dropna=True)

for x in range(0,len(orderedJobTitles)):
    if orderedJobTitles[x] <= 5000:
        orderedJobTitles[x] = 0

orderedJobTitles.plot(kind='pie')

plt.show()


