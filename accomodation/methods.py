from instamojo_wrapper import Instamojo
import os
import requests

def accommodation_payment_request(name, amount, purpose, email, mobile):
    api = Instamojo(api_key=os.getenv('API_AUTH_KEY'),
                auth_token=os.getenv('API_AUTH_TOKEN'))

    # Create a new Payment Request
    response = api.payment_request_create(
        buyer_name=name,
        amount=amount,
        purpose=purpose,
        send_email=True,
        email=email,
        phone=mobile,
        redirect_url="https://advitiya.in/accommodation/accommodation_payment_redirect/",
        webhook="https://advitiya.in/accommodation/accommodation_webhook/"
    )
    return response