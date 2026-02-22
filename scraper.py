import requests
from bs4 import BeautifulSoup
import json
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

def scrape_humble_software():
    print("Starting scan...")
    url = "https://www.humblebundle.com/software"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        script_tag = soup.find('script', id='landingPage-json-data')
        if not script_tag:
            print("ERROR: Data source not found.")
            return

        json_data = json.loads(script_tag.string)
        products = json_data['data']['software']['mosaic'][0]['products']

        fg = FeedGenerator()
        fg.id(url)
        fg.title('Humble Software Bundles')
        fg.link(href=url, rel='alternate')
        fg.description('Latest software offers from Humble Bundle')
        fg.language('en')
        fg.lastBuildDate(datetime.now(timezone.utc))

        for item in products:
            title = item.get('tile_name')
            link = "https://www.humblebundle.com" + item.get('product_url', '')
            img = item.get('tile_image')
            desc = item.get('short_marketing_blurb', 'New bundle available!')
            unique_id = item.get('machine_name', link)

            fe = fg.add_entry()
            fe.id(unique_id)
            fe.title(title)
            fe.link(href=link)
            fe.description(f'<img src="{img}"><br>{desc}')
            fe.published(datetime.now(timezone.utc))

        fg.rss_file('software_feed.xml')
        print(f"SUCCESS: {len(products)} bundles added to feed.")

    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    scrape_humble_software()
