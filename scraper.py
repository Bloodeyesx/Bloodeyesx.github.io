import requests
from bs4 import BeautifulSoup
import json
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
from tinydb import TinyDB, Query

def scrape_humble_software():
    print("📸 Initializing Darkroom Scan...")
    url = "https://www.humblebundle.com/software"
    db = TinyDB('bundles_db.json')
    Bundle = Query()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        script_tag = soup.find('script', id='landingPage-json-data')
        json_data = json.loads(script_tag.string)
        products = json_data['data']['software']['mosaic'][0]['products']

        fg = FeedGenerator()
        fg.id(url)
        fg.title('Humble Software Bundles')
        fg.link(href=url, rel='alternate')
        fg.description('Latest software offers from Humble Bundle')
        fg.lastBuildDate(datetime.now(timezone.utc))

        for item in products:
            unique_id = item.get('machine_name', item.get('product_url'))
            title = item.get('tile_name')
            link = "https://www.humblebundle.com" + item.get('product_url', '')
            img = item.get('tile_image')
            desc = item.get('short_marketing_blurb', 'New bundle detected.')

            # Check if we already have this in the archive
            existing = db.search(Bundle.id == unique_id)
            
            if not existing:
                pub_date = datetime.now(timezone.utc).isoformat()
                # Store EVERYTHING the UI needs
                db.insert({
                    'id': unique_id,
                    'title': title,
                    'link': link,
                    'image': img,
                    'description': desc,
                    'published_at': pub_date
                })
                print(f"➕ New entry exposed: {title}")
            else:
                pub_date = existing[0]['published_at']

            # Update RSS Feed
            fe = fg.add_entry()
            fe.id(unique_id)
            fe.title(title)
            fe.link(href=link)
            fe.description(f'<img src="{img}"><br>{desc}')
            fe.published(datetime.fromisoformat(pub_date))

        fg.rss_file('software_feed.xml')
        print(f"✔️ Scan complete. {len(products)} items in current archive.")

    except Exception as e:
        print(f"❌ SCAN ERROR: {str(e)}")

if __name__ == "__main__":
    scrape_humble_software()
