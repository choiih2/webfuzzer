# core/detectors_sqli.py
SQL_ERROR_PATTERNS = [
    "sqlstate", "syntax error", "mysql", "pdoexception",
    "unterminated", "unclosed", "odbc", "mariadb", "column count",
    "warning: mysql", "you have an error in your sql syntax",
]

def detect_error_based_sqli(text: str) -> bool:
    t = text.lower()
    for err in SQL_ERROR_PATTERNS:
        if err in t:
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
