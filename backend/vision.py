import requests
import os

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': os.environ["VISIONAPI"],
}

params = {
    'visualFeatures': 'Categories',
    'details': 'Celebrities',
    'language': 'en',
}


body = {'url':'https://imgcdn1.gaadi.com/images/carexteriorimages/910x378/Maruti/Maruti-Swift-Dzire/047.jpg'
}

try:
    response = requests.post(url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze',
                             headers = headers,
                             params = params,
                             json = body)
    data = response.json()
    print(data)
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
