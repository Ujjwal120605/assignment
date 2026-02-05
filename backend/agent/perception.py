def is_login_screen(page_source: str):
    if not page_source:
        return False
    src = page_source.lower()
    return "password" in src and ("email" in src or "username" in src)
