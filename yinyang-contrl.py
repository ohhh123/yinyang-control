import asyncio
import math
import time
from asyncio import Future
from typing import Any

import pyautogui
from pynput import keyboard

reset_radspeed = 2.5 * 0.3

rad = 0.0  # 单位 rad
radspeed = 0  # 单位 rad/s
time_interval = 0.1  # 单位 s
screen_width, screen_height = pyautogui.size()
screen_center_x = screen_width / 2
screen_center_y = screen_height / 2
lasttime = time.time()

# 异步函数，用于更新角度
async def update_rad():
    global rad, radspeed, lasttime
    while True:
        timeuased = time.time() - lasttime
        mouse_x, mouse_y = pyautogui.position()
        x = mouse_x - screen_center_x
        y = mouse_y - screen_center_y
        targetrad = math.atan2(-y, -x) + math.pi
        l = (targetrad - rad + math.pi) % (2 * math.pi) - math.pi

        #print(f"rad: {rad}, targetrad: {targetrad}, l: {l}")

        rad = (rad + radspeed * (timeuased)) % (2 * math.pi)
        if abs(l) > 0.2:
            #print(l > 0, radspeed < 0)
            if (l > 0 and radspeed < 0) or (l < 0 and radspeed > 0):
                pyautogui.press('0')
                radspeed = -radspeed

        lasttime = time.time()
        await asyncio.sleep(time_interval)

# 异步函数，用于监听按键
def listen_for_keys():
    print("o1")
    def on_press(key):
        global radspeed, reset_radspeed, rad
        if key == keyboard.Key.esc:
            return False
        try:
            if key.char == 'o':
                print(f"o2")
                if radspeed == 0:
                    radspeed = reset_radspeed
                    mouse_x, mouse_y = pyautogui.position()
                    x = mouse_x - screen_center_x
                    y = mouse_y - screen_center_y
                    rad = math.atan2(-y, -x) + math.pi
                else:
                    reset_radspeed = radspeed
                    radspeed = 0
        except AttributeError:
            pass
    listener = keyboard.Listener(on_press=on_press)
    #loop.run_in_executor(None, listener.join)
    listener.start()

# 异步函数，用于等待用户输入
async def listen_for_input():
    global reset_radspeed
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, input, "Please enter numbers: ")

    while True:
        user_input = await future
        try:
            user_input = float(user_input) * 0.3
            reset_radspeed = user_input
        except ValueError:
            print(f"This is not a valid number.{radspeed}")
        future = loop.run_in_executor(None, input, "Please enter numbers: ")

# 主函数，用于并行运行所有异步任务
async def main():
    listen_for_keys()
    await asyncio.gather(
        update_rad(),
        listen_for_input()
    )

# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())
