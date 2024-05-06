
// 获取滑块元素
const slider = document.getElementById("slider");
// 获取用于显示滑块值的元素
const sliderValueElement = document.getElementById("sliderValue");

// 显示滑块当前值
sliderValueElement.textContent = slider.value;

// 添加事件监听器，当滑块值改变时更新显示的值
slider.addEventListener("input", () => {
    sliderValueElement.textContent = slider.value;
    var data = {
        type: 'change_sleep_time',
        new_sleep_time: 11 - parseInt(slider.value)
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
                throw new Error('sent failed');
            }
        })
        .then(data => {

        })
        .catch(error => {
            console.error('Login error:', error.message);
        });
});



function check_model_list() {
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
        type: 'check_model_list',
        username: firstCookieName
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
                throw new Error('sent failed');
            }
        })
        .then(data => {
            // 找到并获取 <form> 元素
            var radioForm = document.getElementById('radioForm');

            // 清空 <form> 元素中的所有子元素
            while (radioForm.firstChild) {
                radioForm.removeChild(radioForm.firstChild);
            }

            for (var optionCount = 0; optionCount < parseInt(data.len); optionCount++) {
                var radioForm = document.getElementById('radioForm');
                var newRadioButton = document.createElement('input');
                newRadioButton.type = 'radio';
                newRadioButton.name = 'models'; // 与其他单选按钮相同的 name 属性

                // 创建一个新的标签
                var newLabel = document.createElement('label');
                newLabel.htmlFor = 'option' + optionCount;
                var label_name = 'name_' + (optionCount + 1);
                var modelName = data[label_name];
                newLabel.textContent = modelName[0];
                newRadioButton.value = modelName[0];


                // 检查模型名称是否包含 '_training'，如果是则禁用单选按钮
                if (modelName[0].includes('_training')) {

                    newRadioButton.setAttribute('disabled', 'disabled'); // 设置禁用属性
                    newRadioButton.removeAttribute('checked'); // 移除选中状态
                }
                // 将单选按钮和标签添加到表单中
                radioForm.appendChild(newRadioButton);
                radioForm.appendChild(newLabel);

                // 添加一个换行符
                radioForm.appendChild(document.createElement('br'));
            }



        })
        .catch(error => {
            console.error('Login error:', error.message);
        });
}