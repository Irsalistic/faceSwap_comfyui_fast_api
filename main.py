from fastapi import FastAPI
# create API client
app = FastAPI()

# Import routers from each endpoint module
from img2anime import router as img2anime_router
from img2avatar import router as img2avatar_router
from img2disney import router as img2disney_router
from img2cartoon import router as img2cartoon_router
from faceSwap import router as face_swap_router
from img_enhancer import router as enhancer_router
from bg_remover import router as bg_remover_router
from obj_remover import router as obj_remover_router

# Include routers in the application
app.include_router(img2anime_router)
app.include_router(img2avatar_router)
app.include_router(img2disney_router)
app.include_router(img2cartoon_router)
app.include_router(face_swap_router)
app.include_router(enhancer_router)
app.include_router(bg_remover_router)
app.include_router(obj_remover_router)
