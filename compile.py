import os

upx_dir = 'C:\\upx'
param_upx = ""


if os.path.exists(upx_dir):
    param_upx = f"--upx-dir \"{upx_dir}\""
    
os.system(f"pyinstaller main.py -F -w -i icon.ico -n CIPSafety-l5x-IO-viewer -y {param_upx}")