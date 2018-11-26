from gensim.models import KeyedVectors
import pymysql as sql
import pandas as pd


db_connection = sql.connect(host='localhost', database='swapcard', user='root', password='coucou74')

df = pd.read_sql("select * from user where job_title is not NULL and not tags='[]' and not companies='[]'", con=db_connection)

df = df.drop(['educations', 'second_job_title'], axis=1)

df = df.replace(["Dirigeant","Futur Dirigeant","CEO","Président","Directeur Général","Directeur"], "Poste de direction")

df = df.replace(["PDG, DG","Gérant","PDG / Gérant / Directeur général","Chef d'entreprise","CEO/Managing Director","Co-Founder"], "Poste de direction")

df = df.replace(["Autre","Autres","Other","","-"], "Autre")

df = df.replace(["Etudiant","Student"],"Etudiants")

df = df.replace(["Engineering & Technology","Technical/Engineering","Data Scientist"],"Ingé")

df = df.replace(["Marketing","Marketing/Communication"],"Marketing")

df = df.replace(["Sales","Sales/Business Development","Vendeur (commerce de détail)"],"Acheteur")


vecs = KeyedVectors.load_word2vec_format(df)

word = 'STD_c'
print('# of words', len(vecs.wv.vocab))
print('sample words', list(vecs.wv.vocab.keys())[:10])

# all the vocabulary is in this format : STD_ + word (for regular tags) COMPANY_ + word, INDUSTRY_ + word

print(f'most similar words to {word} :\n{vecs.most_similar(word)}')
print(f'vector of word :\n{vecs[word]}')

