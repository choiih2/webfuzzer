# core/fuzzer.py
import time
from core.session import fetch
from core.detectors_sqli import (
    detect_error_based_sqli,
    detect_time_based_sqli,
    detect_boolean_based_sqli
)
from core.detectors_xss import detect_xss
from core.utils import get_endpoint_string

def fuzz_injection_point(url, method, data_fields,
                         payloads,
                         base_resp,
                         injection_name, log_vulns,
                         base_url,
                         enable_sqli, enable_xss,
                         debug):

    print("\n────────────────────────────────────────")
    print(f"[PAYLOAD TESTING] Injection: {injection_name}")
    print("────────────────────────────────────────")

    endpoint = get_endpoint_string(url)
    injected_fields = list(data_fields.keys())

    # baseline timing
    baseline_start = time.time()
    base_check_resp, _ = fetch(url, method=method, data=data_fields)
    baseline_time = time.time() - baseline_start

    error_payloads   = payloads.get("error", [])
    boolean_payloads = payloads.get("boolean", [])
    time_payloads    = payloads.get("time", [])
    xss_payloads     = payloads.get("xss", [])

    # 1) ERROR-BASED SQLi
    if enable_sqli:
        for p in error_payloads:
            data = {k: p for k in data_fields}
            resp, _ = fetch(url, method=method, data=data)

            if resp and detect_error_based_sqli(resp.text):
                print(f"⚠ DETECTED SQLi (Error-based) → {p}")
                log_vulns.append([p, "SQLi (Error-based)", resp.status_code, len(resp.text), endpoint, injected_fields])

    # 2) BOOLEAN-BASED SQLi
    if enable_sqli:
        for true_p, false_p in boolean_payloads:
            keys = list(data_fields.keys())
            if not keys: continue

            data_true  = {k: true_p for k in data_fields}
            data_false = {k: false_p for k in data_fields}

            true_resp, _  = fetch(url, method=method, data=data_true)
            false_resp, _ = fetch(url, method=method, data=data_false)

            if true_resp and false_resp:
                if detect_boolean_based_sqli(true_resp.text, false_resp.text):
                    print(f"⚠ DETECTED SQLi (Boolean-based) → {true_p}|{false_p}")
                    log_vulns.append([ true_p, "SQLi (Boolean-based)", true_resp.status_code, len(true_resp.text), endpoint, injected_fields])

    # 3) TIME-BASED SQLi
    if enable_sqli:
        for p in time_payloads:
            data = {k: p for k in data_fields}

            start = time.time()
            resp, _ = fetch(url, method=method, data=data)
            elapsed = time.time() - start

            if resp and detect_time_based_sqli(elapsed, baseline_time):
                print(f"⚠ DETECTED SQLi (Time-based) → {p}")
                log_vulns.append([p, "SQLi (Time-based)", resp.status_code, len(resp.text), endpoint, injected_fields])

    # 4) REFLECTED XSS
    if enable_xss:
        for p in xss_payloads:
            data = {k: p for k in data_fields}
            resp, _ = fetch(url, method=method, data=data)

            if resp:
                xss_type = detect_xss(p, resp)
                if xss_type:
                    print(f"⚠ DETECTED XSS → {p} ({xss_type})")
                    log_vulns.append([p, xss_type, resp.status_code, len(resp.text), endpoint, injected_fields])

    print(f"✓ Done testing injection: {injection_name}")
