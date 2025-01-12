# NLP_JOBS

Ce projet est un bot qui scrute les offres d'emploi postées sur le site [d'offres d'emplois, stages et post-doc](http://w3.erss.univ-tlse2.fr/membre/tanguy/offres.html) maintenu par Ludovic Tanguy et les poste sur un canal Discord.

## Installation

1. Clonez le dépôt
git clone https://github.com/votre_utilisateur/NLP_JOBS.git 

2. Créer env_virtuel
python -m venv [name]

3. Installez les dépendances :
pip install -r requirements.txt

4. Créez un dossier "data" et le fichier ".env" à la racine du projet et ajoutez vos variables d'environnement :

DISCORD_WEBHOOK_URL=votre_webhook_url
SITE_URL=http://w3.erss.univ-tlse2.fr/membre/tanguy/offres.html
DATA=data_folder
MEDIA="./media/"

5. Exécutez le script 
python src/tanguy_jobs.py

## Configuration
DISCORD_WEBHOOK_URL : L'URL du webhook Discord où les offres d'emploi seront postées.
SITE_URL : L'URL du site web contenant les offres d'emploi.
DATA : Le chemin du dossier où les données temporaires seront stockées.
MEDIA : Le chemin du dossier contenant les fichiers médias (pour le gif).

## Utilisation
Le script [tanguy_jobs.py](src/tanguy_jobs.py) scrute les offres d'emploi sur le site et poste les nouvelles offres sur le canal Discord configuré. Il peut être exécuté manuellement ou configuré pour s'exécuter à intervalles réguliers à l'aide d'un planificateur de tâches (comme *cron* sur Unix).