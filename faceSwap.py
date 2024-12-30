import random
from fastapi import Form, File
from shared import *


@router.post("/faceswap")
async def generate_image(
        pos_prompt: str = Form(None),
        face_image: UploadFile = File(...),
        target_image: UploadFile = File(...),
):
    try:
        # Process face image
        face_image_path = process_image(face_image)

        if pos_prompt:
            with open("worflows/face_swap_api_workflow.json", "r", encoding="utf-8") as f:
                prompt = json.load(f)

            prompt_updates = {
                "2.inputs.text": pos_prompt,
                "17.inputs.image": face_image_path,
                "4.inputs.noise_seed": random.randint(1, 999999999999999),
            }

        else:
            with open("worflows/target_photo_face_swap_api.json", "r", encoding="utf-8") as f:
                prompt = json.load(f)

            target_image_path = process_image(target_image)
            prompt_updates = {
                "17.inputs.image": face_image_path,
                "19.inputs.image": target_image_path,
            }

        # Update prompt
        prompt = update_nested_prompt(prompt, prompt_updates)

        # Perform face swap
        return processed_ready_image(server_address, client_id, prompt)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")



# import random
# from fastapi import FastAPI, Form, File
# from shared import *
#
# app = FastAPI()
#
#
# @router.post("/faceswap")
# async def generate_image(
#         pos_prompt: str = Form(...),
#         image: UploadFile = File(...)
#
# ):
#     try:
#         temp_image_path = process_image(image)
#         with open("worflows/face_swap_api_workflow.json", "r", encoding="utf-8") as f:
#             prompt = json.load(f)
#         prompt_updates = {
#             "2.inputs.text": pos_prompt,
#             "17.inputs.image": temp_image_path,
#             "4.inputs.noise_seed": random.randint(1, 999999999999999),
#         }
#         prompt = update_nested_prompt(prompt, prompt_updates)
#
#         # Perform face swap
#         return processed_ready_image(server_address, client_id, prompt)
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
#
#
#
#
# # import random
# # import tempfile
# # from fastapi import FastAPI, Form, HTTPException, File, UploadFile
# # from fastapi.responses import StreamingResponse
# # import io
# # from websockets_api import *
# #
# # app = FastAPI()
# #
# #
# # @router.post("/faceswap")
# # async def generate_image(
# #         pos_prompt: str = Form(...),
# #         image: UploadFile = File(...)
# #
# # ):
# #     with open("worflows/face_swap_api_workflow (1).json", "r", encoding="utf-8") as f:
# #         workflow_json_data = f.read()
# #
# #     prompt = json.loads(workflow_json_data)
# #     # #set the text prompt for our positive CLIPTextEncode
# #     prompt["2"]["inputs"]["text"] = pos_prompt
# #
# #     image_data = await image.read()
# #     original_image = Image.open(io.BytesIO(image_data))
# #     resized_image = resize_image(original_image)
# #     original_width, original_height = resized_image.size
# #     # print(f"Original Dimensions: {original_width}x{original_height}")
# #
# #     with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image_file:
# #         temp_image_path = temp_image_file.name
# #     resized_image.save(temp_image_path, format="PNG")
# #
# #     try:
# #         # Update workflow JSON with base64 image
# #         prompt["17"]["inputs"]["image"] = temp_image_path
# #         # prompt["6"]["inputs"]["width"] = original_width
# #         # prompt["6"]["inputs"]["height"] = original_height
# #
# #         print("Face is being swapped")
# #         seed = random.randint(1, 999999999999999)
# #         print(f"seed is: {seed}")
# #         prompt["4"]["inputs"]["noise_seed"] = seed
# #
# #         ws = websocket.WebSocket()
# #         ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
# #         images = get_images(ws, prompt)
# #         ws.close()
# #
# #         for node_id in images:
# #             for image in images[node_id]:
# #                 image_data = io.BytesIO(image)
# #                 if image_data:
# #                     return StreamingResponse(image_data, media_type="image/png")
# #
# #     except Exception as e:
# #         print(f"An error occurred: {e}")
# #
# #         raise HTTPException(status_code=500, detail="An error occurred. Please try again.")
# #
# #     return {"error": "Image generation failed"}
