# Chinese Learning Chatbot

Chinese Learning Chatbot is a Flask web app that helps Chinese language students practice conversation, review lesson vocabulary, translate chatbot responses, check vocabulary and grammar errors, and hear Chinese text spoken aloud.

The app uses OpenAI for chat responses and text-to-speech audio. It uses `ICText1.csv` as the lesson vocabulary source, then builds each chat prompt around the vocabulary for the selected lesson.

## Project Structure

```text
ChineseChatbot/
├── server.py
├── requirements.txt
├── ICText1.csv
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── translate.html
│   ├── vocabulary.html
│   ├── grammar.html
│   ├── character_info.html
│   └── process_audio.html
└── static/
    └── css/
        ├── style.css
        └── images/
            └── plainbackground.jpg
```

## What The App Does

The main experience is a Chinese practice chatbot. A student enters a lesson number, and the backend loads the vocabulary for that lesson from `ICText1.csv`. The app asks OpenAI to generate a Chinese conversation prompt using that lesson's vocabulary. The user can then respond in Chinese, and the chatbot continues the conversation while staying focused on the same lesson vocabulary.

The app also generates speech audio for chatbot output and character pages using OpenAI text-to-speech. The generated audio is saved as `output.mp3` and served through the `/audio` route.

## Pages And Routes

### Home Page

Route: `/`

Template: `templates/index.html`

The landing page displays the project title, a short welcome message, and a form where the student enters a lesson number. Submitting the form sends a `POST` request to `/get_response`.

### Chat Response Page

Route: `/get_response`

Template: `templates/result.html`

This route handles the main chatbot flow.

- Reads the selected `lesson_number` from the form.
- Loads `ICText1.csv` with pandas.
- Filters the vocabulary list to the selected lesson.
- Builds an HTML table of clickable vocabulary words.
- If this is the first round, asks OpenAI to start a conversation.
- If the user submitted a response, asks OpenAI to reply in Chinese and ask a follow-up question.
- Generates text-to-speech audio for the chatbot output.
- Displays the chatbot response, audio player, reply form, and vocabulary table.

The vocabulary table links each character or word to its own character information page.

### Audio Route

Route: `/audio`

This route serves the latest generated `output.mp3` file as browser-playable audio.

### Translation Page

Route: `/translate/<output>`

Template: `templates/translate.html`

This page sends the chatbot output to OpenAI and asks for an English translation. It displays the original Chinese text and the generated translation.

### Vocabulary Error Page

Route: `/vocabulary_errors/<user_input>`

Template: `templates/vocabulary.html`

This page sends the user's Chinese sentence to OpenAI and asks it to identify vocabulary errors. If no clear vocabulary errors are found, the response should report that the sentence is correct.

### Grammar Error Page

Route: `/grammar_errors/<user_input>`

Template: `templates/grammar.html`

This page sends the user's Chinese sentence to OpenAI and asks it to identify grammar errors. If no clear grammar errors are found, the response should report that the sentence is correct.

### Character Information Page

Route: `/character/<character>`

Template: `templates/character_info.html`

This page provides more detail about a selected vocabulary word or character. The backend asks OpenAI for:

- the English meaning
- the pinyin
- a concise explanation of grammatical use

It also generates audio for the selected word or character.

### Audio Recording Page

Template: `templates/process_audio.html`

This file contains browser-side microphone recording code. The matching Flask route is currently commented out in `server.py`, so this page is not active in the current app.

## Backend Logic

The backend lives in `server.py`.

Important functions:

- `call_to_GPT(messages, message, model_type="gpt-3.5-turbo")`: adds the user message to a chat history and sends it to OpenAI's chat completions API.
- `call_to_TTS(text)`: sends text to OpenAI text-to-speech and writes the result to `output.mp3`.
- `get_response()`: controls the main chat workflow, vocabulary filtering, OpenAI prompt construction, audio generation, and result rendering.
- `translate_response(output)`: asks OpenAI to translate chatbot output into English.
- `vocabulary_errors(user_input)`: asks OpenAI to review vocabulary usage.
- `grammar_errors(user_input)`: asks OpenAI to review grammar.
- `character_page(character)`: asks OpenAI for character or word details and generates pronunciation audio.


## Requirements

You need Python 3 and an OpenAI API key.

The app depends on the packages in `requirements.txt`. The code also imports `pandas` and `flask_sqlalchemy`, so install them if they are not already in your environment.

## How To Run

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
pip install pandas flask_sqlalchemy
```

3. Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

4. Start the Flask server:

```bash
python server.py
```

5. Open the app in your browser:

```text
http://127.0.0.1:5000
```

## Notes

- `ICText1.csv` must stay in the project root because `server.py` reads it with the relative path `ICText1.csv`.
- `output.mp3` is generated each time the app creates new speech audio.
- The app runs in Flask debug mode when started with `python server.py`.
- OpenAI API usage may incur costs depending on your OpenAI account and usage.
