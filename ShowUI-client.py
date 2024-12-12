import requests
import base64
from PIL import Image
import io

def test_predict_api(image_path, query):
    # API endpoint
    url = "http://36.213.71.72:11503/api/predict"
    
    # 准备文件和数据
    files = {
        'image': ('image.png', open(image_path, 'rb'), 'image/png')
    }
    
    data = {
        'query': query
    }
    
    try:
        # 发送请求
        response = requests.post(url, files=files, data=data)
        
        # 确保文件被正确关闭
        files['image'][1].close()
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                # 获取坐标
                coordinates = result['data']['coordinates']
                print(f"点击坐标: {coordinates}")
                
                # 将 base64 图片转换为 PIL Image 并显示或保存
                image_data = base64.b64decode(result['data']['result_image'])
                result_image = Image.open(io.BytesIO(image_data))
                
                # 保存结果图片
                result_image.save('result.png')
                print("结果图片已保存为 result.png")
                
                return result
            else:
                print(f"API 调用失败: {result.get('error')}")
                return None
        else:
            print(f"HTTP 错误: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
            
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None

# 使用示例
if __name__ == "__main__":
    image_path = "examples/app_store.png"  # 图片路径
    query = "Download Kindle"              # 查询文本
    
    result = test_predict_api(image_path, query)
    if result:
        print("API 调用成功!")
        print(f"完整响应: {result}")
