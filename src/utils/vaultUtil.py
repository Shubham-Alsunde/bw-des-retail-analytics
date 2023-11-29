import requests

VAULT_URL = "http://127.0.0.1:8200"
ROLE_ID = "bc3426dc-dd40-b227-8d82-730b26a360f6"
SECRET_ID = "10a5826e-6dc1-3c32-5b05-2847fc7513df"
SECRET_PATH = "secret/data/snow"


def authenticate_with_approle():
    auth_url = f"{VAULT_URL}/v1/auth/approle/login"
    auth_data = {
        "role_id": ROLE_ID,
        "secret_id": SECRET_ID
    }

    try:
        auth_response = requests.post(auth_url, json=auth_data)
        auth_response.raise_for_status()

        token = auth_response.json()["auth"]["client_token"]
        print("token=======", token)
        return token

    except requests.exceptions.RequestException as e:
        print(f"Authentication error: {e}")
        return None


def get_secret(token):
    headers = {
        "X-Vault-Token": token,
    }

    url = f"{VAULT_URL}/v1/{SECRET_PATH}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        secret_data = response.json()["data"]
        return secret_data

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving secret: {e}")
        return None


token = authenticate_with_approle()
secret_data = get_secret(token)

print(secret_data)
