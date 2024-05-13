import google.cloud.texttospeech as tts
import os
import pygame


credential_path = '/home/rpi4/다운로드/project-tts-371019-b02c45c157dc.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
pygame.mixer.init()

voice_name = 'ko-KR-Wavenet-A'
filename = 'CommandEmpty.wav'


def text_to_wav(voice: str, txt: str):
    language_code = '-'.join(voice.split('-')[:2])
    text_input = tts.SynthesisInput(text=txt)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    with open(filename, 'wb') as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')


textFileName = 'test.txt'

with open(textFileName, 'r', encoding='utf-8') as f:
    text = f.readline()

text_to_wav(voice_name,text)
sound = pygame.mixer.Sound('CommandEmpty.wav')
sound.play()

input()
