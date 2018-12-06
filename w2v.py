from gensim.models import KeyedVectors
from translate import Translator
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn import metrics


trad = Translator(from_lang='fr', to_lang="en")

model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
# model.wv.save_word2vecformat('googlenews.txt')
print('Modele build')

#model = model.reshape(1, -1)

db = DBSCAN(eps=0.3, min_samples=1000000).fit(model)

core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)

condSortie = 1

while condSortie != 0:
    myInput = input("Entrez le mot à trouver : ")
    word = trad.translate(myInput)
    print('# of words', len(model.wv.vocab))
    print('sample words', list(model.wv.vocab.keys())[:10])

    # all the vocabulary is in this format : STD + word (for regular tags) COMPANY + word, INDUSTRY + word

    print(f'most similar words to {word} :\n{model.most_similar(word)}')
    # print(f'vector of word :\n{model[word]}')

    # Some maths

    # print(stereotype)
    condSortie = input("Sortir ? :")


