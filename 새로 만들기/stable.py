from PIL import Image

import requests
import os
import time
import pygame


def play_sound(command):
    path = f'TTS_SOUND/{command}.wav'
    sound = pygame.mixer.Sound(path)
    sound.play()


def stable():
    print('request를 실행합니다.')

    with open('./transcript.txt', 'r') as reader:
        word_list = [s.strip() for s in reader.readlines()]
    text = ' '.join(word_list)

    if not text or text == '':
        play_sound("CommandEmpty")
        time.sleep(5)
        exit(1)

    print("사용자로부터 입력받은 STT : ", text)
    play_sound("Wait")

    response = requests.get('http://pritras.com:8080/api/stable/diffusion?text=' + text)
    output = response.json()['output']

    # 다운로드 이미지 url
    print('url: ', end='')
    print(output)
    url = output

    # time check
    start = time.time()

    # curl 요청 "이미지 주소" > "저장 될 이미지 파일 이름"
    image_name = 'output'
    dir_path = './stable_image/'
    os.system("curl " + url + " > " + dir_path + image_name + '.jpg')

    resizing_list = [48]

    # 이미지 다운로드 시간 체크
    print('**** 이미지 로딩 시간: {:.3F}초'.format(time.time() - start))
    # 저장 된 이미지 확인
    curl_img = Image.open(dir_path + image_name + '.jpg')

    for word in resizing_list:
        img_resize = curl_img.resize((word, word)).convert(dither=Image.FLOYDSTEINBERG)
        img_resize.save(dir_path + image_name + '-' + str(word) + 'x' + str(word) + '.jpg')
