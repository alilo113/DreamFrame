from fastapi import APIRouter, Request, HTTPException
from diffusers import StableDiffusionPipeline
import torch
import uuid
import os

generating_router = APIRouter(
    prefix="/generating",
    tags=["generating"]
)

# ------------------ Load model ONCE ------------------
MODEL_ID = "dreamlike-art/dreamlike-diffusion-1.0"

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32
)

pipe = pipe.to("cpu")  # change to "cuda" later if you have GPU
pipe.enable_attention_slicing()
# ----------------------------------------------------


@generating_router.post("/generate")
async def generate_image(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    negative_prompt = (
        "extra face, multiple faces, duplicate face, bad anatomy, "
        "extra limbs, extra eyes, distorted face, blurry, "
        "low resolution, cartoon, anime, plastic skin, text, watermark"
    )

    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=30,
        guidance_scale=7.5,
        width=768,
        height=960
    ).images[0]

    os.makedirs("generated", exist_ok=True)
    filename = f"{uuid.uuid4()}.png"
    path = f"generated/{filename}"
    image.save(path)

    return {
        "message": "Image generated",
        "image_url": f"/{path}"
    }