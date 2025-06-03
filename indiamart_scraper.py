import requests
from bs4 import BeautifulSoup
import time
import csv

def fetch_html(url, retries=3, delay=2):
    """
    Fetches HTML content from a given URL with retries and delay.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            if i < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2 # Exponential backoff
            else:
                print(f"Failed to fetch {url} after {retries} attempts.")
                return None
    return None

def parse_srp(html_content):
    """
    Parses the Search Results Page (SRP) HTML and extracts product summaries.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []

    # Find all product cards
    product_cards = soup.select('div.listingCardContainer div.card')

    if not product_cards:
        # print("No product cards found on the SRP for this page.") # Removed for cleaner output if no products on a later page
        return products

    for card in product_cards:
        product_name = None
        product_url = None
        product_price = None
        product_unit = None
        supplier_name = None
        supplier_location = None

        # Product Name and URL
        name_url_tag = card.select_one('div.producttitle a.cardlinks')
        if name_url_tag:
            product_name = name_url_tag.get_text(strip=True)
            product_url = name_url_tag.get('href')

        # Price and Unit
        price_tag = card.select_one('p.price')
        if price_tag:
            product_price_text = price_tag.get_text(strip=True)
            # Split price from unit
            if '/' in product_price_text:
                parts = product_price_text.split('/')
                product_price = parts[0].strip()
                product_unit = '/' + parts[1].strip()
            else:
                product_price = product_price_text
                product_unit = '' # No explicit unit found

        # Supplier Name
        supplier_name_tag = card.select_one('div.companyname a.cardlinks')
        if supplier_name_tag:
            supplier_name = supplier_name_tag.get_text(strip=True)

        # Supplier Location
        supplier_location_tag = card.select_one('div.newLocationUi span:first-child')
        if supplier_location_tag:
            supplier_location = supplier_location_tag.get_text(strip=True)


        products.append({
            'product_name': product_name,
            'product_url': product_url,
            'product_price': product_price,
            'product_unit': product_unit,
            'supplier_name': supplier_name,
            'supplier_location': supplier_location,
            'pdp_wattage': None, # Will be filled from PDP
            'pdp_brand': None,   # Will be filled from PDP
            'pdp_body_material': None, # Will be filled from PDP
            'pdp_ip_rating': None,     # Will be filled from PDP
            'pdp_usage/application': None, # Will be filled from PDP
            'pdp_lighting_color': None, # Will be filled from PDP
            'pdp_color_temperature': None, # Will be filled from PDP
            'pdp_country_of_origin': None, # Will be filled from PDP
            'pdp_description': None, # Will be filled from PDP
            'pdp_supplier_member_since': None, # Will be filled from PDP
            'pdp_supplier_rating': None, # Will be filled from PDP
            'pdp_supplier_reviews_count': None # Will be filled from PDP
        })
    return products

def parse_pdp(html_content, product_data):
    """
    Parses the Product Detail Page (PDP) HTML and updates product data.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract specifications from the table
    spec_table = soup.select_one('div.isq-container table')
    if spec_table:
        rows = spec_table.find_all('tr')
        for row in rows:
            key_tag = row.select_one('td.tdwdt')
            value_tag = row.select_one('td.tdwdt1 span.datatooltip')
            if key_tag and value_tag:
                key = key_tag.get_text(strip=True).replace(' ', '_').replace('/', '_').lower() # Normalize key for dict
                value = value_tag.get_text(strip=True)
                # Adjust for potential mismatches in original headers vs. desired CSV headers
                if key == 'usage_application': # Fix common issue where / is replaced by _
                    product_data['pdp_usage/application'] = value
                elif f'pdp_{key}' in product_data:
                    product_data[f'pdp_{key}'] = value

    # Product Description
    description_tag = soup.select_one('div#descp2 div.pro-descN')
    if description_tag:
        product_data['pdp_description'] = description_tag.get_text(separator=' ', strip=True)

    # Supplier Details on PDP (if different or more detailed)
    # Supplier Member Since
    # Look for the span containing "Member:" and then extract the years
    member_since_span = soup.find('span', class_='fs10', string=lambda text: text and 'Member:' in text)
    if member_since_span:
        product_data['pdp_supplier_member_since'] = member_since_span.get_text(strip=True).replace('Member: ', '')

    # Supplier Rating and Reviews Count
    rating_container = soup.select_one('div#slr_rtng') # This might be present on SRP too, but checking PDP for richness
    if rating_container:
        rating_value_tag = rating_container.select_one('span.bo.color')
        if rating_value_tag:
            product_data['pdp_supplier_rating'] = rating_value_tag.get_text(strip=True)
        reviews_count_tag = rating_container.select_one('span.tcund')
        if reviews_count_tag:
            product_data['pdp_supplier_reviews_count'] = reviews_count_tag.get_text(strip=True)

    return product_data

def save_to_csv(data, filename="indiamart_led_lights.csv"):
    """
    Saves the scraped data to a CSV file.
    """
    if not data:
        print("No data to save.")
        return

    # Define fieldnames explicitly to ensure order and cover all PDP fields
    # Ensure this matches the keys used in the parse_srp and parse_pdp functions
    fieldnames = [
        'product_name', 'product_url', 'product_price', 'product_unit',
        'supplier_name', 'supplier_location',
        'pdp_wattage', 'pdp_brand', 'pdp_body_material', 'pdp_ip_rating',
        'pdp_usage/application', 'pdp_lighting_color', 'pdp_color_temperature',
        'pdp_country_of_origin', 'pdp_description', 'pdp_supplier_member_since',
        'pdp_supplier_rating', 'pdp_supplier_reviews_count'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data successfully saved to {filename}")

def main():
    search_query = "led lights"
    base_srp_url = f"https://dir.indiamart.com/search.mp?ss={search_query.replace(' ', '+')}"
    all_products_data = []
    page_number = 1
    max_products_to_scrape = 100 # Target up to 100 products

    while len(all_products_data) < max_products_to_scrape:
        srp_url = f"{base_srp_url}&page_no={page_number}"
        print(f"Scraping SRP Page {page_number}: {srp_url}")
        srp_html = fetch_html(srp_url)

        if srp_html:
            current_page_products = parse_srp(srp_html)
            if not current_page_products:
                print(f"No more products found on page {page_number}. Stopping.")
                break # Exit if no products are found on the current page

            all_products_data.extend(current_page_products)
            print(f"Collected {len(current_page_products)} products from page {page_number}. Total collected: {len(all_products_data)}")

            # Limit the number of products to scrape to max_products_to_scrape
            if len(all_products_data) >= max_products_to_scrape:
                all_products_data = all_products_data[:max_products_to_scrape]
                print(f"Reached target of {max_products_to_scrape} products. Proceeding to PDP scraping.")
                break

            page_number += 1
            time.sleep(3) # Be polite, wait between SRP page requests
        else:
            print(f"Failed to retrieve SRP HTML for page {page_number}. Exiting pagination loop.")
            break

    print(f"\nProceeding to scrape PDPs for {len(all_products_data)} collected products...")
    for i, product in enumerate(all_products_data):
        if product['product_url']:
            print(f"Scraping PDP for '{product['product_name']}' ({i+1}/{len(all_products_data)})")
            pdp_html = fetch_html(product['product_url'])
            if pdp_html:
                all_products_data[i] = parse_pdp(pdp_html, product)
            time.sleep(2) # Be polite, wait between PDP requests
        else:
            print(f"Skipping product {product['product_name']} due to missing URL.")

    save_to_csv(all_products_data)

if __name__ == "__main__":
    main()