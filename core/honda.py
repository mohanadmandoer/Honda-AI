"""
Honda Core System
النظام الأساسي لهوندا
"""

from .logger import HondaLogger
from .config import SYSTEM_NAME, DEFAULT_LANGUAGE
import asyncio

class Honda:
    """
    نظام هوندا الرئيسي
    Personal AI Assistant Operating System
    """
    
    def __init__(self):
        self.logger = HondaLogger()
        self.system_name = SYSTEM_NAME
        self.language = DEFAULT_LANGUAGE
        self.is_online = False
        self.modules = {}
        
        self.logger.info(f"🚀 {self.system_name} System Initialized")
        self.logger.info(f"لغة النظام الافتراضية: {self._get_language_name(self.language)}")
    
    def _get_language_name(self, lang_code: str) -> str:
        """الحصول على اسم اللغة"""
        names = {
            "ar": "العربية",
            "en": "English",
            "ru": "Русский"
        }
        return names.get(lang_code, "Unknown")
    
    def register_module(self, name: str, module):
        """تسجيل وحدة جديدة"""
        self.modules[name] = module
        self.logger.info(f"✅ تم تسجيل الوحدة: {name}")
    
    async def initialize_system(self):
        """تهيئة النظام بشكل كامل"""
        self.logger.info("🔧 جاري تهيئة النظام...")
        
        try:
            # سيتم إضافة التهيئة للوحدات هنا
            self.logger.info("✅ تمت تهيئة النظام بنجاح")
        except Exception as e:
            self.logger.error(f"❌ خطأ في التهيئة: {str(e)}")
            raise
    
    async def start(self):
        """بدء تشغيل النظام"""
        await self.initialize_system()
        self.logger.info(f"🟢 {self.system_name} الآن في وضع التشغيل")
    
    def shutdown(self):
        """إيقاف النظام"""
        self.logger.info(f"🔴 إيقاف {self.system_name}...")
        self.logger.info("تم الإيقاف بنجاح")
