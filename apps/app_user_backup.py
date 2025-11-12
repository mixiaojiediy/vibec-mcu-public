import asyncio
import machine
import time
import math

# WS2812控制类
class WS2812:
    def __init__(self, pin, num_leds):
        self.pin = pin
        self.num_leds = num_leds
        self.buffer = bytearray(num_leds * 3)
        self.neo = machine.Neopixel(pin, num_leds)
    
    def set_pixel(self, index, r, g, b):
        if 0 <= index < self.num_leds:
            self.neo.set(index, (r, g, b))
    
    def fill(self, r, g, b):
        for i in range(self.num_leds):
            self.neo.set(i, (r, g, b))
    
    def show(self):
        self.neo.write()
    
    def clear(self):
        self.fill(0, 0, 0)
        self.show()

# 灯盘控制器类
class LEDDiskController:
    def __init__(self, pin_num=1, num_leds=12):
        self.pin = machine.Pin(pin_num, machine.Pin.OUT)
        self.num_leds = num_leds
        self.ws2812 = WS2812(self.pin, num_leds)
        
        # 状态变量
        self.brightness = 50
        self.red = 255
        self.green = 255
        self.blue = 255
        self.animation_speed = 5
        self.rainbow_density = 6
        self.animation_mode = "static"  # static, breathing, flowing, rainbow
        
        # 动画控制变量
        self.animation_counter = 0
        self.breathing_direction = 1
        self.flow_position = 0
        
        # 初始化灯盘
        self.ws2812.fill(0, 0, 0)
        self.ws2812.show()
    
    async def set_brightness(self, value):
        """设置亮度"""
        self.brightness = max(0, min(255, int(value)))
        # 在静态模式下应用亮度
        if self.animation_mode == "static":
            self._apply_color()
    
    async def set_red(self, value):
        """设置红色值"""
        self.red = max(0, min(255, int(value)))
        if self.animation_mode == "static":
            self._apply_color()
    
    async def set_green(self, value):
        """设置绿色值"""
        self.green = max(0, min(255, int(value)))
        if self.animation_mode == "static":
            self._apply_color()
    
    async def set_blue(self, value):
        """设置蓝色值"""
        self.blue = max(0, min(255, int(value)))
        if self.animation_mode == "static":
            self._apply_color()
    
    async def set_animation_speed(self, value):
        """设置动画速度"""
        self.animation_speed = max(1, min(10, int(value)))
    
    async def set_rainbow_density(self, value):
        """设置彩虹密度"""
        self.rainbow_density = max(1, min(12, int(value)))
    
    async def all_on(self):
        """全亮"""
        self.animation_mode = "static"
        self._apply_color()
    
    async def all_off(self):
        """全灭"""
        self.animation_mode = "static"
        self.ws2812.fill(0, 0, 0)
        self.ws2812.show()
    
    async def breathing_light(self):
        """呼吸灯效果"""
        self.animation_mode = "breathing"
        self.animation_counter = 0
        self.breathing_direction = 1
    
    async def flowing_light(self):
        """流水灯效果"""
        self.animation_mode = "flowing"
        self.flow_position = 0
    
    async def rainbow_mode(self):
        """彩虹模式"""
        self.animation_mode = "rainbow"
        self.animation_counter = 0
    
    async def apply_color(self):
        """应用当前颜色设置"""
        self.animation_mode = "static"
        self._apply_color()
    
    def _apply_color(self):
        """应用当前颜色和亮度设置"""
        # 应用亮度调整
        r = int(self.red * self.brightness / 255)
        g = int(self.green * self.brightness / 255)
        b = int(self.blue * self.brightness / 255)
        self.ws2812.fill(r, g, b)
        self.ws2812.show()
    
    async def update_animation(self):
        """更新动画效果"""
        try:
            if self.animation_mode == "breathing":
                # 呼吸灯效果
                self.animation_counter += self.animation_speed
                if self.animation_counter >= 255:
                    self.animation_counter = 255
                    self.breathing_direction = -1
                elif self.animation_counter <= 0:
                    self.animation_counter = 0
                    self.breathing_direction = 1
                
                # 计算当前亮度
                brightness = self.animation_counter
                r = int(self.red * brightness / 255)
                g = int(self.green * brightness / 255)
                b = int(self.blue * brightness / 255)
                self.ws2812.fill(r, g, b)
                self.ws2812.show()
            
            elif self.animation_mode == "flowing":
                # 流水灯效果
                self.ws2812.clear()
                # 显示几个连续的灯
                for i in range(3):
                    pos = (self.flow_position + i) % self.num_leds
                    # 亮度渐变
                    brightness_factor = 1.0 - (i * 0.3)
                    r = int(self.red * self.brightness / 255 * brightness_factor)
                    g = int(self.green * self.brightness / 255 * brightness_factor)
                    b = int(self.blue * self.brightness / 255 * brightness_factor)
                    self.ws2812.set_pixel(pos, r, g, b)
                self.ws2812.show()
                self.flow_position = (self.flow_position + 1) % self.num_leds
            
            elif self.animation_mode == "rainbow":
                # 彩虹模式
                self.animation_counter += self.animation_speed
                for i in range(self.num_leds):
                    # 使用正弦函数生成颜色变化
                    hue = (i * self.rainbow_density + self.animation_counter) % 255
                    r, g, b = self._hue_to_rgb(hue)
                    # 应用亮度
                    r = int(r * self.brightness / 255)
                    g = int(g * self.brightness / 255)
                    b = int(b * self.brightness / 255)
                    self.ws2812.set_pixel(i, r, g, b)
                self.ws2812.show()
        except Exception as e:
            print(f"动画更新错误: {e}")
    
    def _hue_to_rgb(self, hue):
        """将色相值转换为RGB颜色"""
        hue = hue % 255
        if hue < 85:
            return (255, hue * 3, 0)
        elif hue < 170:
            hue -= 85
            return (255 - hue * 3, 255, 0)
        else:
            hue -= 170
            return (0, 255, hue * 3)
    
    async def get_telemetry(self):
        """获取遥测数据"""
        try:
            mode_names = {
                "static": "静态",
                "breathing": "呼吸",
                "flowing": "流水",
                "rainbow": "彩虹"
            }
            
            telemetry_data = {
                "C1": str(self.brightness),
                "C2": str(self.red),
                "C3": str(self.green),
                "C4": str(self.blue),
                "C5": mode_names.get(self.animation_mode, "未知"),
                "C6": str(0)
            }
            return telemetry_data
        except Exception as e:
            print(f"遥测数据获取错误: {e}")
            return None

