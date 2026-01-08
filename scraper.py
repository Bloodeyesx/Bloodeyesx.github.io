import requests
from bs4 import BeautifulSoup
import json
from feedgen.feed import FeedGenerator

def scrape_humble_software():
    print("Début du scraping...")
    url = "https://www.humblebundle.com/software"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Identification de la balise de données (basé sur votre code source fourni)
        script_tag = soup.find('script', id='landingPage-json-data')
        if not script_tag:
            print("ERREUR : Balise 'landingPage-json-data' introuvable.")
            return

        json_data = json.loads(script_tag.string)
        
        # Navigation vers les produits software
        try:
            products = json_data['data']['software']['mosaic'][0]['products']
        except (KeyError, IndexError):
            print("ERREUR : Structure JSON invalide ou aucun produit trouvé.")
            return

        fg = FeedGenerator()
        fg.id(url)
        fg.title('Humble Software Bundles')
        fg.link(href=url, rel='alternate')
        fg.description('Dernières offres logicielles de Humble Bundle')

        for item in products:
            title = item.get('tile_name')
            # Reconstruction de l'URL complète
            link = "https://www.humblebundle.com" + item.get('product_url', '')
            img = item.get('tile_image')
            desc = item.get('short_marketing_blurb', 'Nouveau bundle disponible !')

            fe = fg.add_entry()
            fe.id(link)
            fe.title(title)
            fe.link(href=link)
            fe.description(f'<img src="{img}"><br>{desc}')

        # Génération du fichier XML à la racine
        fg.rss_file('software_feed.xml')
        print(f"SUCCÈS : {len(products)} bundles ajoutés au flux.")

    except Exception as e:
        print(f"ERREUR : {str(e)}")

# Appel de la fonction (Sur une ligne séparée !)
if __name__ == "__main__":
    scrape_humble_software()
