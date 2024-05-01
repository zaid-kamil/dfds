import requests
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/dima806/deepfake_vs_real_image_detection"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    img = Image.open(filename)
    # resize image to (200, 200)
    img = img.resize((200, 200))
    format = img.format or 'png'
    # temp save in static/temp.jpg
    img.save(f"static/temp.{format}")
    # open temp.jpg in binary mode
    with open(f"static/temp.{format}", "rb") as file:
        data = file.read()
    response = requests.post(API_URL, headers=headers, data=data)
    ans = response.json()
    print(ans)
    return ans
if __name__ == "__main__":
    print(query("static/uploads/zaid-kamil-headshot.jpg"))
    # print(query("static/uploads/fake.jpg"))