from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import os

from utils import licence_dect, ner_recog, read_text_img

app = FastAPI()

# Directory to save the uploaded images
UPLOAD_DIR = "uploads"

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_items():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome to My App</title>
        <style>
        .text {
            font-family: Arial, sans-serif;
            font-size: 16px;
            font-weight: bold;
            color: #333;
            line-height: 1.5;
            text-align: center;
            text-decoration: none;
            text-transform: uppercase;
            letter-spacing: 1px;
            word-spacing: 2px;
            border: 2px solid #ccc;
            border-radius: 18px;
            padding: 25px;
            }

            body {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }
            .footer {
                margin-top: 50px;
                font-size: 14px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to VVIMS AI App! 😊</h1>
            <p class="text"> Explore the wonders of our OCR and ANPR APIs! These powerful tools utilize AI to effortlessly decipher and recognize elements within Cameroonian ID cards, extracting valuable information with just a simple call to the <code> "/idextract" </code> endpoint. With our technology, you'll gain the ability to see beyond the surface and effortlessly identify vehicle license plates using the <code>"/carplate"</code> endpoint. The power is now yours to wield. Unleash the full potential of these tools and revolutionize your workflow..</p>
            <p>Let this app be the beginning of your journey towards greatness!</p>
        </div>
        <div class="footer">
            <p>Made with ❤️ by Ntchinda Giscard</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/idextract", description="This endpoint expects two files one named front and the other back which corresponds to the front and back of the id card, and returns a list of with entity_back and entity_front being the extracted infomation from the image")
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

@app.post("/carplate", description="This endpoint expects a file named license and return a list of turple having the detected number plates and the extracted text")
async def carplate(license: UploadFile = File(...)):
    img_path = 'uploads/car.jpg'
    try:
        if not license:
            raise HTTPException(status_code=400, detail="License plate image is required.")
         # Save the back image to disk
        license_path = os.path.join(UPLOAD_DIR, 'car.jpg')
        with open(license_path, "wb") as license_file:
            license_file.write(await license.read())
        result =  licence_dect(license_path)

        return{"message" : "Upload successful", "status_code" : 200, "data" : result}
    except Exception as e:
        return {"message": f"Internal server error: {str(e)}", "status_code": 500}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)