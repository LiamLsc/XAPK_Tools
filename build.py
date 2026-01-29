import PyInstaller.__main__
import os
import pyaxmlparser

# 自动获取 pyaxmlparser 资源路径
pyaxml_res = os.path.join(os.path.dirname(pyaxmlparser.__file__), 'resources')

PyInstaller.__main__.run([
    'main.py',
    '--onefile',               # 单文件模式
    '--noconsole',             # 无黑窗口
    '--name=XAPK_Tool',        # 软件名
    '--add-data=web;web',      # 网页资源
    f'--add-data={pyaxml_res};pyaxmlparser/resources', # APK解析资源
    '--add-data=adb;adb',      # ADB相关文件
    '--icon=icon.ico'              
])

print("打包完成！请在 dist 文件夹领取你的全集成绿色版软件。")