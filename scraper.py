import requests
from bs4 import BeautifulSoup
import json
from feedgen.feed import FeedGenerator

def scrape_humble_software():
    print("Début du scraping sur la version détectée...")
    url = "https://www.humblebundle.com/software"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ciblage précis de la nouvelle balise ID identifiée dans ton code source
        script_tag = soup.find('script', id='landingPage-json-data')
        if not script_tag:
            print("ERREUR : Balise 'landingPage-json-data' introuvable.")
            return

        json_data = json.loads(script_tag.string)
        
        # Accès au chemin spécifique des produits software
        # Structure : data -> software -> mosaic -> [0] -> products
        try:
            software_data = json_data['data']['software']['mosaic']
            products = software_data[0]['products']
        except (KeyError, IndexError):
            print("ERREUR : Impossible de naviguer dans la structure JSON.")
            return

        fg = FeedGenerator()
        fg.id(url)
        fg.title('Humble Software Bundles')
        fg.link(href=url, rel='alternate')
        fg.description('Dernières offres logicielles de Humble Bundle')

        for item in products:
            title = item.get('tile_name')
            # Le product_url est souvent relatif (ex: /software/bundle-name)
            link = "https://www.humblebundle.com" + item.get('product_url', '')
            img = item.get('tile_image')
            desc = item.get('short_marketing_blurb', 'Nouveau bundle disponible !')

            fe = fg.add_entry()
            fe.id(link)
            fe.title(title)
            fe.link(href=link)
            fe.description(f'<img src="{img}"><br>{desc}')

        fg.rss_file('software_feed.xml')
        print(f"SUCCÈS : {len(products)} bundles détectés et ajoutés au flux.")

    except Exception as e:
        print(f"ERREUR : {str(e)}")

if __name__ == "__main__":
    scrape_humble_software()            fe.link(href=link)
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
