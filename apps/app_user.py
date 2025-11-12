# """
# HS-F26-L 语音播报模块驱动
# """

# from machine import Pin
# import time
# import asyncio


# class HSF26L:
#     """语音播报模块驱动类（OTP语音芯片，127段语音）
#     通信协议：单总线协议
#     """

#     # 语音索引（0-126段，共127段）
#     # 根据模块文档，通过单总线协议发送命令

#     def __init__(self, pin: int):
#         """初始化语音播报模块

#         Args:
#             pin: GPIO引脚号
#         """
#         self.pin = pin
#         self.gpio = None
#         self.is_playing = False

#     async def async_init(self):
#         """异步初始化硬件"""
#         try:
#             self.gpio = Pin(self.pin, Pin.OUT)
#             self.gpio.value(1)  # 默认高电平
#             await asyncio.sleep_ms(100)
#         except Exception as e:
#             print(f"语音播报模块初始化失败: {e}")

#     def _send_byte(self, directives: int):
#         """发送一个字节（单总线协议）

#         协议说明：
#         - 起始信号：拉低5ms
#         - 数据位从低位到高位发送（bit0到bit7）
#         - 数据位0：高电平800us + 低电平2400us
#         - 数据位1：高电平2400us + 低电平800us
#         - 结束：拉高电平

#         Args:
#             directives: 要发送的字节
#         """
#         if not self.gpio:
#             return

#         # 起始信号：拉低5ms
#         self.gpio.value(0)
#         time.sleep_ms(5)

#         # 发送8位数据，从低位到高位
#         for i in range(8):
#             bit = (directives >> i) & 0x01
#             if bit == 0:
#                 # 数据位0：高800us，低2400us
#                 self.gpio.value(1)
#                 time.sleep_us(800)
#                 self.gpio.value(0)
#                 time.sleep_us(2400)
#             else:
#                 # 数据位1：高2400us，低800us
#                 self.gpio.value(1)
#                 time.sleep_us(2400)
#                 self.gpio.value(0)
#                 time.sleep_us(800)

#         # 结束：拉高电平
#         self.gpio.value(1)

#     async def play(self, index: int, delay: int = 1000) -> None:
#         """播放指定索引的语音

#         Args:
#             index: 语音索引，范围 0-126（共127段语音）
#             delay: 播放后延迟时间（毫秒），默认1000ms

#         完整语音列表：
#         0:老师, 1:爸爸, 2:妈妈, 3:爷爷, 4:奶奶, 5:姥姥, 6:姥爷, 7:哥哥, 8:姐姐, 9:叔叔,
#         10:阿姨, 11:上午, 12:下午, 13:晚上, 14:前方, 15:厘米, 16:新年快乐, 17:身体健康, 18:工作顺利, 19:学习进步,
#         20:您好, 21:谢谢, 22:的, 23:祝, 24:慢走, 25:欢迎光临, 26:亲爱的, 27:同学们, 28:工作辛苦了, 29:点,
#         30:打开, 31:关闭, 32:千, 33:百, 34:十/时, 35:1, 36:2, 37:3, 38:4, 39:5,
#         40:6, 41:7, 42:8, 43:9, 44:0, 45:当期, 46:转, 47:左, 48:右, 49:请,
#         50:已, 51:现在, 52:是, 53:红灯, 54:绿灯, 55:黄灯, 56:温度, 57:湿度, 58:欢迎常来, 59:还有,
#         60:秒, 61:分, 62:变, 63:等, 64:下一次, 65:功能, 66:障碍物, 67:世界那么大我想去看看, 68:今天, 69:年,
#         70:月, 71:日, 72:星期, 73:农历, 74:现在时刻, 75:北京时间, 76:整, 77:度, 78:百分之, 79:距离,
#         80:厘米, 81:明天, 82:天气, 83:白天, 84:夜间, 85:晴, 86:多云, 87:阴, 88:雨, 89:雷阵,
#         90:小, 91:中, 92:大, 93:夹, 94:雪, 95:雾, 96:霾, 97:风, 98:东, 99:南,
#         100:西, 101:北, 102:到, 103:级, 104:偏, 105:方向, 106:空气质量, 107:优, 108:良, 109:轻度污染,
#         110:中度污染, 111:重度污染, 112:上, 113:下, 114:接近, 115:远离, 116:灯, 117:远离, 118:红色, 119:绿色,
#         120:蓝色, 121:黄色, 122:白色, 123:叮-音效, 124:滴滴滴-闹铃音效, 125:叮叮叮叮升-音效, 126:叮叮叮叮降-音效
#         """
#         if not self.gpio:
#             return

#         try:
#             # 限制索引范围
#             index = max(0, min(126, index))

#             # 发送播放命令
#             self._send_byte(index)

#             # 播放后延迟
#             await asyncio.sleep_ms(delay)

#             self.is_playing = True
#         except Exception as e:
#             print(f"播放语音失败: {e}")

#     async def stop(self) -> None:
#         """停止播放（发送停止命令）"""
#         if not self.gpio:
#             return

#         try:
#             # 发送停止命令（索引0）
#             self._send_byte(0x00)

#             self.is_playing = False
#         except Exception as e:
#             print(f"停止播放失败: {e}")

#     async def play_sequence(self, indices: list, delay_ms: int = 1000) -> None:
#         """播放语音序列

#         Args:
#             indices: 语音索引列表
#             delay_ms: 每段语音之间的延迟时间（毫秒），默认1000ms
#         """
#         if not self.gpio:
#             return

#         try:
#             for index in indices:
#                 await self.play(index, delay_ms)
#         except Exception as e:
#             print(f"播放序列失败: {e}")

