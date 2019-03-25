# -*- coding: utf-8 -*-

import pickle
import string
import nltk
import time
import sys
import pandas as pd
import pymysql as sql
import numpy as np
import matplotlib.pyplot as plt

from string import digits
from gensim.models import KeyedVectors
from sklearn.cluster import DBSCAN
from wordcloud import WordCloud
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from distance import levenshtein

response = ''


def recommendation(args1):
    global response

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')

    vec = []
    baba = []
    lemmatizer = WordNetLemmatizer()

    # connect to sql db
    db_connection = sql.connect(host='localhost', database='swap_card', user='root', password='password')

    # create dataframe from our db
    dfJobTtl = pd.read_sql(
        "select job_title from user where not tags='[]' and not companies='[]' group by job_title order by count(*) desc limit 100",
        con=db_connection)
    dfJobTtl = dfJobTtl.loc[2:]
    print(dfJobTtl.head())

    # take our job title into a string
    text = dfJobTtl.to_string()

    # removing the digits from the list
    remove_digits = str.maketrans('', '', digits)
    text2 = text.translate(remove_digits)
    print(text2)

    # removing characters
    table = str.maketrans({key: ' ' for key in string.punctuation})
    sentences = text2.translate(table).replace('d’', ' ')

    # convert string to lowercase
    sentences = sentences.lower()

    # suppression de mots de 2 lettres ou moins
    tab = []
    tab = sentences.split()
    for i in tab:
        if len(i) < 3:
            tab.remove(i)
    print(tab)
    chaine = " ".join(tab)

    # use of nltk
    tokens = nltk.word_tokenize(chaine)
    print(tokens)
    tagged = nltk.pos_tag(tokens)
    print(tagged[0:6])

    ##################################################################################################

    vectors = pickle.load(open('foo', 'rb'))
    model = KeyedVectors.load_word2vec_format('testvec')

    print('Model built')

    ##################################################################################################
    ##################################################################################################


    def fillveccluster(namelist):
        for a in namelist:
            if a in model.vocab:
                vec.append((a, model[a]))
                baba.append(a)
        return vec

    ##################################################################################################

    taille_entree = None

    def cleaner(entree):
        global response
        response = response + 'Bonjour, je crois comprendre que vous êtes ' + entree
        print("Bonjour, je crois comprendre que vous êtes", entree)
        entree = entree.lower()

        # découpe la chaine de caractère (tokenize)
        entree = entree.replace('-', ' ').replace('/', ' ').replace(digits, ' ').replace("d'", ' ')
        tokenized_entree = word_tokenize(entree)
        print(tokenized_entree)

        no_caract_entree = []
        for word in tokenized_entree:
            if word not in string.punctuation:
                no_caract_entree.append(word)
        print(no_caract_entree)

        # supprime les stopword
        stoplist = set(stopwords.words('french'))
        int_no_stopwords = []
        for word in no_caract_entree:
            if word not in stoplist:
                int_no_stopwords.append(word)

        # ramène les mots à leur forme la plus simple (lemmatize)
        lemmatized_entree = []
        for word in int_no_stopwords:
            lemmatized_entree.append(lemmatizer.lemmatize(word))
        print(lemmatized_entree)

        # ajoute les mots dans notre vecteur
        taille_entree = 0
        for x in lemmatized_entree:
            taille_entree = taille_entree + 1
            if x in model.vocab:
                vec.append((x, model[x]))
                baba.append(x)
            elif x not in model.vocab:
                # correction avec distance de levenshtein
                metier = pd.read_csv('jobs.csv', sep='\t', low_memory=False)
                liste_metier = metier['libellé métier']
                mini = 100
                monmot = None

                # trouver la distance minimum et la print
                for nom in liste_metier:
                    distance_lev = levenshtein(nom, x)
                    if distance_lev < mini:
                        monmot = nom
                    mini = min(mini, distance_lev)
                    while distance_lev > 5:
                        return exit("Merci de ré-essayer avec une orthographe correcte")
                    correction = monmot
                    print('Le terme dans le dictionnaire le plus proche du mot saisi est à une distance de:', mini)
                    print('TERME LE PLUS PROCHE', correction)
                    vec.append((correction, model[correction]))
                    baba.append(correction)
            else:
                print("----- TEMPS DE REPONSE : %s secondes ----- " % (time.time() - start_time))
                return exit("Merci de ré-essayer avec une orthographe correcte")

            # donne le nombre de mots que l'on va donner à DBSCAN
        print('On ajoute', taille_entree, 'mots !')
            # Affichage des vecteurs du candidat
        print(vec)

    ##################################################################################################

    # Récupération du Cold Start Candidate
    entree = input("Entrez votre métier: ")
    start_time = time.time()
    entreeclean = cleaner(entree)


    ##################################################################################################
    vectors = fillveccluster(tokens)
    dbVec = [v[1] for v in vectors]

    cluster = DBSCAN(eps=0.3, min_samples=2, metric='cosine').fit(dbVec)
    print(cluster.labels_)

    ##################################################################################################

    # compter nombre de clusters
    count = 0
    for i in range(min(cluster.labels_), max(cluster.labels_)):
        nbr = max(cluster.labels_) + 1
    response = response + '\non a ' + str(nbr) + ' clusteurs !'
    print('On a ', nbr, 'clusters !')

    # compter nombre de mots clusterisés
    num_out = (cluster.labels_ == -1).sum()
    tot = 0
    for i in cluster.labels_:
        tot = tot + 1
    response = response + 'On a ' + str(tot) + ' mots dans notre liste de métiers\n' + str(num_out) + 'ne sont pas ' \
                                                                                                      'compris dans ' \
                                                                                                      'un clusteur '
    print('On a ', tot, 'mots dans notre liste de métiers')
    print(num_out, 'ne sont pas compris dans un cluster')

    percent = 100 - round(num_out / tot * 100, 2)
    print('Le pourcentage de mots clusterisés est de :', percent, '%')
    response = response + '\nLe pourcentage de mots clusterisés est de : ' + str(percent) + '%'

    # - - - - - - - - - Var

    arr1 = baba
    arr2 = cluster.labels_
    fooTest = 1

    index = 0
    correctIndex = []
    correspondingWords = []

    dfFinale = pd.DataFrame()

    # - - - - - - - - - Functions
    def fillList(list):
        listRetour = []
        for i in range(0, len(list)):
            listRetour.append(list[i])
        return listRetour

    def cleanTag(a):
        a = a.replace("[", "")
        a = a.replace("]", "")
        a = a.replace("\"", "")

        # Unidecode
        a = a.replace('\\u00e9', "é")
        a = a.replace('\\u00ea', "ê")
        a = a.replace('\\u00e0', "à")
        a = a.replace('\\u00c9', "É")
        return a

    # - - - - - - - - - Core

    # Récupérer les données depuis les clusters

    cntr = 0
    indexCluster = 0
    for y in arr2:
        if y < fooTest and cntr < 5:
            correctIndex.append(indexCluster)
            cntr = cntr + 1
        indexCluster = indexCluster + 1

    for x in correctIndex:
        correspondingWords.append(arr1[x])

    def requests(name):
        tags_tab = []
        event_tab = []
        connTab = []

        swap_tags = pd.read_sql("select tags from user where not tags='[]' and job_title like '%" + name + "%'",
                                con=db_connection)
        swap_events = pd.read_sql(
            "select planning.categories from user join event_attendee ON event_attendee.user_id=user.id join planning on planning.event_id = event_attendee.event_id where user.job_title like '%" + name + "%' and not planning.categories='[]'",
            con=db_connection)
        swap_conn = pd.read_sql(
            "select connection.user_id, count(*) as 'count' from connection join user on user.id = connection.user_id where user.job_title like '%" + name + "%' group by user_id order by count(*) desc",
            con=db_connection)

        # - - - - - - - - Parse data a little
        # TAGS
        for tagsRow in swap_tags.tags:
            tagsRow = cleanTag(tagsRow)
            tempTab = tagsRow.split(",")
            for tag in tempTab:
                tags_tab.append(tag)

        # Event
        for eventRow in swap_events.categories:
            eventRow = cleanTag(eventRow)
            event_tab.append(eventRow)

        # Créer une dataframe des datas pour manipuler

        user_data = pd.DataFrame({'tags': tags_tab})
        user_data = user_data.join(pd.DataFrame({'events': event_tab}))
        user_data = user_data.join(swap_conn['user_id'])
        user_data = user_data.join(swap_conn['count'])

        temp1 = user_data['tags'].value_counts()
        temp2 = user_data['events'].value_counts()

        user_data = user_data.join(pd.DataFrame({'tagsRankingName': temp1.index.tolist()}))
        user_data = user_data.join(pd.DataFrame({'tagsRankingVal': fillList(temp1)}))
        user_data = user_data.join(pd.DataFrame({'eventRankingName': temp2.index.tolist()}))
        user_data = user_data.join(pd.DataFrame({'eventRankingVal': fillList(temp2)}))

        user_data.drop('tags', axis=1, inplace=True)
        user_data.drop('events', axis=1, inplace=True)

        #    user_data[0:3].to_csv(correspondingWords[0] + 'Data.csv')

        return user_data.iloc[:2]


    for jobs in correspondingWords:
        print('Starting new requests ... ')
        frames = [dfFinale, requests(jobs)]
        dfFinale = pd.concat(frames)
        print('Data added to final dataframe')

    print('Exporting data to CSV ... ')
    dfFinale = dfFinale.drop_duplicates()
    dfFinale.to_csv('finale.csv')
    print('Export done !')

    return dfFinale


def main(argv):
    print('ok')


if __name__ == "__main__":
    import sys

    main(sys.argv)


recommendation('Ingénieur')


##################################################################################################
"""
#WordCloud

wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(chaine)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
"""

##################################################################################################
##################################################################################################
"""
# PLOTTING OUR WORDS TO SEE REPARTITION

from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.datasets.samples_generator import make_blobs


# Generate sample data
#centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=tot, random_state=0)
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

##################################################################################################
#CALCULATING MOST APPROPRIATE VALUE OF EPSILON

from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans

mod = KMeans()
visualizer = KElbowVisualizer(mod, k=(1, 10))
visualizer.fit(X)
visualizer.poof()
"""
##################################################################################################

# Performing PCA
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

##################################################################################################


# print("----- TEMPS DE REPONSE : %s secondes ----- " % (time.time() - start_time))