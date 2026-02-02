import torch
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained(
    "prompthero/openjourney",
    torch_dtype=torch.float32
)

pipe.to("cpu")  # switch to "cuda" later if you ever get a GPU

prompt = "portrait of a astronaut golden fish in space, digital art"

image = pipe(
    prompt=prompt,
    num_inference_steps=20,
    guidance_scale=7
).images[0]

image.save("result_2.png")
print("generated")