from paddleocr import PaddleOCR, draw_ocr
import spacy
ocr_model = PaddleOCR(lang='en')



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
