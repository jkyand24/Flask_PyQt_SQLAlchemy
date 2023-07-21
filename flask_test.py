import requests

model_api_url = "http://127.0.0.1:5000/predict"

image_path = "./data/cat.jpg"

with open(image_path, 'rb') as f: # r: 읽기용으로 열기, b: 이진 모드로 열기
    files = {'image': f}
    
    requests = requests.post(model_api_url, files=files)
    
if requests.status_code == 200:
    try:
        predictions = requests.json()['predictions']
        
        print("\n예측 결과:\n", predictions)
        
    except Exception as e:
        print("API 오류", str(e))
        
else:
    print("API 오류", requests.text)