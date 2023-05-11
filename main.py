
# import requirements needed
import os

# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url
import requests

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url + 'static')

app.secret_key = os.urandom(64)

app.config['SESSION_TYPE'] = 'filesystem' 

@app.route(f'{base_url}')
def home():
    return render_template('index.html', generated=None)

@app.route(f'{base_url}', methods=['POST'])
def home_post():
    return redirect(url_for('results'))

@app.route(f'{base_url}/results/')
def results():
  print('in result')
  print(session)
  if 'data' in session:
      data = session['data']
      #data ='Hello World'
      return render_template('results.html', generated=data)
  else:
      return render_template('results.html', generated=None)

"""
Finish the two functions below to complete the website's backend.
"""


API_URL = "https://api-inference.huggingface.co/models/ghoshdebapratim1/gpt2-skspr-generators"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


# def query(payload):
#     """
#     Can you write a function that sends a prompt to the Hugging Face endpoint and
#     returns the model's output as a string?
#     """
#     pass

# session['data'] = 'output'
# redirect(url_for('results'))


parameters={
   'temperature' : 1 ,
   'num_return_sequences':1,
   'top_k':50,
   'max_new_tokens':250,
}

@app.route(f'{base_url}/generate_text/', methods=["POST"])




def generate_text(): 
  prompt = request.form['prompt']
  output = query({
	"inputs": prompt,
   "parameters":parameters,
  })
  session['data'] = str(output)
  #session['data'] = {'generated_text': output['generated_text']}

  print(session)
  #print(output[0]['generated_text'])
  session.modified = True
  return redirect(url_for('results'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)