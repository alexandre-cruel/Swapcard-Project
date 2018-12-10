from gensim.models import KeyedVectors
from translate import Translator

trad = Translator(from_lang='fr', to_lang="en")

model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

print('Model build')

condSortie = 1

# while condSortie != 0:
# myInput = input("Entrez le mot à trouver : ")
#  = trad.translate(myInput)


clusterInge = ["engineer", "electrical_engineer", "mechanical_engineer", "engineering"]

clusterCEO = ["Director", "CEO","Executive_Director", "Vice_President", "director", "General_Manager","President"]

myword = "engineer"
mywordvec = model[myword]


def fillveccluster(namelist):
    vec = []
    for a in namelist:
        vec.append(model[a])
    return vec


def calccentroid(vec):
    centroid = []
    acc = 0
    for y in range(0, len(vec[0])):
        for x in vec:
            acc = acc + x[y]

        centroid.append(acc / (len(vec)))
        acc = 0
    return centroid


def calcdist(vec1,vec2):
    acc = 0
    for x in range(0, len(vec1)):
        acc += pow(vec1[x]-vec2[x], 2)

    return pow(acc, 1/2)


vecClusterInge = fillveccluster(clusterInge)
vecClusterCEO = fillveccluster(clusterCEO)
ingeCentroid = calccentroid(vecClusterInge)
ceoCentroid = calccentroid(vecClusterCEO)

dist = calcdist(ingeCentroid, ceoCentroid)

# print(f'vector of word :\n{model[word]}')
print(f'vector of centroid for inge cluster :\n{ingeCentroid}')
print(f'vector of centroid for inge cluster :\n{ceoCentroid}')

print(f'\n\nThe word : {myword} is {calcdist(mywordvec,ingeCentroid)} away from Inge cluster \nand {calcdist(mywordvec, ceoCentroid)} away from CEO cluster')




