# core/injector.py
def build_injection_points(url, html_forms):
    injection_targets = []
    seen = set()

    for form in html_forms:
        inputs = form["inputs"]
        key = (form["url"], form["method"], tuple(inputs))
        if key in seen:
            continue
        seen.add(key)

        data = {inp: "FUZZ" for inp in form["inputs"]}
        injection_targets.append((
            "form-" + form["method"],
            form["url"],
            form["method"],
            data
        ))

    return injection_targets
