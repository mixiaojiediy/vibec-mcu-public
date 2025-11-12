# boot.py - ESP32S3 MicroPython 启动程序入口
import asyncio
from core.boot_impl import main

# 执行主函数
if __name__ == "__main__":
    asyncio.run(main())