async def handle_commands(controller, remote_cache):
    """处理遥控指令"""
    while True:
        try:
            command = remote_cache.get_and_clear_command()
            if command:
                cmd = command.get("cmd")
                args = command.get("args", {})
                
                # 处理滑块指令
                if cmd == "S1":  # 亮度
                    x = args.get("x", "0")
                    await controller.set_brightness(x)
                elif cmd == "S2":  # 红色
                    x = args.get("x", "0")
                    await controller.set_red(x)
                elif cmd == "S3":  # 绿色
                    x = args.get("x", "0")
                    await controller.set_green(x)
                elif cmd == "S4":  # 蓝色
                    x = args.get("x", "0")
                    await controller.set_blue(x)
                elif cmd == "S5":  # 动画速度
                    x = args.get("x", "0")
                    await controller.set_animation_speed(x)
                elif cmd == "S6":  # 彩虹密度
                    x = args.get("x", "0")
                    await controller.set_rainbow_density(x)
                
                # 处理按钮指令
                elif cmd == "B1":  # 全亮
                    await controller.all_on()
                elif cmd == "B2":  # 全灭
                    await controller.all_off()
                elif cmd == "B3":  # 呼吸灯
                    await controller.breathing_light()
                elif cmd == "B4":  # 流水灯
                    await controller.flowing_light()
                elif cmd == "B5":  # 彩虹模式
                    await controller.rainbow_mode()
                elif cmd == "B6":  # 应用颜色
                    await controller.apply_color()
                
                print(f"处理指令: {cmd}")
            
            await asyncio.sleep_ms(10)
        except Exception as e:
            print(f"处理指令时出错: {e}")
            await asyncio.sleep_ms(1000)

async def update_animations(controller):
    """更新动画效果"""
    while True:
        await controller.update_animation()
        await asyncio.sleep_ms(50)  # 50ms更新一次动画

async def send_telemetry_data(controller, udp_comm):
    """定期发送遥测数据"""
    while True:
        try:
            telemetry = await controller.get_telemetry()
            if telemetry:
                udp_comm.send_telemetry(telemetry)
            await asyncio.sleep(1)  # 每1秒发送一次
        except Exception as e:
            print(f"发送遥测数据时出错: {e}")
            await asyncio.sleep(1)

async def main(remote_cache, udp_comm):
    """主函数"""
    try:
        # 初始化控制器
        controller = LEDDiskController(pin_num=1, num_leds=12)
        
        # 创建主要任务
        app_tasks = [
            asyncio.create_task(handle_commands(controller, remote_cache)),
            asyncio.create_task(update_animations(controller)),
            asyncio.create_task(send_telemetry_data(controller, udp_comm)),
        ]
        
        await asyncio.gather(*app_tasks)
    except KeyboardInterrupt:
        print("收到停止信号")
    except Exception as e:
        print(f"主程序错误: {e}")
