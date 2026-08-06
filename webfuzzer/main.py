# main.py
import argparse
import time
from core.discovery import discover_endpoints
from core.parser import extract_forms
from core.injector import build_injection_points
from core.fuzzer import fuzz_injection_point
from core.login import do_login
from core.cleanup import get_last_post_id, delete_new_posts_after
from core.report import generate_report
from core.payload_loader import load_default_sqli_payloads, load_default_xss_payloads
import core.session as session
from core.config import SQLI_ERROR_FILE, SQLI_TIME_FILE, XSS_PAYLOADS

def run(url, depth, debug=False, enable_xss=False, enable_sqli=False, no_cleanup=False):
    log_vulns = []
    start = time.time()

    # DB cleanup: 게시판형 타깃에서만 의미가 있음. DB가 없거나 --no-cleanup이면 건너뜀
    base_post_id = None
    if no_cleanup:
        print("[CLEAN] Cleanup disabled")
    else:
        try:
            base_post_id = get_last_post_id()
            print(f"[CLEAN] Base post id = {base_post_id}")
        except Exception as e:
            print(f"[CLEAN] DB unavailable, skipping cleanup ({e})")
            base_post_id = None

    sqli_payloads = load_default_sqli_payloads()
    xss_payloads  = load_default_xss_payloads()
    payloads = {}
    if enable_sqli:
        payloads.update(sqli_payloads)
    if enable_xss:
        payloads.update(xss_payloads)
    if not payloads:
        payloads = { **sqli_payloads, **xss_payloads }
        enable_sqli = True
        enable_xss = True

    endpoints = discover_endpoints(url, depth, debug=debug)
    for ep in endpoints:
        print(f"\n[+] Scanning endpoint: {ep}")
        base_resp, _ = session.fetch(ep, debug=debug)
        if not base_resp:
            continue
        html_forms = extract_forms(ep, base_resp.text)
        print("[debug] forms:", html_forms)
        ips = build_injection_points(ep, html_forms)
        for name, target, method, data_fields in ips:
            print(f"   -> Injection: {name}")
            fuzz_injection_point(
                target,
                method,
                data_fields,
                payloads,
                base_resp,
                name,
                log_vulns,
                url,
                enable_sqli,
                enable_xss,
                debug=debug
            )

    # 퍼징으로 생성된 데이터 정리 (cleanup이 활성화되고 DB 연결에 성공했을 때만)
    if not no_cleanup and base_post_id is not None:
        try:
            delete_new_posts_after(base_post_id)
        except Exception as e:
            print(f"[CLEANUP] skipped ({e})")

    end = time.time()
    duration = end - start
    report_text = generate_report(url, log_vulns, endpoints, duration, session.TOTAL_REQUESTS)
    with open("fuzz_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
    print("[+] Report written to fuzz_report.txt")

def inject_cookies(cookie_string, url=None):
    """'PHPSESSID=abc; security=low' 형태의 문자열을 전역 세션에 심는다."""
    from urllib.parse import urlparse
    domain = urlparse(url).hostname if url else None
    for pair in cookie_string.split(";"):
        if "=" in pair:
            k, v = pair.strip().split("=", 1)
            if domain:
                session.SESSION.cookies.set(k.strip(), v.strip(), domain=domain)
            else:
                session.SESSION.cookies.set(k.strip(), v.strip())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--cookie", type=str,
                        help="Session cookie string, e.g. 'PHPSESSID=abc123; security=low'")
    parser.add_argument("--email", type=str, help="Login email (fallback form-login)")
    parser.add_argument("--password", type=str, help="Login password (fallback form-login)")
    parser.add_argument("--no-cleanup", action="store_true",
                        help="Skip DB cleanup (for targets without a DB board, e.g. DVWA)")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--xss", action="store_true", help="Enable XSS fuzzing only")
    parser.add_argument("--sqli", action="store_true", help="Enable SQLi fuzzing only")
    args = parser.parse_args()

    # 인증 처리: 쿠키 주입(범용, 권장) 우선, 없으면 폼 로그인(편의) 폴백
    if args.cookie:
        inject_cookies(args.cookie, args.url)
        print("[+] Cookie injected, fuzzing with provided session")
    elif args.email and args.password:
        ok = do_login(args.url, args.email, args.password)
        if ok:
            print("[+] Login OK, fuzzing with authenticated session")
        else:
            print("[!] Login failed, fuzzing unauthenticated only")
    else:
        print("[!] No auth provided, fuzzing unauthenticated only")

    run(args.url, args.depth, debug=args.debug, enable_xss=args.xss,
        enable_sqli=args.sqli, no_cleanup=args.no_cleanup)
