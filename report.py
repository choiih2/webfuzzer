# core/report.py
def generate_report(target, logs, endpoints, duration, total_requests):
    lines = []
    lines.append("********************************************************")
    lines.append("*                    FUZZER REPORT                     *")
    lines.append("********************************************************\n")
    lines.append(f"Target: {target}")
    lines.append(f"Total requests: {total_requests}")
    lines.append("\nDiscovered Endpoints:")
    lines.append("------------------------------------------------------------")
    for ep in endpoints:
        lines.append(ep)
    lines.append("------------------------------------------------------------\n")
    lines.append("Found issues:")
    lines.append("==========================================================================================================================")
    lines.append("ID     Status   Length   Endpoint                       Fields              Type                    Payload")
    lines.append("==========================================================================================================================")

    for idx, (payload, vtype, status, resp_len, endpoint, injected_fields) in enumerate(logs, start=1):
        fields_str = ",".join(injected_fields) if isinstance(injected_fields, list) else str(injected_fields)
        lines.append(
            f"{idx:05d}  "
            f"{status:<7}  "
            f"{resp_len:<7}  "
            f"{endpoint:<30}  "
            f"{fields_str:<18}  "
            f"{vtype:<22}  "
            f"{payload}"
        )

    lines.append("==========================================================================================================================\n")
    lines.append(f"Total time: {duration:.4f}s")
    lines.append(f"Processed Requests: {total_requests}")
    lines.append(f"Issues Found: {len(logs)}")
    lines.append(f"Requests/sec: {total_requests / duration:.1f}" if duration > 0 else "Requests/sec: N/A")

    return "\n".join(lines)
