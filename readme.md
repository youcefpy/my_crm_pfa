
## Instalation of pipenv 
you need first to install the pipenv with this command : 
```markdown
pip install pipenv

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

## Run the server 
```bash
py manage.py runserver
```

## todo 
this paragraphe is wroten in French

j'ai une serie de prospets :
un prospet peut devenir client comment je peut le perdre 
si le prospet et client dont je vais l'ajouter a la table client et je vais le retirer de prospet
si il est perdu je le supprime 
dans la page d'acceuil on ajoutes des graphe comme le nombre de prospet sous forme de bar 
le nombre de clients on ajoute des filtre par annees, par source et tous 
le nombre de clients perdus source de la magorité de client perdu.
agent qui a plus de clients