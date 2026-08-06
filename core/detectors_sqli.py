# core/detectors_sqli.py

SQL_ERROR_PATTERNS = [
    "you have an error in your sql syntax",
    "warning: mysqli",
    "warning: mysql_",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sqlstate[",
    "xpath syntax error",
    "supplied argument is not a valid mysql",
    "pdoexception",
]

def detect_error_based_sqli(text: str, baseline_text: str = "") -> bool:
    t = text.lower()
    b = baseline_text.lower()
    for err in SQL_ERROR_PATTERNS:
        if err in t and err not in b:
            return True
    return False

def detect_time_based_sqli(response_time: float,
                           baseline_time: float,
                           threshold: float = 2.5) -> bool:
    return response_time > baseline_time + threshold

def detect_boolean_based_sqli(true_resp_text: str,
                              false_resp_text: str,
                              length_diff_threshold: int = 250) -> bool:
    len_true  = len(true_resp_text)
    len_false = len(false_resp_text)

    if abs(len_true - len_false) > length_diff_threshold:
        return True
    return False
