# core/discovery.py
from urllib.parse import urljoin
from core.payload_loader import load_list
from core.parser import extract_links
from core.session import fetch

VALID_CODES = {200, 201, 202, 204, 301, 302, 403}

# 세션을 죽이거나(로그아웃) 퍼징 대상이 아닌 경로는 제외한다.
# logout.php를 밟으면 인증 세션이 풀려서 이후 인증 영역 진단이 전부 무너진다.
EXCLUDE = ("logout.php", "logout")

def _excluded(url):
    return any(x in url for x in EXCLUDE)

def discover_endpoints(base_url, depth, debug=False):
    base = base_url.rstrip("/")
    discovered = set([base])
    queue = [base]
    wordlist = load_list("wordlists/directories.txt")

    print(f"[+] Crawling depth {depth}")

    for d in range(depth):
        next_queue = []
        for current in queue:
            # --- 디렉토리 brute-force는 첫 바퀴(루트)에서만 ---
            if d == 0:
                print("\n────────────────────────────────────────")
                print(f"[DIR BRUTE-FORCE] Target: {current}")
                print("────────────────────────────────────────")
                for i, w in enumerate(wordlist, start=1):
                    url = urljoin(current + "/", w)
                    print(f"[DIR-BF {i}/{len(wordlist)}] → {w}", end="\r")
                    if _excluded(url):
                        continue
                    r, _ = fetch(url, debug=False)
                    if r and r.status_code in VALID_CODES:
                        if url not in discovered:
                            print(f"\n  ✔ Found: {url} (status={r.status_code})")
                            discovered.add(url)
                            next_queue.append(url)

            # --- current 페이지의 링크 추출 (매 depth) ---
            if _excluded(current):
                continue
            r, _ = fetch(current, debug=False)
            if r and r.status_code == 200:
                for link in extract_links(current, r.text):
                    if link not in discovered and not _excluded(link):
                        print(f"  → Discovered link: {link}")
                        discovered.add(link)
                        next_queue.append(link)

        queue = next_queue

    print(f"\n[+] Total discovered endpoints: {len(discovered)}")
    for u in discovered:
        print(" -", u)
    return list(discovered)
