from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
import cv2
import matplotlib.pyplot as plt
import torch
from ultralytics import YOLO
from typing import List
import zipfile
import io
import base64

# Configuração do YOLO
torch.serialization.add_safe_globals(["ultralytics.nn.tasks.DetectionModel"])
model = YOLO("yolov8n.pt")

app = FastAPI()

# Configuração para servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuração do Jinja2 para templates HTML
templates = Jinja2Templates(directory="templates")

# Diretórios temporários
IMAGE_DIR = "temp_images"
ANNOTATION_DIR = "temp_annotations"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(ANNOTATION_DIR, exist_ok=True)

# Função para salvar a imagem localmente
def save_uploaded_file(uploaded_file: UploadFile, save_dir: str):
    file_path = os.path.join(save_dir, uploaded_file.filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.file.read())
    return file_path

# Função para detecção e salvamento das anotações
def detect_and_save_annotations(image_path, output_json_path, classes: List[str], confidence_threshold=0.5):
    image = cv2.imread(image_path)
    results = model(image, conf=confidence_threshold)
    image_name = os.path.basename(image_path)
    image_url = image_path  

    result_annotations = []
    for box in results[0].boxes:
        x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        # Verifica se a classe detectada está na lista de classes selecionadas
        if class_name in classes and conf >= confidence_threshold:
            img_height, img_width = image.shape[:2]
            x = (x_min / img_width) * 100
            y = (y_min / img_height) * 100
            width = ((x_max - x_min) / img_width) * 100
            height = ((y_max - y_min) / img_height) * 100

            result_annotations.append({
                "from_name": "label",
                "to_name": "image",
                "type": "rectangle",
                "value": {
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "rotation": 0,
                    "rectanglelabels": [class_name]
                },
                "score": conf
            })

    label_studio_data = {
        "data": {
            "image": image_url
        },
        "annotations": [
            {
                "result": result_annotations
            }
        ]
    }

    if result_annotations:
        with open(output_json_path, 'w') as f:
            json.dump(label_studio_data, f, indent=4)


import json

# Função para exibir imagens anotadas (mostrando apenas as imagens rotuladas)
def generate_labeled_images():
    image_files = sorted(os.listdir(IMAGE_DIR))
    selected_images = image_files[:5] + image_files[-5:] if len(image_files) > 10 else image_files
    image_paths = [os.path.join(IMAGE_DIR, img) for img in selected_images]
    
    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    axes = axes.ravel()
    
    for i, image_path in enumerate(image_paths):
        # Verifica se existe um arquivo .json correspondente
        json_path = os.path.join(ANNOTATION_DIR, f"{os.path.splitext(os.path.basename(image_path))[0]}.json")
        
        if os.path.exists(json_path):
            # Se o arquivo JSON existir, processa a imagem e suas anotações
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Carregar as anotações do arquivo JSON
            with open(json_path, 'r') as f:
                annotations = json.load(f)

            # Anotar a imagem com base no JSON
            for annotation in annotations.get('annotations', []):
                for result in annotation.get('result', []):
                    value = result.get('value', {})
                    if 'rectanglelabels' in value:
                        x = int(value['x'] * image.shape[1] / 100)
                        y = int(value['y'] * image.shape[0] / 100)
                        width = int(value['width'] * image.shape[1] / 100)
                        height = int(value['height'] * image.shape[0] / 100)
                        class_name = value['rectanglelabels'][0]

                        # Desenha o retângulo e o nome da classe na imagem
                        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
                        cv2.putText(image, class_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Exibe a imagem anotada
            axes[i].imshow(image)
            axes[i].axis("off")
        else:
            # Se não tiver anotações (json), apenas não mostra a imagem
            axes[i].axis("off")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    
    return img_base64


# Rota inicial para carregar o formulário
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "", "labeled_image": ""})

# Rota para processar upload das imagens e gerar anotações
@app.post("/upload")
async def upload_images(request: Request, files: List[UploadFile] = File(...), classes: List[str] = Form(...)):
    for uploaded_file in files:
        local_image_path = save_uploaded_file(uploaded_file, IMAGE_DIR)
        output_json_path = os.path.join(ANNOTATION_DIR, f"{os.path.splitext(uploaded_file.filename)[0]}.json")
        detect_and_save_annotations(local_image_path, output_json_path, classes)
    
    labeled_image = generate_labeled_images()
    return templates.TemplateResponse("index.html", {"request": request, "message": "Imagens processadas e rotulagens salvas!", "labeled_image": labeled_image})

# Rota para exportar JSONs separados
@app.get("/export_separate_jsons")
async def export_separate_jsons():
    zip_filename = "annotations_separate.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for annotation_name in os.listdir(ANNOTATION_DIR):
            annotation_path = os.path.join(ANNOTATION_DIR, annotation_name)
            zipf.write(annotation_path, os.path.join("annotations", annotation_name))
    return FileResponse(zip_filename, media_type='application/zip', filename=zip_filename)

# Rota para exportar um único JSON consolidado
@app.get("/export_consolidated_json")
async def export_consolidated_json():
    all_annotations = []
    for json_file in os.listdir(ANNOTATION_DIR):
        with open(os.path.join(ANNOTATION_DIR, json_file), 'r') as f:
            annotation = json.load(f)
            all_annotations.append(annotation)
    output_file = "annotations_ready.json"
    with open(output_file, 'w') as f:
        json.dump(all_annotations, f, indent=4)
    return FileResponse(output_file, media_type='application/json', filename=output_file)

# Rota para limpar cache
@app.get("/clear_cache")
async def clear_cache(request: Request):  # Agora o request é passado como argumento
    for folder in [IMAGE_DIR, ANNOTATION_DIR]:
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))
    
    # Passando o 'request' junto com a mensagem para o template
    return templates.TemplateResponse("index.html", {"request": request, "message": "Cache limpo com sucesso!"})


# Executar o servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
