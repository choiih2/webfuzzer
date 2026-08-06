# core/utils.py
from urllib.parse import urlparse

def get_endpoint_string(url):
    parsed = urlparse(url)
    endpoint = parsed.path or "/"
    if parsed.query:
        endpoint += "?" + parsed.query
    return endpoint
