# Tweepy mining


This program use Tweepy (Twitter API) to search given terms and save a minedb.
There are 3 scripts.
# 1º buscatweets.py
The first script is the search script (buscatweets.py)
Here you need inset you Keys and tokens from developer.twitter.com (Consumer API keys : API key / API secret key ; Access token & access token secret ) I regenerate my Keys. You also need to set the name of the database and which terms will be searched.
# 2º classification.py
Script that does the analysis. The searches are in PT-BR and translated into English for analysis. The google translation API has a request limit.
Use google cloud (API TRASNLATE) or translate it differently.

# 3º calcmedias.py
Script calculates averages and saves PNG charts (calcmedias.py)
