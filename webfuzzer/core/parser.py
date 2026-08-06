# core/parser.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def extract_links(base_url, html):
    soup = BeautifulSoup(html, "html.parser")
    base_domain = urlparse(base_url).netloc
    links = set()

    ATTR_TAGS = {
        "a": "href",
        "link": "href",
        "area": "href",
        "form": "action",
        "script": "src",
        "img": "src",
        "iframe": "src",
        "frame": "src",
        "embed": "src",
        "object": "data"
    }

    for tag, attr in ATTR_TAGS.items():
        for t in soup.find_all(tag):
            url = t.get(attr)
            if not url:
                continue

            full = urljoin(base_url, url)
            if urlparse(full).netloc == base_domain:
                links.add(full)

    return links

def extract_forms(base_url, html):
    soup = BeautifulSoup(html, "html.parser")
    forms = []

    for form in soup.find_all("form"):
        action = form.get("action")
        if not action:
            full_action = base_url
        else:
            full_action = urljoin(base_url, action)

        method = form.get("method", "GET").upper()

        inputs = []

        for inp in form.find_all("input"):
            name = inp.get("name")
            if name:
                inputs.append(name)

        for ta in form.find_all("textarea"):
            name = ta.get("name")
            if name:
                inputs.append(name)

        for sel in form.find_all("select"):
            name = sel.get("name")
            if name:
                inputs.append(name)

        for btn in form.find_all("button"):
            name = btn.get("name")
            if name:
                inputs.append(name)

        forms.append({
            "url": full_action,
            "method": method,
            "inputs": inputs
        })

    return forms
