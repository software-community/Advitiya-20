from instamojo_wrapper import Instamojo
import os
import requests


def payment_request(name, amount, purpose, email, mobile):
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
        redirect_url="https://advitiya.in/payment_redirect/",
        webhook="https://advitiya.in/webhook/"
    )
    return response

def workshop_payment_request(name, amount, purpose, email, mobile, at_sudhir):
    if at_sudhir:
        api = Instamojo(api_key=os.getenv('WORKSHOP_API_AUTH_KEY'),
                        auth_token=os.getenv('WORKSHOP_API_AUTH_TOKEN'))
    else:
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
        redirect_url="https://advitiya.in/workshop_payment_redirect/",
        webhook="https://advitiya.in/workshop_webhook/"
    )
    return response

def workshop_accomodation_payment_request(name, amount, purpose, email, mobile):
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
        redirect_url="https://advitiya.in/workshop_accomodation_payment_redirect/",
        webhook="https://advitiya.in/workshop_accomodation_webhook/"
    )
    return response