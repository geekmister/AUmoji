import os
from pathlib import Path

import torch
from diffusers import StableDiffusionXLPipeline
from huggingface_hub import snapshot_download
from PIL import Image
from rembg import remove

# -------------------------- 配置区（仅需修改这里，一次配置永久复用） --------------------------
# 1. 基准图路径（你提前生成的完美符合要求的人物基准图）
BASE_IMAGE_PATH = "./base_face.png"
# 2. 生成图保存文件夹
SAVE_DIR = "./au_schematics"
# 3. 全局固定正向提示词
BASE_PROMPT = """
1:1 square ratio, portrait photography, ultra HD 8K, sharp focus, detailed facial features, no distortion, studio soft light, frontal face shot, head fully displayed, close-up facial shot, young beautiful chinese woman, sweet features, light makeup, no bangs, hair pulled back neatly, wearing white collared shirt, solid neutral gray background, only facial expression changes, no body movement
"""
# 4. 全局固定否定提示词
NEGATIVE_PROMPT = """
bang, fringe, messy hair, hat, accessories, earrings, necklace, heavy makeup, deformed face, distorted features, cross-eyed, blurry, low resolution, watermark, text, logo, background clutter, extra limbs, body shot, profile face, tilted head, multiple people, unrelated facial movements, non-target expression
"""
# 5. AU列表（可随时新增/修改，格式：(AU编号, 专属提示词)）
AU_LIST = [
    ("AU1", "inner eyebrows raised, only inner brow movement, no other facial action"),
    ("AU2", "outer eyebrows raised, only outer brow movement, no other facial action"),
    ("AU4", "eyebrows lowered and pulled together, frowning, glabellar wrinkles, no other facial action"),
    ("AU5", "upper eyelids raised, eyes wide open, no other facial action"),
    ("AU6", "cheek raised, orbicularis oculi contracted, under-eye pouches prominent, crow's feet, no mouth movement"),
    ("AU12", "mouth corners pulled up and back, closed mouth smile, no teeth exposed, only lip corner movement"),
    # 在这里继续添加剩余所有AU的编号和提示词即可
]
# 6. 生成参数
GENERATION_CONFIG = {
    "width": 1024,
    "height": 1024,
    "num_inference_steps": 25,
    "guidance_scale": 7.0,
    "ip_adapter_scale": 0.85, # 人物锁定权重，0.8-0.9效果最佳
}
# -----------------------------------------------------------------------------------------------

MODEL_REPO = "stabilityai/stable-diffusion-xl-base-1.0"
IP_ADAPTER_REPO = "h94/IP-Adapter"
IP_ADAPTER_SUBFOLDER = "sdxl_models"
IP_ADAPTER_WEIGHT = "ip-adapter-plus-face_sdxl_vit-h.safetensors"


def _ensure_models_downloaded() -> None:
    """预下载模型并显示 Hugging Face 下载进度条。"""
    print("⬇️ 检查并下载 SDXL 基座模型（如已缓存将跳过）...")
    snapshot_download(repo_id=MODEL_REPO)

    print("⬇️ 检查并下载 IP-Adapter 权重（如已缓存将跳过）...")
    snapshot_download(repo_id=IP_ADAPTER_REPO, allow_patterns=[f"{IP_ADAPTER_SUBFOLDER}/*"])


def _build_pipeline() -> StableDiffusionXLPipeline:
    """按设备自动选择精度，避免 CPU 场景下 fp16 导致异常。"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    use_fp16 = device == "cuda"

    kwargs = {
        "torch_dtype": torch.float16 if use_fp16 else torch.float32,
    }
    if use_fp16:
        kwargs["variant"] = "fp16"

    pipe = StableDiffusionXLPipeline.from_pretrained(MODEL_REPO, **kwargs).to(device)
    pipe.load_ip_adapter(
        IP_ADAPTER_REPO,
        subfolder=IP_ADAPTER_SUBFOLDER,
        weight_name=IP_ADAPTER_WEIGHT,
    )
    pipe.set_ip_adapter_scale(GENERATION_CONFIG["ip_adapter_scale"])
    return pipe


def main() -> None:
    save_dir = Path(SAVE_DIR)
    save_dir.mkdir(parents=True, exist_ok=True)

    base_image_path = Path(BASE_IMAGE_PATH)
    if not base_image_path.exists():
        raise FileNotFoundError(f"基准图不存在: {base_image_path}")

    _ensure_models_downloaded()
    pipe = _build_pipeline()
    base_image = Image.open(base_image_path).convert("RGB")

    # 批量生成 + 自动透明背景处理
    for au_id, au_prompt in AU_LIST:
        print(f"🎬 正在生成 {au_id} 示意图...")
        full_prompt = f"{BASE_PROMPT}, {au_prompt}"

        image = pipe(
            prompt=full_prompt,
            negative_prompt=NEGATIVE_PROMPT,
            ip_adapter_image=base_image,
            width=GENERATION_CONFIG["width"],
            height=GENERATION_CONFIG["height"],
            num_inference_steps=GENERATION_CONFIG["num_inference_steps"],
            guidance_scale=GENERATION_CONFIG["guidance_scale"],
        ).images[0]

        image_transparent = remove(image)
        save_path = save_dir / f"{au_id}.png"
        image_transparent.save(save_path, format="PNG")
        print(f"✅ {au_id} 已保存: {save_path}")

    print("✅ 所有 AU 示意图批量生成完成，均已处理为透明背景！")


if __name__ == "__main__":
    main()