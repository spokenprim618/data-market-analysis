def log_event(logs, row_id, method, status, confidence):
    logs.append({
        "row_id": row_id,
        "method": method,        # regex / nlp
        "status": status,        # success / fallback / failure
        "confidence": confidence
    })