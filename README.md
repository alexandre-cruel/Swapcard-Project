# Swapcard-Project : Projet Data-Science Ingé3 Esme Sudria

Système de recommandation de profil de personnes à rencontrer lors d'événements.

## Description : 

Nous avons pour objectif de créer un système de recommandation pour des utilisateurs sur lesquels nous avons très peu de données. 

Vous retrouverez dans ce projet : 

### Identification des profils 
- _w2v.py_ : Génère de faux cluster basé sur le modèle word2vec de Google News
- _dbScanClustering.py_ : Utilise la bibliothèque DBScan de Scikit-Learn pour créer automatiquement les cluster à partir des vecteurs du modèle GN
### Recommandation
- _main.py_ : Récupération des profils complets dans la base de donnée puis _parsing_ partiel des données (*Work in progress*)


## Télécharger le projet
```bash
git clone https://github.com/alexandre-cruel/Swapcard-Project 
```

## Dev team :  
* Baptiste Chevallier  
* Raphaël Champeaud  
* Alexandre Cruel  


