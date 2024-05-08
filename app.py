from fastapi import FastAPI, File, UploadFile, HTTPException
import os

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

        front_text = "uploads/front.jpg"
        back_text = "uploads/back.jpg"

        return {"message": "Upload successful", "status_code": 200}
    except Exception as e:
        return {"message": f"Internal server error: {str(e)}", "status_code": 500}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)