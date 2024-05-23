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

    return response.json()['data']['entity_front']

# Example usage:
front_image_path = "IMG_0096.jpg"
back_image_path = "IMG_0097.jpg"
url = "https://a13a-129-0-226-192.ngrok-free.app/idextract"  # Change this URL to your FastAPI endpoint URL
response = upload_files_to_fastapi(front_image_path, back_image_path, url)
print(response)

import requests

def send_image_to_fastapi(image_path: str, url: str):
    # Open the image file
    with open(image_path, 'rb') as file:
        # Create a dictionary containing the file (with key 'license')
        files = {'license': file}
        
        # Send a POST request to the FastAPI endpoint with the image file
        response = requests.post(url, files=files)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Image successfully sent to FastAPI endpoint", response.json())
        else:
            print(f"Failed to send image to FastAPI endpoint. Status code: {response.status_code}")

image_path = 'carplate.jpg'

# send_image_to_fastapi(image_path, url)

