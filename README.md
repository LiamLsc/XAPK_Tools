# 📱 XAPK 工具
![QQ20260127-092038.png](https://youke.xn--y7xa690gmna.cn/s1/2026/01/27/6978130c39894.webp)
<p align="center">
  <b>轻松打包和安装XAPK文件的桌面应用程序</b>
</p>

---

## ✨ 功能特性

- 📦 **打包XAPK**: 将APK文件和OBB数据包合并成XAPK格式
- 🚀 **一键安装**: 直接安装APK和OBB到连接的Android设备
- 🔍 **应用信息**: 显示APK的应用名称、包名、版本等详细信息
- 📁 **目录管理**: 选择输出目录，自定义保存位置
- 📊 **实时进度**: 显示操作进度和状态信息

## 🛠️ 技术栈

- **Python**: 后端逻辑处理
- **Eel**: Python与Web前端的桥接框架
- **HTML/CSS/JavaScript**: 用户界面
- **ADB**: Android设备通信

## 📋 依赖库

- `eel`
- `pyaxmlparser`
- `tkinter`
- `subprocess`
- `base64`

## 🚀 使用方法

### 方法一：直接使用（推荐）

1. 从GitHub发布页面下载预编译的 `XAPK_Tool.exe` 文件
2. 双击运行即可使用，无需安装任何依赖

### 方法二：源码运行

1. 确保系统中安装了Python 3.x
2. 下载源代码文件
3. 安装依赖: `pip install eel pyaxmlparser`
4. 运行应用: `python main.py`
5. 在浏览器中自动打开应用界面

### 使用步骤

1. 选择APK文件和OBB文件
2. 选择输出目录（可选）
3. 点击"打包XAPK"或"一键安装"
4. 使用“一键安装”功能需要打开安卓设备的开发者选项--USB调试模式，确保设备已连接到计算机。
5. 观察进度和结果

## 📦 安装要求

- Python 3.6+（如果使用源码运行）
- Android SDK平台工具（用于ADB）
- 启用了USB调试的Android设备

## 🤝 贡献

欢迎提交Issue和Pull Request来帮助改进项目！

## 📄 许可证

此项目采用 MIT 许可证 - 查看 [LICENSE](./LICENSE) 文件了解详情