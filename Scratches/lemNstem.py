import nltk
from nltk.stem import WordNetLemmatizer

from nltk.stem.snowball import SnowballStemmer


#ltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

print(lemmatizer.lemmatize("electrician"))

stemmer = SnowballStemmer("english")
print(stemmer.stem("electrical engineer"))
