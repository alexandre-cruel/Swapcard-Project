from gensim.models import KeyedVectors
from translate import Translator
import pymysql as sql
import pandas as pd
from sklearn.cluster import DBSCAN
import pickle


#db_connection = sql.connect(host='localhost', database='swap_card', user='root', password='password')

#dfJobTtl = pd.read_sql("select job_title from user where not tags='[]' and not companies='[]' group by job_title order by count(*) desc limit 100", con=db_connection)
#dfJobTtl = dfJobTtl.iloc[2:]

#dfJobTtl = dfJobTtl.replace([""])

#print(dfJobTtl.head())

job_list = ['Buyer', 'Director', 'CEO', 'CEO', 'Engineer', 'Managing_Director', 'marketing']

vectors = pickle.load(open('foo','rb'))
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

print('Model build')


def fillveccluster(namelist):
    vec = []
    for a in namelist:
        vec.append((a, model[a]))
    return vec


vectors = fillveccluster(job_list)

pickle.dump(vectors, open('foo', 'wb'))

dbVec = [v[1] for v in vectors]

cluster = DBSCAN(eps=0.4, min_samples=1, metric='cosine').fit(dbVec)

print(cluster.labels_)