#     def deinit(self) -> None:
#         """释放资源"""
#         if self.gpio:
#             try:
#                 self.is_playing = False
#                 self.gpio.value(1)
#                 self.gpio = None
#             except Exception as e:
#                 print(f"释放资源失败: {e}")


# # ==========================================================
# # 用户逻辑代码（大模型生成）
# # ==========================================================

# import asyncio
# import machine


# class Controller:
#     """主控制器类"""

#     def __init__(self):
#         """初始化控制器和外设"""
#         # 初始化语音播报模块
#         self.voice_module = HSF26L(pin=9)

#         # 控制参数
#         self.left_motor_speed = 0
#         self.right_motor_speed = 0
#         self.is_moving = False

#         # 遥测数据
#         self.left_motor_status = "停止"
#         self.right_motor_status = "停止"

#     async def set_left_motor_speed(self, value):
#         """设置左电机速度参数"""
#         self.left_motor_speed = max(0, min(100, value))
#         # 实现具体控制逻辑

#     async def set_right_motor_speed(self, value):
#         """设置右电机速度参数"""
#         self.right_motor_speed = max(0, min(100, value))
#         # 实现具体控制逻辑

#     async def move_forward(self):
#         """前进功能"""
#         self.is_moving = True
#         self.left_motor_status = "前进"
#         self.right_motor_status = "前进"
#         # 实现前进逻辑

#     async def move_backward(self):
#         """后退功能"""
#         self.is_moving = True
#         self.left_motor_status = "后退"
#         self.right_motor_status = "后退"
#         # 实现后退逻辑

#     async def turn_left(self):
#         """左转功能"""
#         self.is_moving = True
#         self.left_motor_status = "左转"
#         self.right_motor_status = "右转"
#         # 实现左转逻辑

#     async def turn_right(self):
#         """右转功能"""
#         self.is_moving = True
#         self.left_motor_status = "右转"
#         self.right_motor_status = "左转"
#         # 实现右转逻辑

#     async def stop_movement(self):
#         """停止功能"""
#         self.is_moving = False
#         self.left_motor_status = "停止"
#         self.right_motor_status = "停止"
#         # 实现停止逻辑

#     async def say_hello_teacher(self):
#         """播放'老师你好'语音"""
#         # '老师'对应索引XX，'你好'对应索引YY
#         # 这里假设'老师'索引为10，'你好'索引为20
#         await self.voice_module.play_sequence([10, 20], 1000)

#     async def control_joystick(self, x, y):
#         """处理摇杆控制"""
#         # 实现摇杆控制逻辑
#         pass

#     async def get_telemetry(self):
#         """获取遥测数据"""
#         try:
#             telemetry_data = {
#                 "C1": str(self.left_motor_status),
#                 "C2": str(self.right_motor_status),
#             }
#             return telemetry_data
#         except Exception as e:
#             return None


# async def handle_commands(controller, remote_cache):
#     """处理遥控指令"""
#     while True:
#         try:
#             command = remote_cache.get_and_clear_command()
#             if command:
#                 cmd = command.get("cmd")
#                 args = command.get("args", {})

#                 # 摇杆控制
#                 if cmd == "J1":
#                     x = int(args.get("x", "0"))
#                     y = int(args.get("y", "0"))
#                     await controller.control_joystick(x, y)

#                 # 滑块控制
#                 elif cmd == "S1":
#                     x = int(args.get("x", "0"))
#                     await controller.set_left_motor_speed(x)
#                 elif cmd == "S2":
#                     x = int(args.get("x", "0"))
#                     await controller.set_right_motor_speed(x)

#                 # 按键控制
#                 elif cmd == "B1":
#                     await controller.move_forward()
#                 elif cmd == "B2":
#                     await controller.move_backward()
#                 elif cmd == "B3":
#                     await controller.turn_left()
#                 elif cmd == "B4":
#                     await controller.turn_right()
#                 elif cmd == "B5":
#                     await controller.stop_movement()
#                 elif cmd == "B6":
#                     await controller.say_hello_teacher()

#                 # 其他指令...

#             await asyncio.sleep_ms(10)
#         except Exception as e:
#             print("处理指令出错: {}".format(e))
#             await asyncio.sleep_ms(1000)


# async def send_telemetry_data(controller, udp_comm):
#     """定期发送遥测数据"""
#     while True:
#         try:
#             telemetry = await controller.get_telemetry()
#             if telemetry:
#                 udp_comm.send_telemetry(telemetry)
#             await asyncio.sleep_ms(200)
#         except Exception as e:
#             print("发送遥测出错: {}".format(e))
#             await asyncio.sleep_ms(200)

import machine
import time


def voice_broadcast(Pin, directives, delay):
    Pin.value(0)
    time.sleep_ms(5)
    for i in range(0, 8, 1):
        if ((directives >> i) & 0x01) == 0:
            Pin.value(1)
            time.sleep_us(800)
            Pin.value(0)
            time.sleep_us(2400)
        elif ((directives >> i) & 0x01) == 1:
            Pin.value(1)
            time.sleep_us(2400)
            Pin.value(0)
            time.sleep_us(800)
    Pin.value(1)
    time.sleep_ms(delay)


Pin9 = machine.Pin(9, machine.Pin.OUT)
Pin9.value(1)
time.sleep_ms(10)


def main():
    while True:
        voice_broadcast(Pin9, 0x10, 1000)
        voice_broadcast(Pin9, 0x11, 1000)
        voice_broadcast(Pin9, 0x12, 1000)
        voice_broadcast(Pin9, 0x13, 1000)
        time.sleep_ms(1000)


if __name__ == "__main__":
    main()
