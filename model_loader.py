from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
import torch

MIN_PIXELS = 256 * 28 * 28
MAX_PIXELS = 1344 * 28 * 28

class ModelLoader:
    _instance = None

    @staticmethod
    def get_instance():
        if ModelLoader._instance is None:
            ModelLoader._instance = ModelLoader()
        return ModelLoader._instance

    def __init__(self):
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            "../../data/huggingface/showui-2b",
            torch_dtype=torch.bfloat16,
            device_map="cpu",
        )
        self.processor = AutoProcessor.from_pretrained(
            "../../data/huggingface/Qwen/Qwen2-VL-2B-Instruct",
            min_pixels=MIN_PIXELS,
            max_pixels=MAX_PIXELS
        )

def get_model_and_processor():
    instance = ModelLoader.get_instance()
    return instance.model, instance.processor
