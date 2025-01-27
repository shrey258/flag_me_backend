import requests
import json
from datetime import datetime

def format_price(price):
    return f"₹{price:,.2f}"

def test_search():
    url = "http://127.0.0.1:8000/search-products"
    headers = {
        "Content-Type": "application/json"
    }
    
    # Test different product categories
    queries = [
        "gaming laptop",
        "wireless earbuds",
        "smartwatch"
    ]
    
    for query in queries:
        print(f"\n{'='*80}")
        print(f"Searching for: {query}")
        print(f"{'='*80}")
        
        data = {"query": query}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            print(f"Status Code: {response.status_code}")
            result = response.json()
            
            if "products" in result:
                products = result["products"]
                print(f"\nFound {len(products)} products:\n")
                
                # Sort products by price
                products.sort(key=lambda x: float(x['price']))
                
                for i, product in enumerate(products, 1):
                    print(f"{i}. {product['title'][:100]}...")
                    print(f"   {'Price:':<10} {format_price(product['price'])}")
                    if 'rating' in product:
                        print(f"   {'Rating:':<10} {'⭐' * int(product['rating'])} ({product['rating']})")
                    if 'reviews' in product and product['reviews']:
                        print(f"   {'Reviews:':<10} {product['reviews']:,}")
                    print(f"   {'Platform:':<10} {product['platform']}")
                    print(f"   {'URL:':<10} {product['url']}\n")
            else:
                print("No products found in response")
                print("Response:", result)
                
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print(f"{'='*80}\n")

if __name__ == "__main__":
    print(f"Testing API at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    test_search()
