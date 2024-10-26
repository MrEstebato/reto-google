import requests


def sendWhatsappMessage(phone_number, msg):
    url = "https://7103.api.greenapi.com/waInstance7103139720/sendMessage/47c2717fc0ae43ffb030270e66a9220dfc5aa51c96d7412ab5"
    
    payload = {
        "chatId": f"521{phone_number}@c.us", 
    "message": msg, 
    "linkPreview": False
    }
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text.encode('utf8'))


def main():
    for i in range(1,6):
        sendWhatsappMessage('7223892688', f"Esteban la chupa {i}")

if __name__ == "__main__":
    main()