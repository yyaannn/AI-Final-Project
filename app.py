from flask import Flask, render_template, request, redirect, url_for,jsonify
import text_generation
import BERT_VADER

app = Flask(__name__)

# message displayed on user interface
messages = []

# prompts used in calling gemini api
prompts = []

# main page
@app.route('/')
def form():
    return render_template('form.html', messages=messages, response1=None, response2=None)

# get user input to do sentiment analysis and text generation
@app.route('/submit', methods=['POST'])
def submit():
    message = request.form['message']
    messages.append(f"You: {message}")
    print(f"input: {message}")
   
    # sentiment analysis
    updated_message, score = BERT_VADER.replace_negative_words(message)
    
    prompts.append(f"Please rewrite the following sentence for precise expression:\n{updated_message}")
    print(f"updated_message: {updated_message}")
    print(f"score: {score}")

    response1 = text_generation.handle_user_input(prompts)
    response2 = text_generation.handle_user_input(prompts)

    # mood
    mood = ""
    if score >= 0.6:
        mood = "Wonderful"
    elif score >= 0.2:
        mood = "Good"
    elif score >= -0.2:
        mood = "Normal"
    elif score >= -0.6:
        mood = "Bad"
    else:
        mood = "Dangerous"

    messages.append(f"Your Mood: {mood}")

    form_html = render_template('form.html', messages=messages,response1=response1, response2=response2)

    return jsonify(form_html=form_html)

# user selects one response
@app.route('/select', methods=['POST'])
def select():
    response = request.form['response']
    messages.append(f"Response: {response}")
    prompts.append(response)
    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(port=5050,debug=True)