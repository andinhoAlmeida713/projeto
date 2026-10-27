import hashlib

def cria_hash_senha(senha: str) -> str:
    """Recebe uma senha em texto puro e retorna o hash SHA-256 dela."""
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()
