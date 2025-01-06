# FaceSwap API

A FastAPI-based service that provides face swapping capabilities using image processing and AI. The API supports both target-based face swapping and prompt-guided face generation.

## Features

- Face swapping between two images
- Prompt-guided face generation and swapping
- Support for custom image uploads
- Error handling and validation

## API Endpoints

### POST /faceswap

Performs face swapping operations based on provided inputs.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| pos_prompt | string | No | Text prompt for guided face generation |
| face_image | file | Yes | Source face image |
| target_image | file | Yes | Target image for face swapping |

#### Request Format

The request should be sent as `multipart/form-data` with the following fields:
- `face_image`: The source face image file
- `target_image`: The target image file
- `pos_prompt` (optional): Text prompt for guided generation

#### Response

Returns the processed image with the face swap applied.

#### Error Handling

The API returns a 500 status code with error details if processing fails.

## Dependencies

- FastAPI
- Python 3.x
- Additional dependencies in `requirements.txt` (to be installed)

## Usage Example

```python
import requests

url = "http://your-server/faceswap"

# Basic face swap
files = {
    'face_image': open('source_face.jpg', 'rb'),
    'target_image': open('target_image.jpg', 'rb')
}
response = requests.post(url, files=files)

# Prompt-guided face swap
files = {
    'face_image': open('source_face.jpg', 'rb'),
    'target_image': open('target_image.jpg', 'rb')
}
data = {
    'pos_prompt': 'your prompt here'
}
response = requests.post(url, files=files, data=data)
```

## Configuration

The API uses workflow configuration files:
- `workflows/face_swap_api_workflow.json`: For prompt-guided face generation
- `workflows/target_photo_face_swap_api.json`: For direct face swapping

## Error Handling

The API includes comprehensive error handling:
- Input validation for required files
- Processing error handling with detailed error messages
- HTTP 500 responses for server-side errors

## Notes

- Ensure proper file permissions for workflow JSON files
- Configure server address and client ID in your environment
- Handle large files appropriately in your deployment

