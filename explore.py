import pandas as pd
import pymysql as sql
from sklearn.cluster import AgglomerativeClustering
import numpy as np


db_connection = sql.connect(host='localhost', database='swapcard', user='root', password='coucou74')

df = pd.read_sql("select * from user where job_title is not NULL and not tags='[]' and not companies='[]' limit 100", con=db_connection)


df = df.drop(['educations', 'second_job_title'], axis=1)

df = df.replace(["Dirigeant","Futur Dirigeant","CEO","Président","Directeur Général","Directeur"], "1")

de = df.replace(["PDG, DG","Gérant","PDG / Gérant / Directeur général","Chef d'entreprise","CEO/Managing Director","Co-Founder"], "1")

df = df.replace(["Autre","Autres","Other","","-", "[]"], "2")

df = df.replace(["Etudiant","Student"],"3")

df = df.replace(["Engineering & Technology","Technical/Engineering","Data Scientist"],"4")

df = df.replace(["Marketing","Marketing/Communication"],"5")

df = df.replace(["Sales","Sales/Business Development","Vendeur (commerce de détail)"],"6")

#orderedf = df.job_title.value_counts(dropna=True)

#for x in range(0,len(orderedf)):
    #if orderedf[x] <= 5000:
        #orderedf[x] = 0


X = np.asarray(df)

clustering = AgglomerativeClustering().fit(X, y=None)
print(clustering)
AgglomerativeClustering(affinity='euclidean', compute_full_tree='auto', connectivity=None, linkage='ward', memory=None, n_clusters=5, pooling_func='deprecated')
print(clustering.labels_)
