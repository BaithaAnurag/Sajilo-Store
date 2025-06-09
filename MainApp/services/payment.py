# payments/services/payment.py
import requests

def verify_khalti_payment(token, amount, secret_key):
    url = "https://khalti.com/api/v2/payment/verify/"
    headers = {
        "Authorization": f"Key {secret_key}"
    }
    payload = {
        "token": token,
        "amount": amount,
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.status_code, response.json()