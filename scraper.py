import requests
from bs4 import BeautifulSoup
import json
from feedgen.feed import FeedGenerator
import os

def scrape_humble_software():
    print("Début du scraping...")
    url = "https://www.humblebundle.com/software"
    # User-Agent pour éviter d'être bloqué
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraction des données JSON
        data_script = soup.find('script', id='webpack-bundle-page-data')
        if not data_script:
            print("ERREUR : Impossible de trouver la balise script 'webpack-bundle-page-data'.")
            return

        json_data = json.loads(data_script.string)
        bundles = json_data.get('content_index', {}).get('bundle_data', [])

        if not bundles:
            print("INFO : Aucun bundle logiciel trouvé actuellement.")
            return

        fg = FeedGenerator()
        fg.id('https://www.humblebundle.com/software')
        fg.title('Humble Software RSS')
        fg.link(href='https://www.humblebundle.com/software', rel='alternate')
        fg.description('Flux RSS automatisé pour Humble Software Bundles')

        for bundle in bundles:
            name = bundle.get('bundle_name')
            machine_name = bundle.get('machine_name')
            link = f"https://www.humblebundle.com/software/{machine_name}"
            img = bundle.get('bundle_image_tile')

            fe = fg.add_entry()
            fe.id(link)
            fe.title(name)
            fe.link(href=link)
            fe.description(f'<img src="{img}"><br>Nouveau bundle : {name}')

        # Sauvegarde forcée à la racine
        output_file = 'software_feed.xml'
        fg.rss_file(output_file)
        print(f"SUCCÈS : Fichier '{output_file}' généré avec {len(bundles)} bundles.")

    except Exception as e:
        print(f"ERREUR CRITIQUE : {str(e)}")

if __name__ == "__main__":
    scrape_humble_software()

if __name__ == "__main__":
    scrape_humble_software()
