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

word = "engineer"
word2 = "electrical_engineer"
word3 = "mechanical_engineer"

# print('# of words', len(model.wv.vocab))
# print('sample words', list(model.wv.vocab.keys())[:10])

print(f'most similar words to {word} :\n{model.most_similar(word)}')
print(f'most similar words to {word2} :\n{model.most_similar(word)}')
print(f'most similar words to {word3} :\n{model.most_similar(word)}')

vec1 = model[word]
vec2 = model[word2]
vec3 = model[word3]

vecCentroide = []

for x in range(0, len(vec1)):
    vecCentroide.append((vec1[x]+vec2[x]+vec3[x])/3)



# print(f'vector of word :\n{model[word]}')
print(f'vector of centroid :\n{vecCentroide}')
