import pickle
import string
import nltk
import pandas as pd
import pymysql as sql

from string import digits
from gensim.models import KeyedVectors
from sklearn.cluster import DBSCAN
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')


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


#convert string to lowercase
sentences = sentences.lower()

#suppression de mots de 2 lettres ou moins
tab = []
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


###################################################################################################

vectors = pickle.load(open('foo','rb'))
model = KeyedVectors.load_word2vec_format('testvec')

print('Model built')


##################################################################################################
##################################################################################################

lemmatizer = WordNetLemmatizer()

#Récupération du Cold Start Candidate
entree = input("Entrez votre métier: ")
entree = entree.lower()
print("Bonjour, j'ai cru comprendre que vous êtes", entree)

if entree in model.vocab:
    vec.append((entree, model[entree]))
else:    #si pas dans le vocabulaire

#découpe la chaine de caractère (tokenize)
    tokenized_entree = word_tokenize(entree)
    print(tokenized_entree)

#supprime les caractères
    no_caract_entree = []
    for word in tokenized_entree:
        if word not in string.punctuation:
            no_caract_entree.append(word)
    print(no_caract_entree)

#supprime les stopword
    stoplist = set(stopwords.words('french'))
    int_no_stopwords = []
    for word in no_caract_entree:
        if word not in stoplist:
            int_no_stopwords.append(word)

#ramène les mots à leur racine (lemmatize)
    lemmatized_entree = []
    for word in int_no_stopwords:
        lemmatized_entree.append(lemmatizer.lemmatize(word))
    print(lemmatized_entree)

#on trouve une solution pour les mots inconnus

#sinon on les supprime

#faire la moyenne des vecteurs


#Placement du candidate dans nos clusters




#Renvoyer les termes les plus proches de notre candidat

###################################################################################################

def fillveccluster(namelist):
    for a in namelist:
        if a in model.vocab:
            vec.append((a, model[a]))
    return vec

vectors = fillveccluster(tokens)
#pickle.dump(vectors,open('foo','wb'))

dbVec = [v[1] for v in vectors]

cluster = DBSCAN(eps=0.5, min_samples=1, metric='cosine').fit(dbVec)
#                                                                                                             grosse valeur de epsilon (mail yue)
print(cluster.labels_)

###################################################################################################

#compter nombre de clusters
count = 0
for i in range(min(cluster.labels_), max(cluster.labels_)):
    nbr = max(cluster.labels_) +1
print('On a ', nbr, 'clusters !')

#compter nombre de mots clusterisés
num_out = (cluster.labels_ == -1).sum()
tot = 0
for i in cluster.labels_:
    tot = tot +1
print('On a ', tot, 'mots dans notre liste de métiers')
print(num_out, 'ne sont pas compris dans un cluster')

percent = 100 - round(num_out/tot * 100, 2)
print('Le pourcentage de mots clusterisés est de :', percent, '%')


###############################################################################################################
###############################################################################################################

# PLOTTING OUR WORDS TO SEE REPARTITION
"""
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
#centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples= tot, random_state=0)
X = StandardScaler().fit_transform(X)

# Compute DBSCAN
core_samples_mask = np.zeros_like(cluster.labels_, dtype=bool)
core_samples_mask[cluster.core_sample_indices_] = True
labels = cluster.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))

# Plot result

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),   # 'o' : marker en forme de cercle
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
"""

############################################################################################

#Performing PCA
"""
from sklearn import decomposition
from sklearn import preprocessing

std_scale = preprocessing.StandardScaler().fit(X)
X_scaled = std_scale.transform(X)
pca = decomposition.PCA(n_components=2)
pca.fit(X_scaled)

print(pca.n_components_)
print(pca.explained_variance_ratio_)
print(pca.explained_variance_ratio_.sum())
"""

#############################################################################################


