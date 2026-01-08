import requests
from bs4 import BeautifulSoup
import json
from feedgen.feed import FeedGenerator
import os

def scrape_humble_software():
    url = "https://www.humblebundle.com/software"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # On récupère le script JSON qui contient tous les bundles
    data = soup.find('script', id='webpack-bundle-page-data')
    if not data:
        return

    json_data = json.loads(data.string)
    bundles = json_data.get('content_index', {}).get('bundle_data', [])

    fg = FeedGenerator()
    fg.id('https://www.humblebundle.com/software')
    fg.title('Humble Software RSS - Mon App')
    fg.author({'name': 'Mon App Automatisée'})
    fg.link(href='https://www.humblebundle.com/software', rel='alternate')
    fg.description('Flux RSS des derniers logiciels Humble Bundle')

    for bundle in bundles:
        # On filtre pour ne prendre que les bundles actifs
        name = bundle.get('bundle_name')
        machine_name = bundle.get('machine_name')
        link = f"https://www.humblebundle.com/software/{machine_name}"
        img = bundle.get('bundle_image_tile')

        fe = fg.add_entry()
        fe.id(link)
        fe.title(name)
        fe.link(href=link)
        fe.description(f'<img src="{img}"><br>Nouveau bundle logiciel disponible : {name}')

    # Sauvegarde du fichier
    fg.rss_file('software_feed.xml')

if __name__ == "__main__":
    scrape_humble_software()
