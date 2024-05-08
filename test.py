import requests

def upload_files_to_fastapi(front_image_path, back_image_path, url):
    """
    Upload front and back images to a FastAPI app.

    Args:
    - front_image_path: Path to the front image file.
    - back_image_path: Path to the back image file.
    - url: The URL of the FastAPI endpoint to upload the files to.

    Returns:
    - dict: A dictionary containing the response from the FastAPI app.
    """
    # Open and read the front image file
    with open(front_image_path, "rb") as front_file:
        front_data = {"front": (front_image_path, front_file, "image/jpeg")}

        # Open and read the back image file
        with open(back_image_path, "rb") as back_file:
            back_data = {"back": (back_image_path, back_file, "image/jpeg")}

            # Upload the files to the FastAPI app
            response = requests.post(url, files={**front_data, **back_data})

    return response.json()

# Example usage:
front_image_path = "IMG_0096.jpg"
back_image_path = "IMG_0097.jpg"
url = "http://localhost:8000/idextract/"  # Change this URL to your FastAPI endpoint URL

response = upload_files_to_fastapi(front_image_path, back_image_path, url)
print(response)