/*
 * @Date: 2024-02-17 16:52:34
 * @LastEditors: Qianshanju
 * @E-mail: z1939784351@gmail.com
 * @LastEditTime: 2024-05-04 11:41:05
 * @FilePath: \Graduation_Project\核心代码\static\script.js
 */
function redirectToPage(url) {
    // 替换成目标页面的URL
    window.location.href = url;
}

// setInterval(() => {
//     wf.click()
// }, 600);
function get_char() {
    var myselect = document.getElementById("get_reference");
    var index = myselect.value;
    var url = "/Select_reference_image?select=" + index;
    // 创建一个XMLHttpRequest对象
    var xhr = new XMLHttpRequest();
    // 设置请求方法和URL
    xhr.open('GET', url, true);
    // 监听请求完成事件
    xhr.onload = function () {
        if (xhr.status === 200) {
            // 获取响应内容
            var responseContent = xhr.responseText;
            // 在控制台打印响应内容
            document.getElementById('reference_image').src = "data:;base64," + responseContent;

        }
        else {
            alert("模型中不存在该字符，请检查输入")
        }
    };
    // 发送请求
    xhr.send();
}
function update() {
    // 创建一个XMLHttpRequest对象
    var xhr = new XMLHttpRequest();
    // 设置请求方法和URL
    xhr.open('GET', '/sentence', true);
    // 监听请求完成事件
    xhr.onload = function () {
        if (xhr.status === 200) {
            // 获取响应内容
            var responseContent = xhr.responseText;
            // 在控制台打印响应内容
            document.getElementById('output').innerText = responseContent;

        }
    };
    // 发送请求
    xhr.send();
    const sliderValueElement = document.getElementById("sliderValue");
    var delay = (11 - parseInt(sliderValueElement.textContent)) * 100;
    setTimeout(update, delay);
}
setTimeout(update, 15000);//要想重新获取sentence内容则解除注释

function check_cookie() {
    const cookies = document.cookie;
    const currentPathname = window.location.pathname;
    if (cookies == "" && currentPathname != "/log_in" && currentPathname != "/create_account") {
        window.location.href = '/log_in';
    }

}

