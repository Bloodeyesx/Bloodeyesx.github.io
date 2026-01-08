import requests
from bs4 import BeautifulSoup
import json
from feedgen.feed import FeedGenerator
import re

def scrape_humble_software():
    print("Début du scraping robuste...")
    url = "https://www.humblebundle.com/software"
    # Headers plus complets pour simuler un vrai navigateur
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # RECHERCHE ROBUSTE : On cherche n'importe quel script qui contient "bundle_data"
        json_data = None
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'bundle_data' in script.string:
                try:
                    # On tente d'extraire le JSON brut du script
                    json_data = json.loads(script.string)
                    break
                except:
                    continue

        if not json_data:
            print("ERREUR : Impossible d'extraire les données JSON de la page.")
            return

        # Extraction selon la structure actuelle de Humble
        bundles = json_data.get('content_index', {}).get('bundle_data', [])
        if not bundles:
            # Test d'une structure alternative
            bundles = json_data.get('bundle_data', [])

        if not bundles:
            print("INFO : Aucun bundle trouvé dans les données extraites.")
            return

        fg = FeedGenerator()
        fg.id('https://www.humblebundle.com/software')
        fg.title('Humble Software RSS')
        fg.link(href='https://www.humblebundle.com/software', rel='alternate')
        fg.description('Flux RSS automatisé pour Humble Software Bundles')

        count = 0
        for bundle in bundles:
            name = bundle.get('bundle_name')
            machine_name = bundle.get('machine_name')
            if not machine_name: continue
            
            link = f"https://www.humblebundle.com/software/{machine_name}"
            img = bundle.get('bundle_image_tile')

            fe = fg.add_entry()
            fe.id(link)
            fe.title(name)
            fe.link(href=link)
            fe.description(f'<img src="{img}"><br>Nouveau bundle disponible : {name}')
            count += 1

        fg.rss_file('software_feed.xml')
        print(f"SUCCÈS : {count} bundles ajoutés au flux RSS.")

    except Exception as e:
        print(f"ERREUR CRITIQUE : {str(e)}")

if __name__ == "__main__":
    scrape_humble_software()
if __name__ == "__main__":
    scrape_humble_software()
