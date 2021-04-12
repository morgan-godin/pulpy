# PulPY Covers 

## Le projet

### Description du projet

Cette application web a pour but de faciliter la visualisation de couvertures *pulp*. Ce terme désigne les publications bon bon marché d'histoires aux thèmes divers comme des romances, des polars, des récits fantastiques... Nous vous proposons ici une sélection de couvertures centrée sur la thématique de la science fiction avec des titres comme *Amazing Stories*, *Astounding Stories*, *Galaxy*...

Les premières couvertures ajoutées sont issues d'une [collection](https://archive.org/details/pulpmagazinearchive) de dépôts Internet Archive sous [Licence Creative Commons](https://creativecommons.org/licenses/?lang=fr-FR).

Vous pourrez naviguer à l'intérieur grâce à l'index des numéros et à la galerie des couvertures.

Vous êtes invité à enrichir notre base de données en ajoutant des couvertures grâce au formulaire dédié.

L'ajout, la suppression et la modification de notices nécessite une inscription préalable pour laquelle vous sont demandés :

* un login
* votre nom
* votre email
* un mot de passe

### À propos

Cette application web est développée dans le cadre du Master 2 Technologies numériques appliquées à l'histoire de l'École nationale des chartes.

### Sources du projet

Ce devoir n'a pour vocation que de générer une interface basée sur Python, HTML et CSS. Les données ont été récupérées depuis la collection [The Pulp Magazine](https://archive.org/details/pulpmagazinearchive) créée par [Jason Scott](https://archive.org/details/@jason_scott) sur Internet Archive.

### Description du projet

PulPY est une application web permettant de donner accès aux couvertures de pulp magazines avec des notices comportant des informations sur ces ces dernières telles que les artistes qui les ont réalisés, les magazines qui les ont publiés et leurs éditeurs.

### Comment fonctionne PulPY

Les différentes pages s'appuient sur les langages HTML, CSS, et Python 3, ainsi que sur une base de données MySQL.

### Comment installer PulPY

Télécharger le dossier GitHub. Nous recommandons la création d'un environnement virtuel. Lancer le fichier run.py.

### Developpé par : Morgan Godin

## Les étapes de la réalisation du projet 

### La base de données

Cette application web s'appuie sur une base de données conçue à partir d'un modèle conceptuel de données avec le logiciel MySQL Workbench. La base a été ensuite modélisé grâce à SQLAlchemy.

La base de données a été rempli avec le logiciel SQLite par des données récupérées sur une collection de couvertures pulp hébergée sur Internet Archive sous licence Creative Commons. 

### L'application web 

L'application a été développé dans le langage Python dans un environnement créé par Pycharm. L'arborescence est conditionnée par les consignes de l'exercice. Elle concerne la navigation, une possibilité de recherche, d'ajout, d'édition et de modification des données. Nous avons donc créé un index organisé par titres de magazines et par numéros, une outil de recherche simple (par artistes, numéros, titres de magazine et éditeur) et nous avons pris la liberté de créer une galerie de couvertures qui nous semblait être un moyen agréable de naviguer dans la collection à travers le visuel. Chacun de ses moyens de naviguer dans le site renvoie à des notices sur chaque couverture. Enfin nous avons développé un formulaire d'ajout, un outil de modification et la possibilité de supprimer les données d'une couverture sans altérer le reste de la base de données. 

### Le graphisme 

La mise en page du site s'appuie sur les outils du framework Bootstrap. 


