
# use Resnet-18 pretrained model for image classification - download from pytorch hub
# create a python virtual env (python -m venv <virtual_env_name>)  and activate it before pip installing (this isolates this project/installs for all otherpython projects on the machine).
# The <virtual_env_name> should not start with . if I need to use the same in VS code.
# pip uninstall torch torchvision torchaudio -y && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
# pip install requests gradio

import torch
import gradio as gr
model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet18', pretrained=True).eval()




# predict function -  function that takes in the user input, which in this case is an image, 
# and returns the prediction (dictionary whose keys are class name and values are confidence probabilities)
import torch
import requests
from torchvision import transforms

# Download human-readable labels for ImageNet
response = requests.get("https://git.io/JJkYN")
labels = [l.strip() for l in response.text.split("\n") if l.strip()]
# Define image preprocessing (IMPORTANT for ResNet)
transform = transforms.Compose([
    transforms.ToTensor(),
     transforms.Normalize(
         [0.485, 0.456, 0.406],
         [0.229, 0.224, 0.225]
     )
 ])

def predict(inp):
    # preprocess image
    inp = transform(inp).unsqueeze(0)
    # ensure model runs in inference mode
    with torch.no_grad():
        prediction = torch.nn.functional.softmax(model(inp)[0], dim=0)
    # map predictions to labels
    confidences = {
        labels[i]: float(prediction[i]) 
        for i in range(len(labels))
    }
    return confidences


gr.Interface(fn=predict,
       inputs=gr.Image(type="pil"),
       outputs=gr.Label(num_top_classes=3),
       examples=["/images/adults_and_juvenile.jpg", "/images/cheetah.jpg"]).launch()

# to run the app - python image_classifier.py and browse to website - http://127.0.0.1:7860/
# it identified perguin, cheetah. For Kim Kardashin it identified doormat (3%), centipede (3%), ant (3%) :)