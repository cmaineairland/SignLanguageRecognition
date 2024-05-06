/*
 * @Date: 2024-03-19 20:47:35
 * @LastEditors: Qianshanju
 * @E-mail: z1939784351@gmail.com
 * @LastEditTime: 2024-05-04 15:38:39
 * @FilePath: \Graduation_Project\核心代码\static\upload.js
 */
const selectButton = document.getElementById('fileInputButton');
const fileInput = document.getElementById('fileInput');


function open_model_window() {
    var modal = document.getElementById("myModal");
    modal.style.display = "block";
}

function containsChinese(fileName) {
    // 匹配中文字符的正则表达式
    var chineseRegex = /[\u4e00-\u9fa5]/;
    return chineseRegex.test(fileName);
}

selectButton.addEventListener('click', function () {


});


fileInput.addEventListener('change', function () {
    var formData = new FormData();
    var fileInput = document.getElementById('fileInput');
    // 确保用户选择了文件
    if (fileInput.files.length > 0) {
        var file = fileInput.files[0];
        var dotIndex = file.name.indexOf(".");
        var afterDot = file.name.slice(dotIndex + 1);
        if (afterDot != 'zip') {
            alert('仅接受zip后缀文件');
            return 0;
        }
        if (containsChinese(file.name)) {
            alert('模型中不能含有中文！');
            return 0;
        }
        formData.append('file', file);
        // 使用 XMLHttpRequest 或 Fetch API 发送文件至后端
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload', true);

        // 获取所有的 cookie
        const cookies = document.cookie;

        // 解析 cookie 字符串，获取第一个 cookie 的名称
        function getFirstCookieName(cookieStr) {
            // 切割 cookie 字符串，获取第一个 cookie
            const cookiePairs = cookieStr.split('; ');

            // 如果有至少一个 cookie
            if (cookiePairs.length > 0) {
                // 获取第一个 cookie 的名称
                const firstCookiePair = cookiePairs[0];
                const firstCookieName = firstCookiePair.split('=')[0].trim(); // 提取 cookie 名称
                return firstCookieName;
            }

            // 如果没有任何 cookie，则返回空字符串或其他指定的默认值
            return '';
        }

        // 使用 getFirstCookieName 函数获取第一个 cookie 的名称
        const firstCookieName = getFirstCookieName(cookies);

        var data = {
            type: 'upload_file',
            username: firstCookieName,
            model_name: file.name,
        };

        fetch('/get_massage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Upload failed');
                }
            })
            .then(data => {
                check_model_list(firstCookieName)
            })
            .catch(error => {
                console.error('Upload error:', error.message);
            });

        xhr.onload = function () {
            if (xhr.status === 200) {
                console.log('文件上传成功');
                check_model_list()

            } else {
                console.error('文件上传失败');
                // 处理上传失败后的逻辑
            }
        };
        xhr.send(formData);
    } else {
        console.error('请先选择文件');
    }
});

function sure() {
    var modal = document.getElementById("myModal");
    fileInput.click();
    modal.style.display = "none";
}

function cancel() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}

