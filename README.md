# HitszEpidemicSubmitter

疫情上报每天都要搞，如果漏报还要被辅导员贴脸输出。是不是很不爽？反正我是被恶心到了。但毕竟疫情嘛，站在校方立场上又确实马虎不得。所以我写了个这玩意儿。

## 环境配置

脚本运行需要Python3.6及以上的环境，此外对于Windows用户，还要安装`requests`包：

```bash
python3 -m pip install requests
```
（或者适用于你电脑配置的其他指令）

## 运行前的准备

运行前，需要在脚本内填写教职工号/学号以及统一身份认证密码，同时也别忘了修改下面的上报信息（相关信息都已详细注释）。

具体来说有这些：

- [第12、13行的账号密码](https://github.com/Sieroy/HitszEpidemicSubmitter/blob/20c2ac53259b123f7e5d5e2199a300b1dbf6fa7b/HITreportor.py#L12)
  
  记得以如下格式填写正确的学号和密码。如果漏填或误填，上报将失败。
  ```python
  login_param = {
    'username': '180310101',  # 学号
    'password': 'ThisIsYourPassword,Daze~',  # 校园认证密码
    # ...
  }
  ```
- [第25行到第56行的上报信息](https://github.com/Sieroy/HitszEpidemicSubmitter/blob/20c2ac53259b123f7e5d5e2199a300b1dbf6fa7b/HITreportor.py#L25)
  
  其中已经填好默认值，如果有需要更改的信息，请参照所在行注释来填写。比如，如果你想修改体温为37.3℃，需要更改[体温信息所在行](https://github.com/Sieroy/HitszEpidemicSubmitter/blob/20c2ac53259b123f7e5d5e2199a300b1dbf6fa7b/HITreportor.py#L37)为`"brzgtw": "37.3",`。

## 自动上报

如果想实现每日自动上报，对于Linux用户，直接上`cron`即可；对于Windows用户，可以[设置任务计划](https://jingyan.baidu.com/article/9080802200cc15fd91c80fcf.html)来实现自动化。如果保证不了实时开机的话，可以在校园网内通过我的[服务器](http://10.249.77.65/app/epidemic.html)来自动执行，但要提供你的学号密码哦~~ （树莓派服务器正在降温中，暂时用不了呜呜呜）

## 最后

**如果你的身体真的有不良状况，请停止脚本运行并通过正规途径如实上报～（求生欲**
