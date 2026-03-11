from usecase.linkedin.query.query_check_job import query_check_job

def check_start():
    res = query_check_job()
    data = res.data or []
    print(f"DEBUG - {len(data)} job(s) trouvé(s)")
    return data