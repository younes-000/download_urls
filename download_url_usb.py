import requests
import os
from concurrent.futures import ThreadPoolExecutor # permet de gerer un pool de threads pour telecharger plusieurs fichiers en parallele

urls = [
    "", # les différent fichiers à telecharger
    
]

dossier_destination = r"D:\dl_temp" # Dossier de destination pour les fichiers téléchargés le r devant le chemin permet de ne pas avoir à échapper les caractères spéciaux
os.makedirs(dossier_destination, exist_ok=True) # Crée le dossier de destination si inexistant

def telecharger_fichier(url):
    nom_fichier = os.path.basename(url) # permet d'extraire le nom du fichier à partir de l'url
    chemin_fichier = os.path.join(dossier_destination, nom_fichier) # permet de créer le chemin complet du fichier
    try: # on utilise try pour gérer les erreurs lors du téléchargement
        with requests.get(url, stream=True) as response: # on utilise stream=True pour télécharger le fichier en streaming
            response.raise_for_status() # permet de vérifier si le téléchargement a réussi
            with open(chemin_fichier, 'wb') as fichier:
                for chunk in response.iter_content(chunk_size=8192): # permet de gérer les chunks de données
                    if chunk: # on vérifie si le chunk n'est pas vide
                        fichier.write(chunk) # on écrit le chunk dans le fichier
        print(f"Téléchargement réussi : {chemin_fichier}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de {url} : {e}")

with ThreadPoolExecutor(max_workers=4) as executor: # on utilise ThreadPoolExecutor pour gérer un pool de threads avec 4 threads
    executor.map(telecharger_fichier, urls) # on utilise map pour appliquer la fonction telecharger_fichier à chaque URL en parallèle
