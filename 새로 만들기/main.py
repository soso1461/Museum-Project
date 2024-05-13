from __future__ import division
from google.cloud import speech
from six.moves import queue
from stable import stable

import re
import sys
import pygame
import time
import pyaudio
import mcpi_module


pygame.mixer.init()

RATE = 16000
CHUNK = RATE // 10
word_list = []  # 사용자가 말한 단어를 저장하는 리스트
is_start = False  # add 명령이 들어오면 그때부터 단어를 입력받음


def play_sound(command):
    path = f'TTS_SOUND/{command}.wav'
    sound = pygame.mixer.Sound(path)
    sound.play()


class MicrophoneStream(object):
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses):
    global is_start
    global word_list

    num_chars_printed = 0

    for response in responses:
        if not response.results:
            continue
        result = response.results[0]

        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()
            num_chars_printed = len(transcript)
        else:
            print(transcript + overwrite_chars)

            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                with open("transcript.txt", "w") as f:
                    for word in word_list:
                        if word == "add":
                            continue
                        else:
                            f.write(word + "\n")
                print("Exiting..")
                print("파일 입력을 종료합니다.")
                stable()
                play_sound("CommandFinish")
                time.sleep(5)
                break
            elif transcript.strip() == "clear":
                play_sound("CommandReset")
                print("모든 리스트를 초기화합니다.")
                is_start = False
                word_list = []
            else:
                # is_start 가 False 라면 add 라고 추가해 줘야함
                if not is_start:
                    if transcript.strip() == "add":
                        is_start = True
                        play_sound("CommandInputStart")
                        print("add 모드로 시작합니다.")
                        word_list.append("add")
                # start mode 이므로 단어 삽입
                else:
                    if transcript.strip() == "delete":
                        word_list.pop()
                        play_sound("CommandCancel")
                        print("delete 실행 !!")
                    else:
                        play_sound("CommandInput")
                        word_list.append(transcript.strip())
            print("#### word_list_start ####")

            for word in word_list:
                print(word)

            print("#### word_list_end ####")

            num_chars_printed = 0


def main():
    language_code = "en-US"

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        use_enhanced=True,
        model='phone_call'
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)
        listen_print_loop(responses)


if __name__ == '__main__':
    main()
