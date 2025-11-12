# main.py - ESP32S3 MicroPython 主程序入口
import asyncio
from core.main_impl import main

# 运行主程序
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user")
    except Exception as e:
        print(f"Program exited abnormally: {e}")
        from machine import reset

        reset()
