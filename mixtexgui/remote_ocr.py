# Remote OCR for MixTeX
import base64
import json
from io import BytesIO
import requests

class RemoteOCR:
    def __init__(self, base_url, api_key, model_name, log_callback=None):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name
        self.log_callback = log_callback  # 用于输出状态到主窗口
    
    def log(self, message):
        """输出日志到主窗口"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
    
    def image_to_base64(self, image):
        """将PIL Image转换为base64字符串"""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def recognize(self, image, use_inline_dollars=False, use_display_mode=False):
        """调用远程API识别图片中的LaTeX
        
        Args:
            image: PIL Image 对象
            use_inline_dollars: 是否使用 $ ... $ 包裹行内公式
            use_display_mode: 是否将多行公式转为 $$ ... $$
        """
        try:
            self.log("正在调用远程API...")
            
            # 转换图片为base64
            image_base64 = self.image_to_base64(image)
            
            # 所有模式统一使用一句话提示词
            prompt = "Only output the recognized text."
            
            # 构建请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_base64
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 2000
            }
            
            # 发送请求
            self.log("等待API响应...")
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                self.log("API调用成功")
                return content.strip()
            else:
                error_msg = f"API调用失败 [{response.status_code}]: {response.text[:200]}"
                self.log(error_msg)
                return ""
        
        except requests.exceptions.Timeout:
            self.log("API调用超时(30秒)，请检查网络连接")
            return ""
        except requests.exceptions.ConnectionError:
            self.log("网络连接失败，请检查网络或API地址")
            return ""
        except Exception as e:
            self.log(f"远程OCR错误: {str(e)}")
            return ""
