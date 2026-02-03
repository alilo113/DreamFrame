from diffusers import StableDiffusionXLPipeline
import torch

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float32,
    use_safetensors=True,
    safety_checker=None,
)

pipe = pipe.to("cpu")  # change to "cuda" if you have GPU

prompt = (
    "A regal cat in a futuristic astronaut suit, floating in outer space, close-up portrait, "
    "intricate astronaut suit details, glowing buttons, cinematic lighting, sharp focus on face, "
    "distant galaxies and colorful nebulae, hyper-realistic digital art, ultra-detailed"
)

negative_prompt = (
    "low quality, blurry, cartoon, anime, CGI, plastic skin, "
    "distorted face, extra limbs, watermark, text"
)

generator = torch.Generator(device="cpu").manual_seed(123456)

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=28,
    guidance_scale=7.5,
    generator=generator,
).images[0]

image.save("portrait_2.png")
print("Image generated")