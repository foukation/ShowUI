from flask import Flask, request, jsonify
import torch
from PIL import Image
import numpy as np
import base64
from io import BytesIO
from datetime import datetime
import os
import ast

# 保持原有的模型和处理器导入
from qwen_vl_utils import process_vision_info
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from model_loader import get_model_and_processor

app = Flask(__name__)

# 保持原有的常量定义
MIN_PIXELS = 256 * 28 * 28
MAX_PIXELS = 1344 * 28 * 28
_SYSTEM = "Based on the screenshot of the page, I give a text description and you give its corresponding location. The coordinate represents a clickable location [x, y] for an element, which is a relative coordinate on the screenshot, scaled from 0 to 1."

# 使用原有的模型加载代码
# model = Qwen2VLForConditionalGeneration.from_pretrained(
#     "../../data/huggingface/showui-2b",
#     torch_dtype=torch.bfloat16,
#     device_map="cpu",
# )

# processor = AutoProcessor.from_pretrained(
#     "../../data/huggingface/Qwen/Qwen2-VL-2B-Instruct",
#     min_pixels=MIN_PIXELS,
#     max_pixels=MAX_PIXELS
# )

model, processor = get_model_and_processor()

def save_uploaded_image(image_data):
    """保存上传的图片并返回路径"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.png"

    # 确保目录存在
    os.makedirs("temp_images", exist_ok=True)
    filepath = os.path.join("temp_images", filename)

    image_data.save(filepath)
    return filepath


def encode_image_base64(image):
    """将图片转换为 base64 编码"""
    # buffered = BytesIO()
    # image.save(buffered, format="PNG")
    # return base64.b64encode(buffered.getvalue()).decode()


@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # 1. 验证请求数据
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        if 'query' not in request.form:
            return jsonify({'error': 'No query text provided'}), 400

        image_file = request.files['image']
        query = request.form['query']

        # 2. 保存上传的图片
        image = Image.open(image_file)
        image_path = save_uploaded_image(image)

        try:
            # 3. 使用原有的推理流程
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": _SYSTEM},
                        {"type": "image", "image": image_path, "min_pixels": MIN_PIXELS, "max_pixels": MAX_PIXELS},
                        {"type": "text", "text": query}
                    ],
                }
            ]

            # 移动模型到 GPU（保持原有逻辑）
            global model
            model = model.to("cuda")

            # 处理输入
            text = processor.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )

            image_inputs, video_inputs = process_vision_info(messages)
            inputs = processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt"
            )
            inputs = inputs.to("cuda")

            # 生成输出
            generated_ids = model.generate(**inputs, max_new_tokens=128)
            generated_ids_trimmed = [
                out_ids[len(in_ids):]
                for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]

            output_text = processor.batch_decode(
                generated_ids_trimmed,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False
            )[0]

            # 解析坐标
            coordinates = ast.literal_eval(output_text)

            # 4. 在图片上绘制点
            # width, height = image.size
            # x, y = coordinates[0] * width, coordinates[1] * height
            # from PIL import ImageDraw
            # draw = ImageDraw.Draw(image)
            # radius = 10
            # draw.ellipse(
            #     (x - radius, y - radius, x + radius, y + radius),
            #     fill='red'
            # )

            # 5. 转换结果图片为 base64
            # result_image_base64 = encode_image_base64(image)

            # 6. 返回结果
            return jsonify({
                'success': True,
                'data': {
                    'coordinates': coordinates,
                    # 'result_image': result_image_base64
                }
            })

        finally:
            pass
            # 7. 清理临时文件
            # if os.path.exists(image_path):
            #     os.remove(image_path)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11506, debug=False)
