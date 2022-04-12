# Kanged 

"""
Credits to @Yuuki [github.com/xcscxr]
https://github.com/xcscxr/gplinks-bypass/blob/main/gplinks_bypass.py
"""
 
import asyncio
import cloudscraper
from urllib.parse import urlparse
from bs4 import BeautifulSoup


async def get_link(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    res = client.head(url)
    header_loc = res.headers['location']
    param = header_loc.split('postid=')[-1]
    req_url = f'{p.scheme}://{p.netloc}/{param}'

    p = urlparse(header_loc)
    ref_url = f'{p.scheme}://{p.netloc}/'

    h = { 'referer': ref_url }
    res = client.get(req_url, headers=h, allow_redirects=False)

    bs4 = BeautifulSoup(res.content, 'html.parser')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'referer': ref_url,
        'x-requested-with': 'XMLHttpRequest',
    }
    asyncio.sleep(10)
    res = client.post(final_url, headers=h, data=data)
    try:
        return res.json()['url'].replace('\/','/')
    except Exception as e:
        print(e)
        return False
