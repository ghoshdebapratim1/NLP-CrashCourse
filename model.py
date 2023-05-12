# import requests

# API_URL = "https://api-inference.huggingface.co/models/ghoshdebapratim1/gpt2-skspr-generators"
# headers = {"Authorization": "Bearer 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"}

# def query(payload):
#   response = requests.post(API_URL, headers=headers, json=payload)
#   try:
#     response.raise_for_status()
#   except requests.exceptions.HTTPError:
#     return "Error:" + "".join(response.json()['error'])
#   else:
#     return response.json()[0]['generated_text']

import requests

API_URL = "https://api-inference.huggingface.co/models/ghoshdebapratim1/gpt2-skspr-generators"
headers = {"Authorization": "Bearer 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"}


def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  if 'error' in response.json():
    return response.json()['error']
  else:
    return response.json()[0]['generated_text']
