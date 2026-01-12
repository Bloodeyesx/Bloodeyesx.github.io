import requests
from bs4 import BeautifulSoup
import json
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

def scrape_humble_software():
    print("Starting scrape...")
    url = "https://www.humblebundle.com/software"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Extract the hidden JSON data
        script_tag = soup.find('script', id='landingPage-json-data')
        if not script_tag:
            print("ERROR: 'landingPage-json-data' tag not found.")
            return

        json_data = json.loads(script_tag.string)
        
        # 2. Navigate the JSON structure to find products
        try:
            products = json_data['data']['software']['mosaic'][0]['products']
        except (KeyError, IndexError, TypeError):
            print("ERROR: Invalid JSON structure or no products found.")
            return

        # 3. Initialize the RSS Feed Generator
        fg = FeedGenerator()
        fg.id(url)
        fg.title('Humble Software Bundles')
        fg.link(href=url, rel='alternate')
        fg.description('Latest software offers from Humble Bundle')
        fg.language('en')
        
        # IMPORTANT: Update the build date so RSS readers see it as "Fresh"
        fg.lastBuildDate(datetime.now(timezone.utc))

        # 4. Loop through products and add to feed
        for item in products:
            title = item.get('tile_name')
            link = "https://www.humblebundle.com" + item.get('product_url', '')
            img = item.get('tile_image')
            desc = item.get('short_marketing_blurb', 'New bundle available!')
            
            # Use machine_name as ID if available, otherwise fallback to link
            unique_id = item.get('machine_name', link)

            fe = fg.add_entry()
            fe.id(unique_id)
            fe.title(title)
            fe.link(href=link)
            fe.description(f'<img src="{img}"><br>{desc}')
            
            # Set the publication date to now (UTC)
            fe.published(datetime.now(timezone.utc))

        # 5. Save the file
        fg.rss_file('software_feed.xml')
        print(f"SUCCESS: {len(products)} bundles added to feed.")

    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    scrape_humble_software()
