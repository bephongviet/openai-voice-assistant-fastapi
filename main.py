import google.cloud.texttospeech as tts
from google.oauth2 import service_account
from fastapi import FastAPI, File, UploadFile
import openai
import aiofiles
import soundfile as sf
from fastapi.responses import FileResponse

app = FastAPI()
openai.api_key = 'sk-p...s5e'
credentials = service_account.Credentials.from_service_account_file('iron-ripple-...json')

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/assist/")
async def assist(voice: UploadFile):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Keep your answer short to 2-3 sentences max."},
    ]

    # save file voice to disk
    user_voice_file = 'user_voice.m4a'
    async with aiofiles.open(user_voice_file, 'wb') as out_file:
        content = await voice.read()  # async read
        await out_file.write(content)  # async write
    audio_file = open(user_voice_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    # send user transcript to gpt to get a response from AI
    messages.append({"role": "user", "content": transcript["text"]})
    print(messages)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # convert ai response text to voice
    # get response from chatgpt and append to our message again
    assistant_text = response['choices'][0]['message']['content']
    aivoice_file = text_to_voice("en-US-Neural2-F", assistant_text)

    #return {"transcript": transcript}
    return FileResponse(aivoice_file)

def text_to_voice(voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient(credentials=credentials)
    gg_response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    filename = "ai_voice.wav"
    with open(filename, "wb") as out:
        out.write(gg_response.audio_content)
        # Extract data and sampling rate from file
        data, fs = sf.read(filename, dtype='float32')

    return filename

