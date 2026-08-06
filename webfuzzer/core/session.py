# core/session.py
import time
import requests

SESSION = requests.Session()
TOTAL_REQUESTS = 0
DEBUG_RESPONSE_SNIPPET_LEN = 200

def fetch(url, method="GET", debug=False, **kwargs):
    """
    기존 코드와 동일한 동작을 하도록 구현.
    returns: (Response or None, elapsed_seconds)
    """
    global TOTAL_REQUESTS
    try:
        start = time.time()
        r = SESSION.request(method, url, timeout=5, **kwargs)
        elapsed = time.time() - start
        TOTAL_REQUESTS += 1

        if debug:
            print("\n────────────────────────────────────────")
            print("📡 FETCH REQUEST")
            print("────────────────────────────────────────")
            print(f"URL     : {url}")
            print(f"METHOD  : {method}")
            if "data" in kwargs:  print(f"DATA    : {kwargs['data']}")
            if "json" in kwargs:  print(f"JSON    : {kwargs['json']}")
            if "headers" in kwargs: print(f"HEADERS : {kwargs['headers']}")
            if "cookies" in kwargs: print(f"COOKIES : {kwargs['cookies']}")

            print("\n────────── RESPONSE ──────────")
            print(f"STATUS  : {r.status_code}")
            print(f"LENGTH  : {len(r.text)}")
            print("SNIPPET :")
            print(r.text[:DEBUG_RESPONSE_SNIPPET_LEN])
            print("────────────────────────────────────────\n")
            print("\n[DEBUG HTML SNIPPET]")
            print(r.text[:400])   # 앞 400자만
            print("-" * 80)

        return r, elapsed

    except Exception as e:
        print("[fetch error]", e)
        return None, 0
