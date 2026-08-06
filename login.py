# core/login.py
import re
from urllib.parse import urljoin, urlparse
from core.session import fetch
import core.session as session

def _extract_token(html):
    m = re.search(r"name=['\"]user_token['\"]\s+value=['\"]([0-9a-f]+)['\"]", html)
    return m.group(1) if m else None

def do_login(base_url, email=None, password=None):
    if not email or not password:
        return False

    LOGIN_URL = urljoin(base_url, "/login.php")

    # 1) GET으로 로그인 페이지 받아서 user_token 추출
    r_get, _ = fetch(LOGIN_URL, method="GET")
    if not r_get:
        return False
    token = _extract_token(r_get.text)
    if not token:
        print("[!] user_token not found")
        return False

    # 2) username / password / Login / user_token 함께 POST
    payload = {
        "username": email,      # DVWA는 username 필드
        "password": password,
        "Login": "Login",
        "user_token": token,
    }
    r_post, _ = fetch(LOGIN_URL, method="POST", data=payload)
    if not r_post:
        return False

    # 3) DVWA security 레벨 쿠키를 도메인 명시해서 심는다
    #    (도메인 없이 심으면 서버가 준 security 쿠키와 충돌 → CookieConflictError)
    host = urlparse(base_url).hostname
    session.SESSION.cookies.set("security", "low", domain=host, path="/")

    # 4) 성공 판정: 로그인 후에도 여전히 login 페이지면 실패
    return "login.php" not in r_post.url.lower() and "login ::" not in r_post.text.lower()
