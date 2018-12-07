from gensim.models import KeyedVectors
from translate import Translator
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn import metrics


trad = Translator(from_lang='fr', to_lang="en")

model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
# model.wv.save_word2vecformat('googlenews.txt')
print('Modele build')

condSortie = 1

# while condSortie != 0:
# myInput = input("Entrez le mot à trouver : ")
#  = trad.translate(myInput)


clusterInge = ["engineer","electrical_engineer","mechanical_engineer"]
vecClusterInge = []

clusterCEO = []

for x in clusterInge:
    print(f'most similar words to {x} :\n{model.most_similar(x)}')
    vecClusterInge.append(model[x])

# print('# of words', len(model.wv.vocab))
# print('sample words', list(model.wv.vocab.keys())[:10])

acc = 0

vecCentroid = []

for y in range(0, len(vecClusterInge[0])):
    for x in vecClusterInge:
        acc = acc + x[y]

    vecCentroid.append(acc/(len(clusterInge)))
    acc = 0


# print(f'vector of word :\n{model[word]}')
print(f'vector of centroid :\n{vecCentroid}')
