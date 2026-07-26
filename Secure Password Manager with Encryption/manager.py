import database
import crypto_utils

def add_new_credential(website: str, username: str, plain_password: str) -> bool:
    """Validates input, encrypts the password, and writes the record to storage."""
    if not website.strip() or not username.strip() or not plain_password.strip():
        print("\nError: Website, username, and password fields are required.")
        return False

    encrypted_pwd = crypto_utils.encrypt_password(plain_password)
    entry_id = database.insert_credential(website, username, encrypted_pwd)
    print(f"\nSuccess: Credential for '{website}' stored securely under Entry ID {entry_id}.")
    return True

def get_decrypted_credentials() -> list:
    """Fetches all records and decrypts stored passwords."""
    records = database.fetch_all_credentials()
    result = []
    for r in records:
        decrypted_pwd = crypto_utils.decrypt_password(r["encrypted_password"])
        result.append({
            "id": r["id"],
            "website": r["website"],
            "username": r["username"],
            "password": decrypted_pwd,
            "created_at": r["created_at"]
        })
    return result

def search_and_decrypt_credentials(query: str) -> list:
    """Searches credentials by website and decrypts matching passwords."""
    if not query.strip():
        print("\nError: Search query cannot be blank.")
        return []

    records = database.search_credentials_by_website(query.strip())
    result = []
    for r in records:
        decrypted_pwd = crypto_utils.decrypt_password(r["encrypted_password"])
        result.append({
            "id": r["id"],
            "website": r["website"],
            "username": r["username"],
            "password": decrypted_pwd,
            "created_at": r["created_at"]
        })
    return result

def remove_credential(entry_id: int) -> bool:
    """Deletes a credential entry from storage."""
    if database.delete_credential_by_id(entry_id):
        print(f"\nSuccess: Credential Entry ID {entry_id} removed.")
        return True
    else:
        print(f"\nError: Credential Entry ID {entry_id} not found.")
        return False