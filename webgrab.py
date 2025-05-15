import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import mimetypes

def make_folder(name):
    if not os.path.exists(name):
        os.makedirs(name)

def save_file(path, content, mode='wb'):
    with open(path, mode) as f:
        f.write(content)

def download_file(url, folder):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            if not filename:
                ext = mimetypes.guess_extension(r.headers.get('content-type', '').split(';')[0]) or '.bin'
                filename = 'file' + ext
            path = os.path.join(folder, filename)
            save_file(path, r.content)
            print(f'saved {url} -> {path}')
    except: pass

def extract_links(soup, base):
    links = set()
    tags_attrs = {
        'link': 'href',
        'script': 'src',
        'img': 'src',
        'iframe': 'src',
        'source': 'src',
        'video': 'src',
        'audio': 'src',
        'embed': 'src',
        'object': 'data'
    }
    for tag, attr in tags_attrs.items():
        for element in soup.find_all(tag):
            url = element.get(attr)
            if url:
                full_url = urljoin(base, url)
                links.add(full_url)
    return links

def main():
    url = input('url: ').strip()
    parsed = urlparse(url)
    base = f'{parsed.scheme}://{parsed.netloc}'
    folder = parsed.netloc
    make_folder(folder)
    try:
        r = requests.get(url, timeout=5)
    except:
        return
    html = r.content
    save_file(os.path.join(folder, 'index.html'), html)
    soup = BeautifulSoup(html, 'html.parser')
    resources = extract_links(soup, base)
    for res in resources:
        download_file(res, folder)

if __name__ == '__main__':
    main()
