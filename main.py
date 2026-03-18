"""
Honda AI Main Entry Point
نقطة البداية الرئيسية لنظام هوندا
"""

import asyncio
from core.honda import Honda
from core.logger import HondaLogger

async def main():
    """الدالة الرئيسية"""
    logger = HondaLogger("Main")
    
    try:
        # Initialize Honda System
        honda = Honda()
        
        # Start the system
        await honda.start()
        
        # Keep system running
        logger.info("💡 نظام هوندا جاهز للاستخدام")
        
        # Placeholder for main loop
        while True:
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("\n⏹️ تم إيقاف النظام من قبل المستخدم")
    except Exception as e:
        logger.error(f"❌ خطأ في النظام الرئيسي: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Failed to start Honda: {e}")
