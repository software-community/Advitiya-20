from instamojo_wrapper import Instamojo
import os
import requests


def payment_request(name, amount, purpose, email, mobile, payment_detail = None):
    api = Instamojo(api_key=os.getenv('API_AUTH_KEY'),
                    auth_token=os.getenv('API_AUTH_TOKEN'))

    # Create a new Payment Request
    if payment_detail:
        response = api.payment_request_status(payment_detail.payment_request_id)
    else:
        response = api.payment_request_create(
            buyer_name=name,
            amount=amount,
            purpose=purpose,
            send_email=True,
            email=email,
            phone=mobile,
            redirect_url="https://advitiya.in/startup_conclave/payment_redirect/",
            webhook="https://advitiya.in/startup_conclave/webhook/"
        )
    return response