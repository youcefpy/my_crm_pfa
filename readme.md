
## Instalation of pipenv 
you need first to install the pipenv with this command : 
```markdown
pip install pipenv
```

## Clone the project
```bash
git clone https://github.com/youcefpy/my_crm_pfa.git
```

## installing the dependencies and the packages
run this command for installing the dependencies 
```bash
pipenv install
```

## lanching the virtual envirement 
for runing the virtuel envirement you need to run : 

```bash 
pipenv shell 
```

## Make migrations of the database 

```bash
py manage.py makemigraitons
```

## Migrate

```bash
py manage.py migrate
```

## Creating a superuser
```bash
py manage.py createsuperuser
```



## Run the server 
```bash
py manage.py runserver
```

## todo 
This paragraphe is wroten in French

-   Authentification :
    -   Chaque agent doit s'authentifier - FAIT
    -   L'agent peut voir que c'est propre prospet et client - FAIT
    -   L'admin peut avoir une vision global sur les prospet de tous les agents - FAIT
    -   Une authentification est pre-requie pour n'importe quelle actions sur le crm - FAIT

j'ai une serie de prospets :
 - Un prospet peut devenir client comme je peut le perdre -FAIT
 - Si le prospet devient un client donc je vais l'ajouter a la table client et je vais le retirer de prospet. -FAIT
 - Si il est perdu alors je le supprime - FAIT
## Page d'accueil
Dans la page d'accueil on ajoute des graphe: 
- Le nombre de prospet par jour representé par un graphe a bar 
- Le nombre de clients. On ajoute des filtre par jours, mois, annees et par source de prospet 
- Graphe pour le nombre de prospet perdus ainsi que leurs source de provenance (Youtube, Google...).
- Agent qui a plus de clients | agent qui a perdu plus de prospet 

## Chart.js
We use Chart.js for displaying graphs on the dashboard. To use it, we first need to install the package.

## install Chart.js 
with nmp run this command : 
```bash 
npm install chart.js
```