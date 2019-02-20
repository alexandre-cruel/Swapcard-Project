from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
from gensim.models.wrappers import FastText

ftPath = 'foo'

model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
model.wv.save_word2vec_format('googlenews.txt')

model2 = FastText.load_fasttext_format(ftPath)

### TODO : 1 Tester ça next /w un seul language
#model2.similarity()
#model2.most_similar()

# TODO : 1.2 Tester avec deux lang voir si ça pose un problème qu'elles soient pas alignées.

### TODO : 2 pull le git de ce gars ( Vecteurs alignés et combinés )
# https://github.com/Babylonpartners/fastText_multilingual


# TODO : 3 le git de ce mec pour augmenter la taille du model FT in case on veut rentrer de new mots
#  https://github.com/facebookresearch/fastText/pull/423

