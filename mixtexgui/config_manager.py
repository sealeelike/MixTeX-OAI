# Config Manager for MixTeX
import json
import os

class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.default_config = {
            "model_type": "local",  # "local" or "remote"
            "remote_api": {
                "base_url": "https://api.siliconflow.cn/v1/chat/completions",
                "api_key": "",
                "model_name": "deepseek-ai/DeepSeek-OCR"
            }
        }
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件，如果不存在则创建默认配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置失败: {e}")
                return self.default_config.copy()
        else:
            return self.default_config.copy()
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def get_model_type(self):
        """获取当前模型类型"""
        return self.config.get("model_type", "local")
    
    def set_model_type(self, model_type):
        """设置模型类型"""
        self.config["model_type"] = model_type
        self.save_config()
    
    def get_remote_config(self):
        """获取远程API配置"""
        return self.config.get("remote_api", {})
    
    def set_remote_config(self, base_url, api_key, model_name):
        """设置远程API配置"""
        self.config["remote_api"] = {
            "base_url": base_url,
            "api_key": api_key,
            "model_name": model_name
        }
        self.save_config()
