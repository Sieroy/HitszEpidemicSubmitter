import requests
import random
import re
from urllib.parse import parse_qs as urldecode
from json import JSONEncoder
from time import sleep

json_encoder = JSONEncoder()

# 请确保使用期间其他地方的HIT学工账号已经退出

login_param = {
    'username': '',  # 学号
    'password': '',  # 校园认证密码
    'rememberMe': 'on',
    'lt': '',
    'execution': 'e1s1',
    '_eventId': 'submit',
    'openid': '',
    'vc_username': '',
    'vc_password': ''
}

report = lambda my_token: {'info': json_encoder.encode({
    "model": {
        # 当前状态。
        # 01 - 在校（校内宿舍住）
        # 02 - 在校（校内隔离）
        # 03 - 事假
        # 04 - 病假
        # 05 - 在校（走读）
        # 07 - 校外隔离
        # 99 - 其他
        "dqzt":"01",

        # 所在地点GPS经纬，加了个正态分布噪声。
        # 注意：经度和纬度0.001的偏差约为现实中两道街宽的距离，想稳一稳的话可以手输定值。
        "gpsjd":str(113.9726+random.normalvariate(0, 0.000005))[:8],
        "gpswd":str(22.58838+random.normalvariate(0, 0.000005))[:8],

        # 所在地点。0 - 国外，1 - 国内
        "kzl1":"1",
        # 所在地为境外（上一项为 0）时填写以下四项：
            # 所在国家或地区
            "kzl2":"",
            # 所在国家城市
            "kzl3":"",
            # 具体地址
            "kzl4":"",
            # 近一个月内是否计划回国，填写对应数字：1 - 是，0 - 否
            "kzl5":"",

        # 所在地点。需要与上面GPS对应。
        "kzl6":"广东省",
        "kzl7":"深圳市",
        "kzl8":"南山区",
        "kzl9":"学苑大道3968号",
        "kzl10":"广东省深圳市南山区学苑大道3968号",

        # 如果所在地点与前一日有较大出入，需填写以下一至两项：
            # 原因
            # 0 - 探亲
            # 1 - 旅游
            # 2 - 回家
            # 3 - 因公出差/实习实训
            # 4 - 其他
            "kzl11":"",
            # 如果上一项原因为其他，那么需要填写下一项作为原因，否则不填
                # 地点变动原因
                "kzl12":"",

        # 当前所在地状态。0 - 低风险，1 - 中风险，2 - 高风险
        "kzl13":"0",
        # 如果上一项为中风险或高风险（1或2），那么需要填写下面一项
            # 所处街道社区名称
            "kzl14":"",

        # 当日是否途径中高风险地区。1 - 是，0 - 否
        "kzl15":"0",
        # 如果上一项为是（1），那么需要填写下面一项：
            # 所经中高风险街道社区名称
            "kzl16":"",

        # 今日体温情况。1 - ≥ 37.3℃，0 - < 37.3℃
        "kzl17":"1",

        # 今日是否出现不适（单选0，或多选1234，每个选项后加分号;）。
        # 0 - 无不适
        # 1 - 乏力
        # 2 - 干咳
        # 3 - 呼吸困难
        # 4 - 其他
        "kzl18":"0;",
        # 如果上一项填写了不适情况（1、2、3或4），那么填写下面几项：
            # 是否就诊。1 - 是，0 - 否
            "kzl19":"",
            # 如果上一项为是（1），那么填写以下一项，否则填写其后一至二项：
                # 诊断结果。0 - 疑似感染，1 - 确诊感染，2 - 其他。
                # 注意，填写其他时，请自行在 "kzl34" 字段填写其他确诊情况
                "kzl20":"",
                # 自行采取措施。0 - 已服药无异常，1 - 未服药无异常，2 - 其他
                "kzl21":"",
                # 如果上一项选择了其他（2），需填写下面一项
                    # 情况内容
                    "kzl22":"",

        # 当前健康状况。0 - 正常，1 - 新冠无症状感染者，2 - 新冠确诊
        "kzl23":"0",

        # 当前是否处于隔离期。1 - 是，0 - 否
        "kzl24":"0",
        # 如果上一项填写了是（1），那么填写下面三项：
            # 隔离场所。0 - 定点医院，1 - 集中隔离点，2 - 居家隔离
            "kzl25":"",
            # 隔离详细地点
            "kzl26":"",
            # 隔离开始时间。格式：yyyy-mm-dd，数字位数不足时不补零占位
            "kzl27":"",

        # 本人或周边是否与新冠患者有交集。1 - 是，0 - 否
        "kzl28":"0",
        # 如果上一项填写了是，那么填写下面两项
            # 是否与患者同乘航班、列车。1 - 是，0 - 否
            "kzl29":"",
            # 详细接触情况
            "kzl30":"",

        # 48小时内是否做过核酸检测。1 - 是，0 - 否。（抓包发现默认未填）
        "kzl31":"",

        # 疫苗接种情况。0 - 未接种，1 - 部分剂次接种，2 - 全部剂次接种
        "kzl32":"2",

        # 其他信息。默认不填。
        "kzl33":"",

        # 如果在上面填写了身体不适，且已确诊为其他情况，填写下面一项（格式不对劲，推荐通过学工系统手动填写）
        "kzl34":{},

        # 以下保留即可
        "kzl38":"广东省",
        "kzl39":"深圳市",
        "kzl40":"南山区"
    },
	"token": my_token
})}

