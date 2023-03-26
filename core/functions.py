import logging
from pathlib import Path
from typing import Dict

from diffusers.models.attention_processor import AttnProcessor2_0
from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion import (
    StableDiffusionPipeline,
)
from PIL import Image

from core.config import config

logger = logging.getLogger(__name__)


def optimize_model(pipe: StableDiffusionPipeline) -> None:
    "Optimize the model for inference"

    logger.info("Optimizing model")

    if config.api.lowVRAM:
        pipe.enable_model_cpu_offload()
        logger.info("Optimization: Enabled model CPU offload")

    pipe.enable_vae_slicing()
    logger.info("Optimization: Enabled VAE slicing")

    try:
        pipe.enable_xformers_memory_efficient_attention()
        logger.info("Optimization: Enabled xFormers memory efficient attention")
    except ModuleNotFoundError:
        pipe.unet.set_attn_processor(AttnProcessor2_0())  # type: ignore
        logger.info("Optimization: Enabled SDPA, because xformers is not installed")

        logger.info("Optimization complete")


def image_meta_from_file(path: Path) -> Dict[str, str]:
    "Return image metadata from a file"

    with path.open("rb") as f:
        image = Image.open(f)
        text = image.text  # type: ignore

        return text
