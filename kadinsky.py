import json, time, base64, requests
from config import FB_KEY, FB_SECRET


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        # style = "ANIME"
        # styles= ["UHD","DEFAULT","ANIME","KANDINSKIY","UHD","DEFAULT","UHD","DEFAULT"]
        style = "DEFAULT"
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "style": style,
            "censored": False,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=20, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            attempts -= 1
            time.sleep(delay)



async def create_image(prompt,chat_id):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', FB_KEY, FB_SECRET)
    model_id = api.get_model()
    # Генерируем 5 изображений на основе одного промпта
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)
    # Сохраняем каждое изображение в отдельный файл
    try:
        image_base64 = images[0]
        image_data = base64.b64decode(image_base64)
        photo_path = f"{chat_id}.jpg"
        with open(photo_path, "wb") as file:
            file.write(image_data)
        print("Done!")
        return photo_path
    except:
        pass
