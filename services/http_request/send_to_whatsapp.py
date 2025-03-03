import os
import requests

BASE_URL = os.environ.get('BASE_URL')
API_VERSION = os.environ.get('API_VERSION')
BUSINESS_PHONE = os.environ.get('BUSINESS_PHONE')
API_TOKEN = os.environ.get('API_TOKEN')

def send_to_whatsapp(data):
    base_url = f"{BASE_URL}/{API_VERSION}/{BUSINESS_PHONE}/messages"
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }

    try:
        response = requests.post(base_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(error)
        raise RuntimeError(f"Failed to send message: {error}")