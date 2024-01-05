from dependency_modules.rewarding.models import BaseT2IModel
from dependency_modules.rewarding.utils import download_checkpoint
import diffusers
import torch
import os


class StableDiffusion(BaseT2IModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_model(self, checkpoint_file, download_url):
        if not os.path.exists(checkpoint_file):
            download_checkpoint(download_url, checkpoint_file)

        pipe = diffusers.StableDiffusionPipeline.from_single_file(
            checkpoint_file, use_safetensors=True, torch_dtype=torch.float16
        )
        pipe.scheduler = diffusers.EulerAncestralDiscreteScheduler.from_config(
            pipe.scheduler.config
        )
        pipe.to("cuda")

        def inference_function(*args, **kwargs):
            return pipe(*args, **kwargs)

        return inference_function


class StableDiffusionXL(BaseT2IModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_model(self, checkpoint_file, download_url):
        if not os.path.exists(checkpoint_file):
            download_checkpoint(download_url, checkpoint_file)

        pipe = diffusers.StableDiffusionXLPipeline.from_single_file(
            checkpoint_file, use_safetensors=True, torch_dtype=torch.float16
        )
        pipe.scheduler = diffusers.EulerAncestralDiscreteScheduler.from_config(
            pipe.scheduler.config
        )
        pipe.to("cuda")

        def inference_function(*args, **kwargs):
            return pipe(*args, **kwargs)

        return inference_function
