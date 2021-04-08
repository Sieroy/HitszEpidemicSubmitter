import requests
import re
from urllib.parse import parse_qs as urldecode
from json import JSONEncoder
from time import sleep

json_encoder = JSONEncoder()

# 请确保使用期见其他地方的HIT学工账号已经退出

login_param = {
    'username': '',  # 学号
    'password': '',  # 校园认证密码
    'rememberMe': 'on',
    'lt': '',
    'execution': 'e1s1',
    '_eventId': 'submit',
    'vc_username': '',
    'vc_password': '' 
}

report = lambda mid: {'info': json_encoder.encode({
    "model": {
        "id": mid,
        "stzkm": "01",  # 身体状况，'01'-健康，'02'-异常
        "dqszd": "01",  # 当前所在地，'01'-国内，'02'-海外
        "hwgj": "",  # （海外填写）海外国家，海外党请自行确定填写内容，不要伪造
        "hwcs": "",  # （海外填写）海外城市
        "hwxxdz": "",  # （海外填写）海外详细地址
        "dqszdsheng": "440000",  # （国内填写）当前所在地省号，可以参考区号填前两位，剩下四位补零
        "dqszdshi": "440300",  # （国内填写）当前所在地市号，可以参考区号填前四位，剩下两位补零
        "dqszdqu": "440305",  # （国内填写）当前所在地区号，自行百度
        "gnxxdz": "平山一路哈工大（深圳）",  # 详细地址
        "dqztm": "01",  # 当前状态，'01'-在校住宿，'02'-在校隔离，'03'-事假，'04'-病假，'05'-在校走读，'07'-校外隔离，'99'-其他
        "dqztbz": "",  # 备注
        "brfsgktt": "0",  # 是否发烧干咳头疼，'0'-否，'1'-是
        "brzgtw": "36.5",  # 体温
        "brsfjy": "",  # （发烧干咳头痛时填写）是否就医，'0'-否，'1'-是
        "brjyyymc": "",  # （发烧干咳头痛并就医时填写）医院名称
        "brzdjlm": "",  #（发烧干咳头痛并就医时填写）诊断结论，'01'-疑似，'02'-确诊，'03'-无症状感染者，'99'-其他
        "brzdjlbz": "",  #（发烧干咳头痛并就医时填写）诊断结论备注
        "qtbgsx": "",  # （身体异常时填写）身体情况备注
        "sffwwhhb": "0",  # 是否毕业班学生，'0'-否，'1'-是
        "sftjwhjhb": "0",  # 是否途径高危地区，'0'-否，'1'-是
        "tcyhbwhrysfjc": "0",  # 是否与患者同乘交通工具，'0'-否，'1'-是
        "sftzrychbwhhl": "0",  # 同住人员有无来自高危地区，'0'-否，'1'-是
        "sfjdwhhbry": "0",  # 实习情况，'0'-不实习，'1'-实习住校，'2'-实习不住校
        "tcjtfs": "",  # （与患者同乘时填写）同乘交通方式，'01'-火车，'02'-飞机，'03'-长途汽车，'99'-自驾或其他
        "tchbcc": "",  # （与患者同乘火车飞机时填写）同乘航班/车次
        "tccx": "",  # （与患者同乘火车时填写）同乘车厢
        "tczwh": "",  # （与患者同乘火车时填写）座位号
        "tcjcms": "",  # （与患者同乘时填写）接触描述
        "gpsxx": "",  # 未知项目，盲猜GPS信息
        "sfjcqthbwhry": "0",  # 是否有其他接触情况，'0'-否，'1'-是
        "sfjcqthbwhrybz": "",  # （接触时填写）情况备注
        "tcjtfsbz":""  # （与患者一同自驾或其他时填写）交通方式备注
    }
})}

re_lt = re.compile('<input type="hidden" name="lt" value="(.+?)" />')

cookies = {}

header = { 
    'Host': 'xgsm.hitsz.edu.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': '',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}


# 红色入口界面
header['Referer'] = 'http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/xsHome'
res = requests.get('http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange', headers=header, cookies=cookies)
cookies['JSESSIONID'] = res.cookies.get('JSESSIONID')

# 认证并跳转至登陆页面
header['Referer'] = 'http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange'
res = requests.get('http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/shsj/common', cookies=cookies, headers=header)
cookies['JSESSIONID'] = res.cookies.get('JSESSIONID')
post_server = res.url
lt = re.search(re_lt, res.text).group(1)

# 保险起见，还是睡一秒吧
sleep(1)

# 登陆
login_param['lt'] = lt
header['Referer'] = post_server
res = requests.post(post_server, headers=header, data=login_param, cookies=cookies)
cookies['JSESSIONID'] = res.history[2].cookies.get('JSESSIONID')

# 保险起见，还是睡一秒吧
sleep(1)

# 上报
header['Referer'] = 'http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/xsHome'
res = requests.post('http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/xs/csh', headers=header, cookies=cookies)
res = requests.post('http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/xs/getYqxxList', headers=header, cookies=cookies)
newinfo = res.json()['module']['data'][0]
moid, zt = newinfo['id'], newinfo['zt']
header['Referer'] = f'http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/xs/editYqxx?id={moid}&zt={zt}'
res = requests.post('http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/xs/saveYqxx', headers=header, data=report(moid), cookies=cookies)

