#!/usr/bin/python3
import os
import subprocess
import glob
import sys

def find_latest_appimage(directory, base_name):
    # 查找所有的 .AppImage 文件
    appimage_files = glob.glob(os.path.join(directory, f"{base_name}*.AppImage"))
    
    if not appimage_files:
        print("没有找到任何 .AppImage 文件")
        return None

    # 获取最新的文件
    latest_file = max(appimage_files, key=os.path.getctime)
    return latest_file

def run_appimage(appimage_path, args):
    # 运行 .AppImage 文件并传递命令行参数
    try:
        subprocess.run([appimage_path] + args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"运行 {appimage_path} 时出错: {e}")

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    appimage_name = "OrcaSlicer_Linux_V"  # 只需指定到版本号前缀
    
    latest_appimage = find_latest_appimage(script_directory, appimage_name)
    
    if latest_appimage:
        # 获取系统传过来的命令行参数（去掉脚本名）
        command_line_args = sys.argv[1:]
        run_appimage(latest_appimage, command_line_args)
