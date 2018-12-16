import pandas as pd
import pymysql as sql
import matplotlib.pyplot as plt
import sklearn as skt
import matplotlib

plt.figure(figsize=(40,40))

font = {'family' : 'arial',
        'weight' : 'bold',
        'size'   : 40}

matplotlib.rc('font', **font)


db_connection = sql.connect(host='localhost', database='swap_card', user='root', password='password')

df = pd.read_sql("select company.industries from user inner join company on company_id = company.id where not company.industries='[]' and not company.industries = '[\"\"]'", con=db_connection)
df = df.iloc[2:]


#PTDR ON RECUPERE PAS LES BONNES DONNEES

#df = pd.DataFrame(data={'count': [204681, 386829]})

df = df['industries'].value_counts(dropna=True)

for x in range(0,len(df)):
    if df[x] <= 2000:
        df[x] = 0



df.plot(kind='pie', subplots=True, x=None, y=None, autopct='%1.2f%%')

plt.show()

