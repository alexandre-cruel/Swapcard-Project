import pickle
import string

import nltk
import pandas as pd
import pymysql as sql
from gensim.models import KeyedVectors
from sklearn.cluster import DBSCAN

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from string import digits


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


#convert string to lowercase
sentences = sentences.lower()

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

vectors = pickle.load(open('foo','rb'))
model = KeyedVectors.load_word2vec_format('wiki.fr.align.vec').load_word2vec_format('wiki.en.align.vec')

print('Model built')


def fillveccluster(namelist):
    vec = []
    for a in namelist:
        if a in model.vocab:
            words = a
            vec.append((words, model[words]))
    return vec

vectors = fillveccluster(tokens)
#pickle.dump(vectors,open('foo','wb'))

dbVec = [v[1] for v in vectors]

cluster = DBSCAN(eps=0.3, min_samples=3, metric='cosine').fit(dbVec)

print(cluster.labels_)

#compter nombre de clusters
for i in range(min(cluster.labels_), max(cluster.labels_)):
    nbr = max(cluster.labels_) +1
print('On a ', nbr, 'clusters !')

#################################################
#################################################
#################################################
#################################################

"""
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
cluster, labels_true = make_blobs(n_samples= cluster.labels_, centers=centers, cluster_std=0.4,
                            random_state=0)

X = StandardScaler().fit_transform(X)

# #############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

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
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()"""


