import cv2
from doclayout_yolo import YOLOv10



def generate(image):
        
    # Load the pre-trained model
    model = YOLOv10("/Users/a2/.cache/huggingface/hub/models--juliozhao--DocLayout-YOLO-DocStructBench/snapshots/8c3299a30b8ff29a1503c4431b035b93220f7b11/doclayout_yolo_docstructbench_imgsz1024.pt")

    det_res = model.predict(
        image,   # Image to predict
        imgsz=1024,        # Prediction image size
        conf=0.2,          # Confidence threshold
        device="cpu"    # Device to use (e.g., 'cuda:0' or 'cpu')
    )   
    return det_res

if __name__ == "__main__":
    path = '/Users/a2/Desktop/Bildschirmfoto 2024-08-05 um 17.36.03.png'
    print(generate(path))
