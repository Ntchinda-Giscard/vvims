from paddleocr import PaddleOCR, draw_ocr
import spacy
from ultralytics import YOLO
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

ocr_model = PaddleOCR(lang='en')
nlp_ner = spacy.load("output/model-best")
detector = YOLO('best.pt')


def licence_dect(img: any) -> list:
    image = Image.open(img)
    # image = np.array(image)
    results = detector(img)
    detections = []
    boxes = results[0].numpy() 
    print(boxes)
    for result in results:
        x1, y1, x2, y2, confidence, _ = result[0].numpy()

        confidence = float(confidence)
        print("Confidence :", confidence)
        print("Confidence :", confidence)

        cropped_image = image.crop((x1, y1, x2, y2))

        plt.imshow(cropped_image)
        plt.show()

        detections.append(result)
    
    return detections

res = licence_dect("IMG_0551.JPG" )
print(res)
def ner_recog(text:str) -> dict:
    """
    Extract entities from text using SpaCy and return them as JSON.

    Args:
    - text: The input text.

    Returns:
    - dict: A dictionary containing the extracted entities in JSON format.
    """
    # Load SpaCy model
    # Process the text
    doc = nlp_ner(text)

    # Extract entities and format them as JSON
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    return {"entities": entities}





def read_text_img(img_path:str) -> str:
    """
        Read text from images

        Args:
        - img_path: Path to the images in which the text will be extracted

        Returns:
        - text: The extracted text
    """

    result = ocr_model.ocr(img_path)

    text = ''
    for res in result[0]:
        text += res[1][0] + ' '
    return text
