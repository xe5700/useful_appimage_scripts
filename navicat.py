#!/usr/bin/python3
import os
import subprocess
import glob
import sys
import time

from kdotool import Kdotool
from querywindow import queryWindowInfo
kdotool = Kdotool(bin=os.path.expanduser("~/.local/bin/kdotool"))
def find_latest_appimage(directory, base_name):
    # 查找所有的 .AppImage 文件
    appimage_files = glob.glob(os.path.join(directory, f"{base_name}*-premium-cs*.AppImage"))
    
    if not appimage_files:
        print("没有找到任何 .AppImage 文件")
        return None
    # items = []
    # for item in appimage_files:
    #     if item.endswith("premium-cs.AppImage"):
    #         items += item
    #         pass      
    # 获取最新的文件
    latest_file = max(appimage_files, key=os.path.getctime)
    return latest_file

def run_appimage(appimage_path, args):
    # 运行 .AppImage 文件并传递命令行参数
    try:
        os.system("dconf reset -f /com/premiumsoft/navicat-premium/")
        os.system("sed -i -E 's/,?\"([A-Z0-9]+)\":\{([^\}]+)},?//g' ~/.config/navicat/Premium/preferences.json")
        p = subprocess.Popen([appimage_path] + args)
        time.sleep(2)
        for i in range(10): 
            try:
                window_id = kdotool.search("注册",{"--name": True})
                if window_id and len(window_id) > 0:
                    kdotool.window_close(window_id)
                    break
                    print(window_id)
                # info = queryWindowInfo()
                # if info["activities"] == "caption: 注册":
                #     #pyautogui.press('esc') 
                #     subprocess.run(["ydotool","key","1:1", "1:0"])
                #    
                #     break
                #     pass
                time.sleep(1)
                pass
            except subprocess.CalledProcessError as e:
                pass
        p.wait()
    
    except subprocess.CalledProcessError as e:
        print(f"运行 {appimage_path} 时出错: {e}")

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    appimage_name = "navicat"  # 只需指定到版本号前缀
    
    latest_appimage = find_latest_appimage(script_directory, appimage_name)
    
    if latest_appimage:
        # 获取系统传过来的命令行参数（去掉脚本名）
        command_line_args = sys.argv[1:]
        run_appimage(latest_appimage, command_line_args)
