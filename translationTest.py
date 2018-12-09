from gensim.models import KeyedVectors
from translate import Translator

trad = Translator(from_lang='fr', to_lang="en")

model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
# model.wv.save_word2vecformat('googlenews.txt')
print('Modele build')


# while condSortie != 0:
# myInput = input("Entrez le mot à trouver : ")
#  = trad.translate(myInput)

clusterCEO = ["Director", "CEO","Executive_Director", "Vice_President", "director", "General_Manager","President"]


for a in clusterCEO:
    print(f'most similar words to {a} :\n{model.most_similar(a)}')
