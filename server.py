from flask import Flask, render_template, request, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
my_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = my_key
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def call_to_GPT(messages, message, model_type="gpt-3.5-turbo"):
  messages.append({"role":"user","content": message})
  client = OpenAI()
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
  )
  return response.choices[0].message.content




@app.route('/audio')
def serve_audio():
    return send_file('output.mp3', as_attachment=False, mimetype='audio/mpeg')

def call_to_TTS(text):
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice= "alloy",
        input=text
    )
    response.stream_to_file("output.mp3")
    

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        lesson_number = request.form['lesson_number']
    except:
        lesson_number = "1"
    try:
        user_input = request.form['user_input']
        first_round= False
    except:
        first_round= True
        user_input=""

    
    vocabulary = pd.read_csv('ICText1.csv')
    vocab = pd.DataFrame(data={"Character":list(vocabulary.iloc[:,0]), "Lesson":list(vocabulary.iloc[:,1])})
    vocab['Lesson'] = vocab['Lesson'].astype(str)
    lesson = vocab.loc[vocab['Lesson']==lesson_number,'Character'].tolist()

    html_content = "<table>"
    html_content += "<tr>"
    count = 0
    for character in lesson:
        if count<7:
            html_content += f"<td><a href='/character/{character}'>{character}</a></td>"
        else:
            count = 0
            html_content += f"</tr><tr><td><a href='/character/{character}'>{character}</a></td>"
        count+=1

    html_content += "</tr></table>"  
    messages = [
        {"role":"system","content":"You are an instructor chatbot that responds to students using given vocabulary."},
        {"role":"system","content": f"""The following vocabulary list consists of Chinese level {lesson_number} vocabulary: {str(lesson)}"""},
        ]


    if first_round==False:
        message = f"""Consider the following text: {user_input}
        Use the Chinese level {lesson_number} vocabulary to respond directly to the message and ask a follow-up question that relates to the user's message in Chinese."""
        output = call_to_GPT(messages, message)
        
    else:
        message = f"""Use the Chinese level {lesson_number} vocabulary to pose an interesting question to the user that will iniate a back and forth conversation."""
        output= call_to_GPT(messages, message)
    call_to_TTS(output)
        
    return render_template('result.html', table=html_content, user_input=user_input, output=output, lesson_number=lesson_number, first_round=first_round)


@app.route('/translate/<output>')
def translate_response(output):
    messages = [
        {"role":"system","content":"You are an instructor chatbot that teaches the meanings and usages of Chinese words."}
    ]
    message = f""""Translate the following phrase into English and output just the English translation: {output}"""
    description= call_to_GPT(messages, message)
    #description = "Hello!"
    return render_template('translate.html', output=output, description=description)

@app.route('/vocabulary_errors/<user_input>')
def vocabulary_errors(user_input):
    messages = [
        {"role":"system","content":"You are an instructor chatbot that teaches the meanings and usages of Chinese words."}
    ]
    message = f""""Identitfy the vocabulary errors in the following Chinese sentence: {user_input}. If there are no identitfiable errors, report that the sentence is correct."""
    description= call_to_GPT(messages, message)
    #description = "This sentence has no vocabulary errors!"
    return render_template('vocabulary.html', user_input=user_input, description=description)


@app.route('/grammar_errors/<user_input>')
def grammar_errors(user_input):
    messages = [
        {"role":"system","content":"You are an instructor chatbot that teaches the meanings and usages of Chinese words."}
    ]
    message = f""""Identitfy the grammatical errors in the following Chinese sentence: {user_input}. If there are no identitfiable errors, report that the sentence is correct."""
    description= call_to_GPT(messages, message)
    #description = "This sentence has no grammar errors!"
    return render_template('grammar.html', user_input=user_input, description=description)
   




@app.route('/character/<character>')
def character_page(character):
    # Here you can render a specific template or do any other necessary processing
    messages = [
        {"role":"system","content":"You are an instructor chatbot that teaches the meanings and usages of Chinese words."}
    ]
    message = f""""Output the English meaning of the Chinese word {character}, print the pinyin of the word, and consicely explain its grammatical use in the Chinese language."""
    description= call_to_GPT(messages, message)
    call_to_TTS(character)
    return render_template('character_info.html', character=character, description=description)


# @app.route('/process_audio', methods=['POST'])
# def process_audio():
#     # Get the uploaded audio file
#     if 'audio' not in request.files:
#         return jsonify({'error': 'No audio file uploaded'}), 400

#     audio_file = request.files['audio']

#     # Save the audio file temporarily
#     temp_filename = 'uploaded_audio.webm'
#     audio_file.save(temp_filename)

#     # Send the audio file to OpenAI for transcription
#     with open(temp_filename, 'rb') as f:
#         transcription_response = OpenAI.Audio.transcribe(
#             file=f,
#             model='whisper-1'
#         )

#     # Clean up the temporary file
#     os.remove(temp_filename)

#     # Return the transcription result as JSON
#     return transcription_response['text']







if __name__ == '__main__':
    app.run(debug=True)




