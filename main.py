import eel, os, json, zipfile, tkinter as tk, base64, sys, subprocess, time
from tkinter import filedialog
from pyaxmlparser import APK

# --- 核心：全绿色环境初始化 ---
def resource_path(relative_path):
    """获取程序运行时的临时路径（支持开发环境和打包环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 自动定位 ADB 路径（确保程序能找到打进去的 ADB ）
ADB_EXE = resource_path("adb/adb.exe")

# 修复 pyaxmlparser 资源路径
if getattr(sys, 'frozen', False):
    os.environ['PYAXMLPARSER_RESOURCES'] = os.path.join(sys._MEIPASS, 'pyaxmlparser', 'resources')

eel.init('web')

def get_adb_path():
    """动态获取 ADB 路径：优先找打包后的临时目录，找不到则找当前目录"""
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, "adb", "adb.exe")
    else:
        path = os.path.join(os.path.abspath("."), "adb", "adb.exe")
    return f'"{path}"' # 加引号防止空格路径报错

@eel.expose
def check_adb_connection():
    """供前端调用的设备检测函数"""
    adb = get_adb_path()
    si = subprocess.STARTUPINFO(); si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        # 检查设备列表，不再强制重启服务以避免卡顿
        res = subprocess.run(f"{adb} devices", capture_output=True, text=True, startupinfo=si, shell=True)
        lines = [l for l in res.stdout.strip().split('\n') if l.strip()]
        
        if len(lines) > 1:
            # 检查是否有在线设备
            for line in lines[1:]:
                if 'device' in line and not line.startswith('offline'):
                    device_id = line.split('\t')[0]
                    return {"status": "success", "msg": f"已连接: {device_id}"}
        return {"status": "error", "msg": "未发现设备"}
    except:
        return {"status": "error", "msg": "ADB引擎启动失败"}
    
def get_clean_info(apk_path):
    """安全解析 APK 信息"""
    try:
        apk = APK(apk_path)
        pkg = apk.package
        # 深度保底：解析名称
        try:
            name = apk.get_app_display_name()
            if not name or name.startswith('@'): name = apk.application_label
        except: name = None
        
        if not name or name == "None":
            name = pkg.split('.')[-1].capitalize()

        icon_b64 = ""
        try:
            icon_data = apk.get_file(apk.get_app_icon())
            icon_b64 = base64.b64encode(icon_data).decode('utf-8')
        except: pass

        return {
            "name": name, "pkg": pkg, "verName": apk.version_name,
            "verCode": str(apk.version_code), "min": apk.get_min_sdk_version(),
            "size": f"{os.path.getsize(apk_path)/(1024*1024):.1f}MB",
            "icon": icon_b64, "perms": len(apk.get_permissions())
        }
    except: return None

@eel.expose
def select_file(ext):
    root = tk.Tk(); root.withdraw(); root.wm_attributes('-topmost', 1)
    path = filedialog.askopenfilename(filetypes=[("Files", f"*{ext}")])
    root.destroy()
    return path

@eel.expose
def select_dir():
    root = tk.Tk(); root.withdraw(); root.wm_attributes('-topmost', 1)
    path = filedialog.askdirectory(); root.destroy()
    return path

@eel.expose
def get_details(apk_path):
    try:
        apk = APK(apk_path)
        pkg = apk.package
        # 深度名称提取
        try:
            name = apk.get_app_display_name()
            if not name or name.startswith('@'): name = apk.application_label
        except: name = None
        if not name or name == "None": name = pkg.split('.')[-1].capitalize()

        icon_b64 = ""
        try:
            icon_data = apk.get_file(apk.get_app_icon())
            icon_b64 = base64.b64encode(icon_data).decode('utf-8')
        except: pass

        return {
            "name": name, "pkg": pkg, "verName": apk.version_name,
            "verCode": str(apk.version_code), "min": apk.get_min_sdk_version(),
            "size": f"{os.path.getsize(apk_path)/(1024*1024):.1f}MB",
            "icon": icon_b64, "perms": len(apk.get_permissions())
        }
    except: return None

@eel.expose
def process_xapk(apk_path, obb_path, out_dir):
    try:
        info = get_details(apk_path)
        if not out_dir: out_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        out_path = os.path.join(out_dir, f"{info['name']}_v{info['verCode']}.xapk")
        
        # 模拟进度
        eel.update_status(10, "正在准备打包...")()
        time.sleep(0.5)
        
        eel.update_status(30, "正在打包 APK 文件...")()
        time.sleep(0.5)
        
        with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as x:
            x.write(apk_path, f"{info['pkg']}.apk")
            
            eel.update_status(60, "正在压入 OBB 数据包...")()
            time.sleep(0.5)
            x.write(obb_path, f"Android/obb/{info['pkg']}/main.{info['verCode']}.{info['pkg']}.obb")
            
            eel.update_status(80, "正在写入清单文件...")()
            time.sleep(0.3)
            x.writestr("manifest.json", json.dumps({"xapk_version":1,"package_name":info['pkg'],"name":info['name'],"version_code":int(info['verCode']),"install_type":"full"}, indent=4))
        
        eel.update_status(100, "打包完成！")()
        time.sleep(0.2)
        return {"status":"success", "msg":"XAPK打包成功！"}
    except Exception as e: 
        eel.update_status(100, "打包失败")()
        return {"status":"error", "msg":str(e)}

@eel.expose
def fast_install(apk_path, obb_path):
    try:
        info = get_details(apk_path)
        adb = get_adb_path()
        si = subprocess.STARTUPINFO(); si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        # 1. 再次确认连接
        eel.update_status(10, "正在连接手机...")()
        check = subprocess.run(f"{adb} devices", capture_output=True, text=True, startupinfo=si, shell=True)
        
        # 修复设备检测逻辑
        lines = [l for l in check.stdout.strip().split('\n') if l.strip()]
        device_connected = False
        if len(lines) > 1:
            for line in lines[1:]:
                if 'device' in line and not line.startswith('offline'):
                    device_connected = True
                    break
        
        if not device_connected:
            return {"status":"error", "msg":"连接中断，请重新插拔"}

        # 2. 安装 APK
        eel.update_status(30, "正在发送 APK (请在手机上点击允许安装)...")()
        # 使用 -t 允许安装测试版，-r 覆盖安装
        subprocess.run(f"{adb} install -t -r \"{apk_path}\"", startupinfo=si, shell=True, check=True)
        
        # 3. 创建 OBB 路径
        eel.update_status(60, "同步 OBB 目录...")()
        remote_dir = f"/sdcard/Android/obb/{info['pkg']}/"
        subprocess.run(f"{adb} shell mkdir -p {remote_dir}", startupinfo=si, shell=True, check=True)
        
        # 4. 推送 OBB
        eel.update_status(80, "正在传输数据包 (请勿断开)...")()
        remote_obb = f"{remote_dir}main.{info['verCode']}.{info['pkg']}.obb"
        subprocess.run(f"{adb} push \"{obb_path}\" {remote_obb}", startupinfo=si, shell=True, check=True)
        
        eel.update_status(100, "安装成功！")()
        return {"status":"success", "msg":"恭喜！应用及数据包已安装。"}
    except Exception as e:
        return {"status":"error", "msg": f"安装失败: {str(e)}"}

eel.start('index.html', size=(800, 620), mode='default')