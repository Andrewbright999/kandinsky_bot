import json
import requests
import asyncio
import logging
import base64

from urllib3.exceptions import ProtocolError
from http.client import RemoteDisconnected
from config import FB_KEY, FB_SECRET, SECOND_FB_KEY, SECOND_FB_SECRET
from typing import List


ACCOUNTS = [
    {"api_key": FB_KEY, "secret_key": FB_SECRET},
    {"api_key": SECOND_FB_KEY, "secret_key": SECOND_FB_SECRET}
]

FUSIONBRAIN_URL = 'https://api-key.fusionbrain.ai/'


class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    async def get_model(self):
        try:
            response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
            data = response.json()
            return data[0]['id']
        except (RemoteDisconnected, ProtocolError):
            logging.error("Ошибка подключения. Повторный запрос...")
            return await self.get_model()

    async def generate(self, prompt, model, images=1, width=1024, height=1024):
        style = "UHD"
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "style": style,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        try:
            response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
            data = response.json()
            return data['uuid']
        except (RemoteDisconnected, ProtocolError):
            logging.error("Ошибка подключения. Повторный запрос...")
            return await self.generate(prompt, model, images, width, height)

    async def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            try:
                response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
                data = response.json()
                if data['status'] == 'DONE':
                    return data['images']
            except (RemoteDisconnected, ProtocolError):
                logging.error("Ошибка подключения. Повторный запрос...")

            attempts -= 1
            await asyncio.sleep(delay)

async def generate_image(prompt, account_index):
    api_data = ACCOUNTS[account_index]
    api = Text2ImageAPI(FUSIONBRAIN_URL, api_data['api_key'], api_data['secret_key'])

    model_id = await api.get_model()
    uuid = await api.generate(prompt, model_id)
    images = await api.check_generation(uuid)

    # Преобразуем изображение из base64 в байты
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)

    return image_data