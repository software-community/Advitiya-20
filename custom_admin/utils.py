import requests
import os
from firebase_admin import credentials

try:
    cred = credentials.Certificate("service-account.json")
    access_token_info = cred.get_access_token().access_token
except:
    access_token_info = ''

def sendNotification(title, message):
    headers = {'Content-type': 'application/json',
               'Authorization': 'Bearer ' + access_token_info}
    postdata = {
        "message": {
            "condition": "!('anytopicyoudontwanttouse' in topics)",
            "notification": {
                "title": title,
                "body": message
            },
            "data":
            {
                "click_action": "FLUTTER_NOTIFICATION_CLICK"
            },
            "webpush": {
                "fcm_options": {
                    "link": "https://play.google.com/store/apps/details?id=com.softcom.advitiya"
                }
            }
        }
    }
    r = requests.post('https://fcm.googleapis.com//v1/projects/advitiya2020-719da/messages:send',
                      json=postdata, headers=headers)


from instamojo_wrapper import Instamojo
def check_payment(request_id, at_sudhir):
    if at_sudhir:
        api = Instamojo(api_key=os.getenv('WORKSHOP_API_AUTH_KEY'),
                        auth_token=os.getenv('WORKSHOP_API_AUTH_TOKEN'))
    else:
        api = Instamojo(api_key=os.getenv('API_AUTH_KEY'),
                    auth_token=os.getenv('API_AUTH_TOKEN'))

    # Create a new Payment Request
    response = api.payment_request_status(request_id)
    if response['success'] and response['payment_request']['status'] == 'Completed':
        for payment in response['payment_request']['payments']:
            if payment['status'] == 'Credit':
                return payment['payment_id']
    return None