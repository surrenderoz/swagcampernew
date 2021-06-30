
from pyfcm import FCMNotification


push_service = FCMNotification(api_key="AAAAqLQ7_AY:APA91bEPWSfiiETtyhtTdjcj_--hgCl3UEdbWX-CTmynXLemu7u0TXVBRt4eKX8D3tjLFOBJ8rejGxgy8hUiyTnpEcT5J5n0rLcyvpbZWEhFjaqESFLDAZzUXNnHrApS1oqq_jya1XNH")

# OR initialize with proxies

proxy_dict = {
          "http"  : "http://127.0.0.1",
          "https" : "http://127.0.0.1",
        }
push_service = FCMNotification(api_key="AAAAqLQ7_AY:APA91bEPWSfiiETtyhtTdjcj_--hgCl3UEdbWX-CTmynXLemu7u0TXVBRt4eKX8D3tjLFOBJ8rejGxgy8hUiyTnpEcT5J5n0rLcyvpbZWEhFjaqESFLDAZzUXNnHrApS1oqq_jya1XNH", proxy_dict=proxy_dict)

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

registration_id = "dgQykCv0YkfNqkoP3NQPbA:APA91bF7-qH0YxXbqqScRsqJwotJjVNId4XeNlweDVY4qTRJlXvX9xMlk2mCkx0qg0bTpp4krGlLmoEmRN7pVe_KqD4A7iqEc6kXm6vrt-ttA-JmBR5VF1G9NBbk3enoy5tjTJ0Qre-1"
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

print(result)
 
# Send to multiple devices by passing a list of ids.
# registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
# message_title = "Uber update"
# message_body = "Hope you're having fun this weekend, don't forget to check today's news"
# result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

# print result
