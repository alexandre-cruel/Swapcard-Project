from gensim.models import KeyedVectors
import pymysql as sql
import pandas as pd
from sklearn.cluster import DBSCAN
import pickle

vec = []


def fillveccluster(namelist):
    vec = []
    for a in namelist:
        vec.append((a, model[a]))
    return vec


db_connection = sql.connect(host='localhost', database='swap_card', user='root', password='password')

dfJobTtl = pd.read_sql("select job_title from user where not tags='[]' and not companies='[]' group by job_title order by count(*) desc limit 100", con=db_connection)
dfJobTtl = dfJobTtl.iloc[2:]

# job_list = ['Buyer', 'Director', 'CEO', 'CEO', 'Engineer', 'Managing_Director', 'marketing']
#
# vectors = pickle.load(open('foo','rb'))
model = KeyedVectors.load_word2vec_format('/Users/baptiste/Documents/3CI/SwapTest/Swap-CardAlex/Swapcard-Project/GoogleNews-vectors-negative300.bin', binary=True)
#
# print('Model build')

dfJobTtl = dfJobTtl.replace(["Etudiant","Student"], 2)




for jobs in dfJobTtl.job_title:
    try:
        print(jobs)
        vec.append((jobs, model[jobs]))
    except KeyError as err:
        print(err)
        print(jobs)




