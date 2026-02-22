import requests
from bs4 import BeautifulSoup
import json
import os
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
from tinydb import TinyDB, Query # <-- Added TinyDB

def scrape_humble_software():
    print("Starting scrape...")
    url = "https://www.humblebundle.com/software"
    db_file = 'bundles_db.json'
    
    # Initialize TinyDB
    db = TinyDB(db_file)
    Bundle = Query()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        script_tag = soup.find('script', id='landingPage-json-data')
        if not script_tag:
            print("ERROR: 'landingPage-json-data' tag not found.")
            return

        json_data = json.loads(script_tag.string)
        
        try:
            products = json_data['data']['software']['mosaic'][0]['products']
        except (KeyError, IndexError, TypeError):
            print("ERROR: Invalid JSON structure or no products found.")
            return

        fg = FeedGenerator()
        fg.id(url)
        fg.title('Humble Software Bundles')
        fg.link(href=url, rel='alternate')
        fg.description('Latest software offers from Humble Bundle')
        fg.language('en')
        fg.lastBuildDate(datetime.now(timezone.utc))

        for item in products:
            unique_id = item.get('machine_name', item.get('product_url'))
            title = item.get('tile_name')
            link = "https://www.humblebundle.com" + item.get('product_url', '')
            img = item.get('tile_image')
            desc = item.get('short_marketing_blurb', 'New bundle available!')

            # --- TINYDB STATE LOGIC ---
            existing_entry = db.search(Bundle.id == unique_id)
            
            if not existing_entry:
                # First time seeing this bundle
                pub_date = datetime.now(timezone.utc).isoformat()
                db.insert({
                    'id': unique_id,
                    'title': title,
                    'published_at': pub_date,
                    'last_seen': pub_date
                })
                print(f"🆕 New entry logged: {title}")
            else:
                # Already exists, keep the original published date
                pub_date = existing_entry[0]['published_at']
                db.update({'last_seen': datetime.now(timezone.utc).isoformat()}, Bundle.id == unique_id)
            # ---------------------------

            fe = fg.add_entry()
            fe.id(unique_id)
            fe.title(title)
            fe.link(href=link)
            fe.description(f'<img src="{img}"><br>{desc}')
            
            # Use the stored date so RSS readers don't get duplicates
            fe.published(datetime.fromisoformat(pub_date))

        fg.rss_file('software_feed.xml')
        print(f"SUCCESS: {len(products)} bundles processed. Database updated.")

    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    scrape_humble_software()
