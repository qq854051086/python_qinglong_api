### Python 青龙面板api 的封装
### 如何使用：
+ 安装依赖：`pip install -r requirements.txt`
+ 去青龙面板设定应用：
```text
路径：系统设置--应用设置--新建应用
权限根据自己的情况选择，测试本脚本需要勾选'定时任务'
```
+ 按照这个格式填写你的青龙面板信息：
```text
'{"host":"192.168.0.2:5700","ClientID":"v********qZ_s","ClientSecret":"Ilh**********h"}'
```
+ 然后替换main.py中 142行的值
+ 运行`python3 main.py`

### 如何完成其他需求业务。如修改环境变量：
+ 你可以实现对哪些功能的API访问：
  ```text
    参考：https://qinglong.ukenn.top/
    ```
+ 例如按照`run_task`方法的写法，你需要知道请求的`url`、`请求方式`、`请求体(json,特定的方法下可能不需要)`

+ url 要注意，在`https://qinglong.ukenn.top`这里展示的地址前要加`/open/`，例如：`/open/crons/run`
  
+ 然后通过class内定义的四种方式去发起请求。