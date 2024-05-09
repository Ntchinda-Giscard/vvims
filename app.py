from fastapi import FastAPI, File, UploadFile, HTTPException
import os

from utils import ner_recog, read_text_img

app = FastAPI()

# Directory to save the uploaded images
UPLOAD_DIR = "uploads"

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/idextract/")
async def upload_files(front: UploadFile = File(...), back: UploadFile = File(...)):
    """
    Endpoint to receive front and back image uploads and save them to disk.

    Args:
    - front: The uploaded front image file.
    - back: The uploaded back image file.

    Returns:
    - dict: A dictionary containing information about the uploaded files.
    """
    try:
        # Check if either front or back image is missing
        if not front or not back:
            raise HTTPException(status_code=400, detail="Both front and back images are required.")

        # Save the front image to disk
        front_path = os.path.join(UPLOAD_DIR, 'front.jpg')
        with open(front_path, "wb") as front_file:
            front_file.write(await front.read())

        # Save the back image to disk
        back_path = os.path.join(UPLOAD_DIR, 'back.jpg')
        with open(back_path, "wb") as back_file:
            back_file.write(await back.read())

        front_img_path = "uploads/front.jpg"
        back_img_path = "uploads/back.jpg"

        front_text = read_text_img(front_img_path)
        back_text = read_text_img(back_img_path)
        
        ent_front = ner_recog(front_text)
        ent_back = ner_recog(back_text)
        



        return {"message": "Upload successful", "status_code": 200, "text_front": f'{front_text}', 'entity_front': ent_front, 'text_back': f'{back_text}', 'entity_back': ent_back}
    except Exception as e:
        return {"message": f"Internal server error: {str(e)}", "status_code": 500}

@app.post("/carplate")
async def carplate(license: UploadFile = File(...)):
    try:
        if not license:
            raise HTTPException(status_code=400, detail="Both front and back images are required.")
         # Save the back image to disk
        license_path = os.path.join(UPLOAD_DIR, 'car.jpg')
        with open(license_path, "wb") as license_file:
            license_file.write(await license.read())

        
    except Exception as e:
        return {"message": f"Internal server error: {str(e)}", "status_code": 500}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)