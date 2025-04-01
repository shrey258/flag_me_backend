from typing import List, Dict, Optional
import asyncio
import httpx
from bs4 import BeautifulSoup
from price_parser import Price
from datetime import datetime
from urllib.parse import quote_plus, urlencode
import os
from dotenv import load_dotenv
import random
import json

load_dotenv()

class ProductSearchResult:
    def __init__(self, title: str, price: float, url: str, platform: str, image_url: str = None, rating: Optional[float] = None, reviews: Optional[int] = None):
        self.title = title
        self.price = price
        self.url = url
        self.platform = platform
        self.image_url = image_url
        self.rating = rating
        self.reviews = reviews

class EcommerceSearcher:
    def __init__(self):
        self.amazon_tag = os.getenv("AMAZON_AFFILIATE_TAG")
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
        ]
        
    def _get_headers(self):
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }

    def _create_amazon_affiliate_url(self, base_url: str) -> str:
        """Create Amazon affiliate URL with tracking ID"""
        if not self.amazon_tag:
            return base_url
            
        # Remove existing tags if present
        if "tag=" in base_url:
            base_url = base_url.split("tag=")[0].rstrip("&?")
            
        separator = "&" if "?" in base_url else "?"
        return f"{base_url}{separator}tag={self.amazon_tag}"

    async def search_amazon(self, query: str, max_results: int = 10) -> List[ProductSearchResult]:
        async with httpx.AsyncClient(headers=self._get_headers(), timeout=30.0, follow_redirects=True) as client:
            try:
                # First, try the mobile API endpoint
                api_params = {
                    'k': query,
                    'ref': 'nb_sb_noss',
                    'sprefix': quote_plus(query),
                    'crid': '2MVMZ14C0WRQW',
                    'ref_': 'nav_bb_sb'
                }
                
                url = f"https://www.amazon.in/s?{urlencode(api_params)}"
                response = await client.get(url)
                
                if response.status_code != 200:
                    print(f"Amazon search failed with status code: {response.status_code}")
                    return []
                
                soup = BeautifulSoup(response.text, 'html.parser')
                products = []
                
                # Multiple product card selectors to try
                product_selectors = [
                    '.s-result-item[data-component-type="s-search-result"]',
                    '.sg-col-4-of-12',
                    '.sg-col-4-of-16',
                    '.s-result-item'
                ]
                
                for selector in product_selectors:
                    items = soup.select(selector)
                    if items:
                        for item in items:
                            if len(products) >= max_results:
                                break
                                
                            try:
                                # Multiple selectors for each element
                                title_elem = (
                                    item.select_one('h2 .a-link-normal') or
                                    item.select_one('.a-text-normal') or
                                    item.select_one('h2 a')
                                )
                                
                                price_elem = (
                                    item.select_one('.a-price .a-offscreen') or
                                    item.select_one('.a-price') or
                                    item.select_one('.a-color-price')
                                )
                                
                                link_elem = (
                                    item.select_one('h2 .a-link-normal') or
                                    item.select_one('h2 a') or
                                    item.select_one('.a-link-normal')
                                )
                                
                                img_elem = (
                                    item.select_one('img.s-image') or
                                    item.select_one('.s-image')
                                )
                                
                                if not all([title_elem, price_elem, link_elem]):
                                    continue
                                
                                # Get product URL and add affiliate tag
                                product_url = link_elem.get('href', '')
                                if not product_url:
                                    continue
                                    
                                if not product_url.startswith('http'):
                                    product_url = f"https://www.amazon.in{product_url}"
                                
                                affiliate_url = self._create_amazon_affiliate_url(product_url)
                                
                                # Extract price
                                price_text = price_elem.text.strip() if price_elem else ''
                                if not price_text:
                                    continue
                                    
                                try:
                                    price = Price.fromstring(price_text).amount_float
                                except:
                                    continue
                                
                                if not price:
                                    continue
                                
                                # Create product result
                                product = ProductSearchResult(
                                    title=title_elem.text.strip(),
                                    price=price,
                                    url=affiliate_url,
                                    platform="Amazon",
                                    image_url=img_elem['src'] if img_elem else None
                                )
                                
                                products.append(product)
                                
                            except Exception as e:
                                print(f"Error processing Amazon product: {str(e)}")
                                continue
                        
                        if products:
                            break
                
                return products
                
            except Exception as e:
                print(f"Error searching Amazon: {str(e)}")
                return []

    async def search_all(self, query: str, min_price: float = None, max_price: float = None) -> List[ProductSearchResult]:
        """Search all platforms (currently only Amazon) with optional price filtering"""
        # Add a small delay to avoid rate limiting
        await asyncio.sleep(random.uniform(0.5, 1.5))
        results = await self.search_amazon(query)
        
        # Deduplicate products based on title similarity
        unique_products = {}
        for product in results:
            # Create a simplified title by removing common variations
            simple_title = product.title.lower()
            for remove in ['/','(', ')', '[', ']', '{', '}', ',']:
                simple_title = simple_title.replace(remove, ' ')
            simple_title = ' '.join(simple_title.split())
            
            # If we haven't seen this product or if this one is cheaper
            if simple_title not in unique_products or product.price < unique_products[simple_title].price:
                unique_products[simple_title] = product
        
        # Convert back to list and sort
        final_results = list(unique_products.values())
        sorted_results = sorted(final_results, key=lambda x: (x.price if x.price else float('inf')))
        
        # Apply price filters if specified
        if min_price is not None or max_price is not None:
            filtered_results = []
            for product in sorted_results:
                if min_price is not None and product.price < min_price:
                    continue
                if max_price is not None and product.price > max_price:
                    continue
                filtered_results.append(product)
            return filtered_results
        
        return sorted_results
