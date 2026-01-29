eel.expose(update_status);
function update_status(per, text) {
    document.getElementById('pBar').style.width = per + "%";
    document.getElementById('pText').innerText = text;
    document.getElementById('pPercent').innerText = per + "%";
}

// 自定义居中弹窗函数
function showAlert(message) {
    // 如果已有弹窗，则不重复创建
    if(document.querySelector('.custom-alert-overlay')) {
        return;
    }
    
    // 创建遮罩层
    const overlay = document.createElement('div');
    overlay.className = 'custom-alert-overlay';
    
    // 创建弹窗主体
    const alertBox = document.createElement('div');
    alertBox.className = 'custom-alert-box';
    
    // 创建消息内容
    const msgElement = document.createElement('div');
    msgElement.className = 'custom-alert-message';
    msgElement.textContent = message;
    
    // 创建确定按钮
    const button = document.createElement('button');
    button.className = 'custom-alert-button';
    button.textContent = '确定';
    button.onclick = function() {
        document.body.removeChild(overlay);
    };
    
    // 组装弹窗
    alertBox.appendChild(msgElement);
    alertBox.appendChild(button);
    overlay.appendChild(alertBox);
    
    // 显示弹窗
    document.body.appendChild(overlay);
    
    // 点击遮罩关闭弹窗
    overlay.addEventListener('click', function(e) {
        if(e.target === overlay) {
            document.body.removeChild(overlay);
        }
    });
}

async function selAPK() {
    let p = await eel.select_file('.apk')();
    if(p) {
        document.getElementById('apkP').value = p;
        let d = await eel.get_details(p)();
        if(d) {
            document.getElementById('icon').src = "data:image/png;base64,"+d.icon;
            document.getElementById('aName').innerText = d.name;
            document.getElementById('dPkg').innerText = d.pkg;
            document.getElementById('dVer').innerText = d.verName;
            document.getElementById('dSize').innerText = d.size;
            document.getElementById('dMin').innerText = d.min;
            document.getElementById('dPerm').innerText = d.perms;
        }
    }
}

async function selFile(ex) {
    let p = await eel.select_file(ex)();
    if(p) document.getElementById('obbP').value = p;
}

async function selDir() {
    let p = await eel.select_dir()();
    if(p) document.getElementById('outP').value = p;
}

async function doPack() {
    const a = document.getElementById('apkP').value;
    const o = document.getElementById('obbP').value;
    const out = document.getElementById('outP').value;
    if(!a || !o) return showAlert("请选齐文件");
    document.getElementById('b1').disabled = true;
    let r = await eel.process_xapk(a, o, out)();
    showAlert(r.msg);
    document.getElementById('b1').disabled = false;
}

async function doInst() {
    const a = document.getElementById('apkP').value;
    const o = document.getElementById('obbP').value;
    if(!a || !o) return showAlert("请选齐文件");
    document.getElementById('b2').disabled = true;
    let r = await eel.fast_install(a, o)();
    showAlert(r.msg);
    document.getElementById('b2').disabled = false;
}

async function checkDev() {
    let res = await eel.check_adb_connection()();
    let el = document.getElementById('devStatus');
    el.innerText = res.msg;
    if(res.status === "success") {
        el.classList.add('dev-online');
    } else {
        el.classList.remove('dev-online');
    }
}

// 页面加载后不立即检测设备，而是显示提示信息
document.addEventListener('DOMContentLoaded', function() {
    // 可以在此处添加其他初始化代码
    console.log("XAPK 工具 已就绪");
});