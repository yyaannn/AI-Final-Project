from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import text_generation

app = Flask(__name__)
CORS(app)
# message displayed on user interface
messages = []

# prompts used in calling gemini api
prompts = []

# main page
# @app.route('/')
# def form():
#     return render_template('index.html', messages=messages, response1=None, response2=None)

# get user input to do sentiment analysis and text generation
@app.route('/submit', methods=['POST'])
def submit():
    message = request.form
    print("\n\n msg: ",message)
    return {"message":message}
    messages.append(f"You: {message}")

    ''' sentiment analysis here '''
    
    prompts.append(f"Please rewrite the following sentence for precise expression:\n{message}")
    response1 = text_generation.handle_user_input(prompts)
    response2 = text_generation.handle_user_input(prompts)
    messages.append("Your Mood:\nWonderful/Normal/Dangerous...")
    return {'messages':messages, 'response': [response1,response2]}
    # return render_template('index.html', messages=messages, response1=response1, response2=response2)

# user selects one response
@app.route('/select', methods=['POST'])
def select():
    response = request.form['response']
    messages.append(f"Response: {response}")
    prompts.append(response)
    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(debug=True)
