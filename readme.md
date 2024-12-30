# Image Generation ComfyUI API

## Overview
This project provides a FastAPI-based web application that transforms images into various artistic styles, including anime, cartoon, Disney, and avatar styles. Each transformation is implemented as a separate endpoint.

## Features
- **Anime Style**: Converts uploaded images into anime-inspired artwork.
- **Cartoon Style**: Generates cartoon-like images with bold outlines and vibrant colors.
- **Disney Style**: Creates Disney-inspired portraits with fairy-tale aesthetics.
- **Avatar Style**: Produces digital avatars with semi-realistic features, perfect for profile pictures.

## Project Structure
```
project-root/
├── main.py          # Main application file that integrates all routers
├── img2anime.py     # Endpoint for anime-style transformation
├── img2cartoon.py   # Endpoint for cartoon-style transformation
├── img2disney.py    # Endpoint for Disney-style transformation
├── img2avatar.py    # Endpoint for avatar-style transformation
├── shared.py        # Shared utilities and functions
├── workflows/       # JSON workflow files for each transformation
│   ├── img2anime_workflow.json
│   ├── img2cartoon_workflow.json
│   ├── img2disney_workflow.json
│   └── img2avatar_workflow.json
├── uploaded_images/ # Folder for storing uploaded images temporarily
└── requirements.txt # Project dependencies
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Metex-Labz-AI-Projects/photolabz-compfyui
   cd photolabz-compfyui
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints
### `/img2anime`
- **Method**: POST
- **Parameters**:
  - `pos_prompt` (string): Description of the desired image style.
  - `denoising_strength` (float): Controls the level of transformation.
  - `image` (file): Input image to be transformed.
- **Response**: Streamed PNG image.

### `/img2cartoon`
- **Method**: POST
- **Parameters**:
  - `pos_prompt` (string): Description of the desired image style.
  - `denoising_strength` (float): Controls the level of transformation.
  - `image` (file): Input image to be transformed.
- **Response**: Streamed PNG image.

### `/img2disney`
- **Method**: POST
- **Parameters**:
  - `pos_prompt` (string): Description of the desired image style.
  - `denoising_strength` (float): Controls the level of transformation.
  - `image` (file): Input image to be transformed.
- **Response**: Streamed PNG image.

### `/img2avatar`
- **Method**: POST
- **Parameters**:
  - `pos_prompt` (string): Description of the desired image style.
  - `denoising_strength` (float): Controls the level of transformation.
  - `image` (file): Input image to be transformed.
- **Response**: Streamed PNG image.

## Notes
- Ensure that the `workflows` folder contains valid JSON configurations for each transformation.
- The `uploaded_images` folder is used for temporary storage and will automatically clean up images post-processing.
- The `shared.py` module should include common utilities, such as image resizing functions.

## Future Enhancements
- Add support for additional artistic styles.
- Implement caching for frequently requested transformations.
- Enhance error handling and logging mechanisms.



