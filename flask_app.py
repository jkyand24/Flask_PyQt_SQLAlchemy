import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request
from imagenet1000_lables_temp import lable_dict
from vgg11 import VGG11

# image 전처리하는 함수 정의

def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    output_image = transform(image).unsqueeze(0)
    
    return output_image

# model load하는 함수 정의

def load_model(model_path):
    model = VGG11(num_classes=1000)
    model.load_state_dict(torch.load(model_path))
        # 모델 전체가 아니라 state_dict를 불러오는 경우 - load 이후 load_state_dict 해줘야 함
    model.eval()
    
    return model

# model 준비

model_path = "./data/vgg11-bbd30ac9.pth"

model = load_model(model_path)

#

app = Flask(__name__) 
    # 플라스크 객체 생성. __name__: 현재 실행중인 모듈 이름

@app.route("/predict", methods=['POST']) 
    # 데코레이터는 기존 함수를 수정하지 않으면서 추가 기능을 구현
    # 주소 뒤에 "/predict" 입력 -> predict() 실행됨, 결과가 웹상에 표현됨  

def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
            # jsonify(): GET 요청이 오면, 미리 만들어둔 딕셔너리를 json으로 변경시켜서 보내기
    
    image = request.files['image']
    
    img = Image.open(image)
    
    img = preprocess_image(img)
    
    with torch.no_grad():
        outputs = model(img)
        
        _, pred = torch.max(outputs.data, 1)
        
        labels = int(pred.item())
        
        classes = lable_dict[labels]
        
        predictions = str(classes)
        
    return jsonify({'predictions': predictions}), 200

if __name__ == '__main__':
    app.run(debug=True)
    """
        host: flask를 동작시키면서 모니터링할 IP
        port: 위 IP에서 접속할 포트 번호
        debug: 에러 발생시 python cmd 창에서 확인 가능
    """