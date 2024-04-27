import requests

API_URL = "https://api-inference.huggingface.co/models/dima806/deepfake_vs_real_image_detection"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("static/fake_1006.jpg")
print(output)