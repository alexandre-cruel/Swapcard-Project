import string
from gensim.models import KeyedVectors
import pymysql as sql
import pandas as pd
from sklearn.cluster import DBSCAN
import pickle
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from string import digits
from translate import Translator

tab = []
vec = []

#connect to sql db
db_connection = sql.connect(host='localhost', database='swapcard', user='root', password='coucou74')

#create dataframe from our db
dfJobTtl = pd.read_sql("select job_title from user where not tags='[]' and not companies='[]' group by job_title order by count(*) desc limit 100", con=db_connection)
dfJobTtl = dfJobTtl.loc[2:]
print(dfJobTtl.head())


#take our job title into a string
text = dfJobTtl.to_string()

#removing the digits from the list
remove_digits = str.maketrans('', '', digits)
text2 = text.translate(remove_digits)
print(text2)


#removing characters
table = str.maketrans({key: ' ' for key in string.punctuation})
sentences = text2.translate(table).replace('d’', ' ')


#suppression de mots de 2 lettres ou moins
tab = sentences.split()
for i in tab:
    if len(i) < 3:
        tab.remove(i)
print(tab)
chaine = " ".join(tab)

#use of nltk
tokens = nltk.word_tokenize(chaine)
print(tokens)
tagged = nltk.pos_tag(tokens)
print(tagged[0:6])


#####################################################

#job_list = ['Director', 'CEO', 'CEO', 'Engineer', 'Managing_Director', 'marketing']

vectors = pickle.load(open('foo','rb'))
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

print('Model build')

trad = Translator(from_lang='fr', to_lang="en")


def fillveccluster(namelist):
    vec = []
    for a in namelist:
        vec.append((a,model[a]))
    return vec

vectors = fillveccluster(tokens)

dbVec = [v[1] for v in vectors]

cluster = DBSCAN(eps=0.4, min_samples=1, metric='cosine').fit(dbVec)

print(cluster.labels_)
#print(cluster.components_)


