# core/login.py
from urllib.parse import urljoin
from core.session import fetch

from core.session import fetch
from urllib.parse import urljoin

def do_login(base_url, email=None, password=None):
    if not email or not password:
        return False
    LOGIN_URL = urljoin(base_url, "/login.php")
    payload = {
        "email": email,
        "password": password,
    }
    r, _ = fetch(LOGIN_URL, method="POST", data=payload, debug=True)
    return r and r.status_code == 200
