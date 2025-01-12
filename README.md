# NLP_JOBS

Ce projet est un bot qui scrute les offres d'emploi postée sur le site [d'offres d'emplois, stages et post-doc](http://w3.erss.univ-tlse2.fr/membre/tanguy/offres.html) maintenu par Ludovic Tanguy et les poste sur un canal Discord.

## Installation

1. Clonez le dépôt :

2. Créer env_virtuel

3. Installez les dépendances :
pip install -r requirements.txt

4. Créez un fichier .env à la racine du projet et ajoutez vos variables d'environnement :

DISCORD_WEBHOOK_URL=votre_webhook_url
SITE_URL=votre_site_url
PATH=votre_chemin

5. Exécutez le script 
python src/main.py
