from paddleocr import PaddleOCR, draw_ocr
import spacy

ocr_model = PaddleOCR(lang='en')
nlp_ner = spacy.load("output/model-best")


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
  # print(res[1][0])
