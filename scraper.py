import requests
from bs4 import BeautifulSoup
import json
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

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
        
        # Identification de la balise de données
        script_tag = soup.find('script', id='landingPage-json-data')
        if not script_tag:
            print("ERREUR : Balise 'landingPage-json-data' introuvable.")
            return

        json_data = json.loads(script_tag.string)
        
        # Navigation vers les produits software
        try:
            # Note: This path is specific to Humble's current layout
            products = json_data['data']['software']['mosaic'][0]['products']
        except (KeyError, IndexError, TypeError):
            print("ERREUR : Structure JSON invalide ou aucun produit trouvé.")
            return

        fg = FeedGenerator()
        fg.id(url)
        fg.title('Humble Software Bundles')
        fg.link(href=url, rel='alternate')
        fg.description('Dernières offres logicielles de Humble Bundle')
        fg.language('en')
        
        # IMPORTANT: Set the last build date to NOW (UTC)
        # This ensures the XML file content changes every time, satisfying git
        fg.lastBuildDate(datetime.now(timezone.utc))

        for item in products:
            title = item.get('tile_name')
            # Reconstruction de l'URL complète
            link = "https://www.humblebundle.com" + item.get('product_url', '')
            img = item.get('tile_image')
            desc = item.get('short_marketing_blurb', 'Nouveau bundle disponible !')
            
            # Essayons de trouver une date de fin ou de début pour l'ID unique
            # Humble uses 'machine_name' as a unique ID usually
            unique_id = item.get('machine_name', link)

            fe = fg.add_entry()
            fe.id(unique_id)
            fe.title(title)
            fe.link(href=link)
            fe.description(f'<img src="{img}"><br>{desc}')
            
            # --- DATE HANDLING ---
            # If the JSON doesn't have a clean date, we default to the current time
            # so the RSS reader accepts it. 
            fe.published(datetime.now(timezone.utc))

        # Génération du fichier XML à la racine
        fg.rss_file('software_feed.xml')
        print(f"SUCCÈS : {len(products)} bundles ajoutés au flux.")

    except Exception as e:
        print(f"ERREUR : {str(e)}")

if __name__ == "__main__":
    scrape_humble_software()        fg.description('Dernières offres logicielles de Humble Bundle')

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
