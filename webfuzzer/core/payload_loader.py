# core/payload_loader.py
from core.config import DIR_WORDLIST, SQLI_ERROR_FILE, SQLI_BOOLEAN_TRUE_FILE, SQLI_BOOLEAN_FALSE_FILE, SQLI_TIME_FILE, XSS_PAYLOADS
import os

def load_list(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [x.strip() for x in f if x.strip()]

def load_boolean_pairs(true_file, false_file):
    true_list  = load_list(true_file)
    false_list = load_list(false_file)

    if len(true_list) != len(false_list):
        print("[!] Boolean payload line count mismatch!")
        print(f"  true:  {len(true_list)} lines")
        print(f"  false: {len(false_list)} lines")

    pairs = list(zip(true_list, false_list))

    print(f"[+] Loaded {len(pairs)} boolean-based SQLi pairs")
    return pairs

def load_default_sqli_payloads():
    return {
        "error": load_list(SQLI_ERROR_FILE) if os.path.exists(SQLI_ERROR_FILE) else [],
        "boolean": load_boolean_pairs(SQLI_BOOLEAN_TRUE_FILE, SQLI_BOOLEAN_FALSE_FILE),
        "time": load_list(SQLI_TIME_FILE) if os.path.exists(SQLI_TIME_FILE) else []
    }

def load_default_xss_payloads():
    return {"xss": load_list(XSS_PAYLOADS) if os.path.exists(XSS_PAYLOADS) else []}
