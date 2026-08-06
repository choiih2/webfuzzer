# core/detectors_xss.py
import html

XSS_KEYWORDS = [
    "<script", "onerror=", "onload=", "onclick=", "onfocus=",
    "javascript:", "<img", "<svg", "<iframe", "<body", "<video", "<audio"
]

XSS_DANGEROUS_CHARS = ['<', '>', '"', "'", '&']

def is_escaped_version_in_response(payload: str, resp_text: str) -> bool:
    escaped = html.escape(payload, quote=True)
    return escaped in resp_text

def detect_xss(payload, test_resp):
    try:
        t = test_resp.text.lower()
    except Exception:
        return None

    p = payload.lower()

    if p not in t:
        return None

    if not any(ch in payload for ch in XSS_DANGEROUS_CHARS):
        return None

    if is_escaped_version_in_response(payload, t):
        return None

    for kw in XSS_KEYWORDS:
        if kw in t:
            return "XSS"

    return None
