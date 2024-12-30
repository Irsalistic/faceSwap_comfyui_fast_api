import io
import tempfile
import uuid
import json
import urllib.request
import urllib.parse

import websocket
from fastapi import APIRouter, UploadFile, HTTPException
from PIL import Image, PngImagePlugin
from fastapi.responses import StreamingResponse

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())
router = APIRouter()


def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    try:
        response = urllib.request.urlopen(req).read()
        return json.loads(response)
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
        print("Response:", e.read().decode())
        raise


def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()


def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())


def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break  #Execution is done
        else:
            # If you want to be able to decode the binary stream for latent previews, here is how you can do it:
            # bytesIO = BytesIO(out[8:])
            # preview_image = Image.open(bytesIO) # This is your preview in PIL image format, store it in a global
            continue  #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        images_output = []
        if 'images' in node_output:
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
        output_images[node_id] = images_output

    return output_images


max_dimension = 768
min_dimension = 320


def resize_image(img: Image.Image) -> Image.Image:
    original_width, original_height = img.size
    aspect_ratio = original_width / original_height

    # Start with the assumption that no resizing is needed
    new_width, new_height = original_width, original_height

    # Resize if either dimension is below the minimum
    if new_width < min_dimension or new_height < min_dimension:
        if aspect_ratio >= 1:  # Width is smaller or equal
            new_width = max(new_width, min_dimension)
            new_height = round(new_width / aspect_ratio)
        else:  # Height is smaller
            new_height = max(new_height, min_dimension)
            new_width = round(new_height * aspect_ratio)

    # Adjust if the new dimensions exceed the maximum allowed size
    if new_width > max_dimension or new_height > max_dimension:
        if aspect_ratio >= 1:  # Width is the larger dimension
            new_width = min(new_width, max_dimension)
            new_height = round(new_width / aspect_ratio)
        else:  # Height is the larger dimension
            new_height = min(new_height, max_dimension)
            new_width = round(new_height * aspect_ratio)

    # Round to the nearest multiple of 64 for both dimensions (optional, depends on your specific requirement)
    new_width = max(min_dimension, (round(new_width / 64) * 64))
    new_height = max(min_dimension, (round(new_height / 64) * 64))

    # Ensure that both dimensions are within the specified limits after rounding
    new_width = min(max(new_width, min_dimension), max_dimension)
    new_height = min(max(new_height, min_dimension), max_dimension)

    # Resize the image
    resized_image = img.resize((int(new_width), int(new_height)), Image.LANCZOS)
    return resized_image


def process_image(uploaded_file: UploadFile,resize=True) -> str:
    """Save the uploaded image to a temporary file and return its path."""
    image_data = uploaded_file.file.read()
    image = Image.open(io.BytesIO(image_data))
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_path = temp_file.name
    if resize:
        image = resize_image(image)

    image.save(temp_path,format="PNG")
    return temp_path


def update_nested_prompt(prompt: dict, updates: dict) -> dict:
    """Update a nested JSON workflow prompt."""
    for key, value in updates.items():
        keys = key.split(".")
        ref = prompt
        for part in keys[:-1]:
            ref = ref.setdefault(part, {})
        ref[keys[-1]] = value

    return prompt


def processed_ready_image(server_address: str, client_id: str, prompt: dict) -> StreamingResponse:
    """Connect to the WebSocket server and swap the face based on the prompt."""
    try:
        ws = websocket.WebSocket()
        ws.connect(f"ws://{server_address}/ws?clientId={client_id}")
        images = get_images(ws, prompt)
        ws.close()

        for node_id, node_images in images.items():
            for image in node_images:
                image_data = io.BytesIO(image)
                return StreamingResponse(image_data, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Face swapping failed: {e}")
