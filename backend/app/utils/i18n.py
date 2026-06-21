# backend/app/utils/i18n.py
import json
import os
from typing import Optional
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class I18nMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Lấy language từ header
        lang = request.headers.get("Accept-Language", "en")
        if lang not in ["en", "vi", "zh"]:
            lang = "en"
        
        # Lưu language vào request state
        request.state.lang = lang
        
        response = await call_next(request)
        return response

class Translator:
    def __init__(self):
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load tất cả file ngôn ngữ"""
        lang_dir = os.path.join(os.path.dirname(__file__), "../locales")
        for file in os.listdir(lang_dir):
            if file.endswith(".json"):
                lang = file.split(".")[0]
                with open(os.path.join(lang_dir, file), "r", encoding="utf-8") as f:
                    self.translations[lang] = json.load(f)
    
    def translate(self, key: str, lang: str = "en", **kwargs) -> str:
        """Dịch một key"""
        if lang not in self.translations:
            lang = "en"
        
        text = self.translations.get(lang, {}).get(key, key)
        
        # Thay thế placeholder
        for k, v in kwargs.items():
            text = text.replace(f"{{{k}}}", str(v))
        
        return text

translator = Translator()

def get_translator(request: Request):
    """Dependency để lấy translator"""
    return translator

def t(key: str, lang: str = "en", **kwargs) -> str:
    """Helper function để dịch"""
    return translator.translate(key, lang, **kwargs)