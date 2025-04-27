import requests
from django.conf import settings

def verify_paystack_payment(reference):
    """
    Verifies a transaction using Paystack's API.

    Args:
        reference (str): The transaction reference to verify.

    Returns:
        dict: A dictionary with the verification status and transaction data.
    """
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    try:
        # Send request to Paystack
        response = requests.get(url, headers=headers)
        response_data = response.json()

        # Check if the request was successful
        if not response_data.get("status"):
            return {"status": False, "message": "Transaction verification failed."}

        # Extract transaction data from the response
        paystack_data = response_data.get("data")
        if not paystack_data:
            return {"status": False, "message": "Invalid transaction data received."}

        return {
            "status": True,
            "data": paystack_data,
            "message": "Transaction verified successfully.",
        }

    except requests.RequestException as e:
        # Handle network errors or API issues
        return {"status": False, "message": f"An error occurred: {str(e)}"}
