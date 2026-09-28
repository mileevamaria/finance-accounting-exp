from pwdlib import PasswordHash

hash_tool = PasswordHash.recommended()

# password hashing
def hash_password(password: str) -> str:
    return hash_tool.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_tool.verify(password, hashed_password)


# token hashing
def hash_refresh_token(token: str) -> str:
    return hash_tool.hash(token)


def verify_refresh_token(token: str, token_hash: str) -> bool:
    return hash_tool.verify(token, token_hash)
