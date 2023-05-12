# import requirements needed
import os

# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session, flash, get_flashed_messages
from utils import get_base_url
import requests
import model

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

#app.config['SESSION_TYPE'] = 'filesystem'


@app.route(f'{base_url}')
def home():
  return render_template('index.html', generated=None)


@app.route(f'{base_url}', methods=['POST'])
def home_post():
  return redirect(url_for('results'))


@app.route(f'{base_url}/results/')
def results():
  if 'data' in session:
    data = session['data']
    return render_template('results.html', generated=data)
  else:
    return render_template('results.html', generated=None)


"""
Finish the two functions below to complete the website's backend.
"""


@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
  prompt = request.form['prompt']
  parameters = {
    'temperature': request.form['temp'],
    'num_return_sequences': 1,
    'top_k': 50,
    'max_new_tokens': request.form['length'],
  }
  generated_text = model.query({
    "inputs": prompt,
    "parameters": parameters,
  })
  session['data'] = generated_text
  print(session['data'])
  session.modified = True
  #return redirect(url_for('results', data=session["data"]))
  return render_template('results.html', generated=session['data'])


# def generate_text():
#   """
#     view function that will return json response for generated text.
#     """

#   prompt = request.form['prompt']
#   if prompt is not None:
#     payload = {
#       "inputs": prompt,
#       "parameters": {
#         'temperature': 1,
#         'num_return_sequences': 1,
#         'top_k': 50,
#         'max_new_tokens': 250,
#       }
#     }

#   generated_text = model.query(payload)
#   if 'error' in generated_text:
#     return render_template('results.html',
#                            generated="Sorry, please enter again")
#   else:
#     data = generated_text
#     return render_template('results.html', generated=data)

if __name__ == '__main__':
  # IMPORTANT: change url to the site where you are editing this file.
  website_url = 'localhost'
  print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
  app.run(host='0.0.0.0', port=port, debug=True)
