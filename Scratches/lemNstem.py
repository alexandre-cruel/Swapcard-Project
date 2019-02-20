import nltk
from nltk.stem import WordNetLemmatizer


from nltk.stem.snowball import SnowballStemmer
import nltk

#
# _______________ Levenstein distance __________________
#

word1 = "engineer"

word2 = "electrical_engineer"

print(nltk.edit_distance(word1, word2))

print(nltk.edit_distance(word1, word2)/len(word2))

#
#  ____________________ STEMMER _______________________
#

stemmer = SnowballStemmer("french")

print(stemmer.stem("voudrais"))