re_lt = re.compile('<input type="hidden" name="lt" value="(.+?)" />')

cookies_student = dict()
cookies_login = dict()

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'student.hitsz.edu.cn',
    'Referer': 'https://student.hitsz.edu.cn/xg_mobile/home',
    'sec-ch-ua': '"Microsoft Edge";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
}

# 自带返回的统一身份认证登陆系统界面
res = requests.get('https://student.hitsz.edu.cn/common/login/tyLogin?url=%2Fxg_mobile%2FxsMrsbNew%2Findex', headers=header, cookies=cookies_student, allow_redirects=False)
# 一次重定向
res = requests.get(res.next.url, headers=header, cookies=cookies_login, allow_redirects=False)
# 二次重定向
header['Host'] = 'sso.hitsz.edu.cn:7002'
res = requests.get(res.next.url, headers=header, cookies=cookies_login, allow_redirects=False)
cookies_login['JSESSIONID'] = res.cookies.get('JSESSIONID')
lt = re.search(re_lt, res.text).group(1)

# 安全起见，睡一秒
sleep(1)

# 登陆！
loginsplit = res.url.split('?')
loginsplit[0] += ';jsessionid='+cookies_login['JSESSIONID']
login_url = '?'.join(loginsplit)
login_param['lt'] = lt
cookies_login['j_username'] = login_param['username']
header['Origin'] = 'https://sso.hitsz.edu.cn:7002'
header['Referer'] = res.url
res = requests.post(login_url, headers=header, data=login_param, cookies=cookies_login, allow_redirects=False)
cookies_login['CASTGC'] = res.cookies.get('CASTGC')
# 一次重定向
header['Origin'] = 'student.hitsz.edu.cn'
header['Referer'] = 'https://sso.hitsz.edu.cn:7002/'
res = requests.get(res.next.url, headers=header, cookies=cookies_student, allow_redirects=False)
cookies_student['JSESSIONID'] = res.cookies.get('JSESSIONID')
# 二次重定向
res = requests.get(res.next.url, headers=header, cookies=cookies_student, allow_redirects=False)
# 四次重定向
res = requests.get(res.next.url, headers=header, cookies=cookies_student, allow_redirects=False)

# 要不这儿也睡一秒吧
sleep(1)

# 获取上报token
res = requests.post('https://student.hitsz.edu.cn/xg_common/getToken', cookies=cookies_student, allow_redirects=False)
token = res.text

# 上报
res = requests.post('https://student.hitsz.edu.cn/xg_mobile/xsMrsbNew/checkTodayData', cookies=cookies_student)
print(res.text)
if res.json().get('module') == '0':  # 如果今日已上报，则跳过
    res = requests.post('https://student.hitsz.edu.cn/xg_mobile/xsMrsbNew/save', data=report(token), cookies=cookies_student)
#'''
