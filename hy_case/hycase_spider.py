# -*- coding:utf-8 -*-
import os
import sys
import django

import time
import requests
import re
import hashlib

# 脚本连接django models
# 系统路径
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
# 连接django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hylg_web.settings")
django.setup()
# 导入models
from hy_case.models import CaseData,Customer

# 登录账号
username = "LIUJIANWEN"
password = "b78e222571294fb62c0e3518809ebdb3"
# md5 salt
salt = "1#2$3%4(5)6@7!poeeww$3%4(5)djjkkldss"
# 查询起止日期
startdate = "20100101"
enddate = "20151110" #(time.strftime("%Y%m%d"), time.localtime())[0]

# 运输数据修正
def trans_repair(trans):
    trans = "无" if (trans != "快递" and trans != "物流") else trans
    return  trans

# 涉案卷烟数量修正
def carton_repair(cartons):
    carton_count = 0
    for c in cartons:
        carton_count += float(c[39:-3])
    return '%.2f' % float(carton_count)

# 爬虫脚本
def start_spider():
    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }

    # 建立session
    session = requests.Session()

    # 获取隐藏验证码
    reCode = session.post("http://10.88.4.46/v6/rdmCode")
    code = reCode.text[7:11]

    # 密码
    # pwd = var_usr_pwd.get() + "{" + salt + "}"
    # m1 = hashlib.md5()
    # m1.update(pwd.encode("utf-8"))
    # password = m1.hexdigest()

    # 登录开始
    check_url = "http://10.88.4.46/v6/j_bsp_security_check/"
    check_data = {
        "j_username": username,
        "j_password": password,
        "rdmCode": code
    }
    session.post(check_url, headers=headers, data=check_data)
    print("-----" + "登录验证" + "-----\n")

    # 访问主页
    get_home_url = "http://10.88.4.46/rm/home/rmhomepagesc.cmd?method=goHomePage"
    session.get(get_home_url, headers=headers)
    print("-----" + "请求首页访问" + "-----\n")

    # SSO跳转1
    sso_url = "http://10.88.4.46/v6/SAML2/POST/SSO"
    sso_data = {
        "RelayState": "http://10.88.4.146/rm/home/rmhomepagesc.cmd?method=goHomePage",
        "SAMLRequest": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c2FtbHA6QXV0aG5SZXF1ZXN0IHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIEFzc2VydGlvbkNvbnN1bWVyU2VydmljZVVSTD0iL3JtL1NBTUwyL1NQQXNzZXJ0aW9uQ29uc3VtZXIiIERlc3RpbmF0aW9uPSIvdjYvU0FNTDIvUE9TVC9TU08iIElkcEVudGl0eUlEPSJJRFAiIEZvcmNlQXV0aG49ImZhbHNlIiBJc3N1ZUluc3RhbnQ9IjIwMTkwNjMwIDEwOjU1OjEwIiBQcm90b2NvbEJpbmRpbmc9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpiaW5kaW5nczpIVFRQLVBPU1QiIGlzUGFzc2l2ZT0iZmFsc2UiIFZlcnNpb249IjIuMCI+PHNhbWw6SXNzdWVyIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iID5WNlNQUklTPC9zYW1sOklzc3Vlcj4KPC9zYW1scDpBdXRoblJlcXVlc3Q+"
    }
    session.post(sso_url, headers=headers, data=sso_data)
    print("-----" + "SSO访问跳转" + "-----\n")

    # SSO跳转2
    sso_resp_url = "http://10.88.4.46/rm/SAML2/SPAssertionConsumer"
    sso_resp_data = {
        "RelayState": "http://10.88.4.146/rm/home/rmhomepagesc.cmd?method=goHomePage",
        "SAMLRequest": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIERlc3RpbmF0aW9uPSIvcm0vU0FNTDIvU1BBc3NlcnRpb25Db25zdW1lciIgSXNzdWVJbnN0YW50PSIyMDE5MDYzMCAxMToxMDo0MiIgVmVyc2lvbj0iMi4wIj4KPHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSIwMTZiYTY1ZDA0NWM2ZDQ4IiBJc3N1ZUluc3RhbnQ9IjIwMTkwNjMwIDExOjEwOjQyIiBWZXJzaW9uPSIyLjAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+SURQPC9zYW1sOklzc3Vlcj4KPHNhbWw6U3ViamVjdCB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj48c2FtbDpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDplbnRpdHkiPkxJVUpJQU5XRU48L3NhbWw6TmFtZUlEPgo8c2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uIE1ldGhvZD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmNtOmJlYXJlciI+PHNhbWw6U3ViamVjdENvbmZpcm1hdGlvbkRhdGEgQWRkcmVzcz0iMTAuODkuMTI0LjQ3IiBOb3RPbk9yQWZ0ZXI9IjIwMTkwNjMwIDExOjE1OjQyIiBSZWNpcGllbnQ9Ii9ybS9TQU1MMi9TUEFzc2VydGlvbkNvbnN1bWVyIi8+Cjwvc2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uPjwvc2FtbDpTdWJqZWN0Pgo8c2FtbDpDb25kaXRpb25zIE5vdEJlZm9yZT0iMTU2MTg2NDI0MjI2OCIgTm90T25PckFmdGVyPSIyMDE5MDYzMCAxMToxNTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+PHNhbWxwOkF1ZGllbmNlUmVzdHJpY3Rpb24+CjxzYW1scDpBdWRpZW5jZT5WNlNQUklTPC9zYW1scDpBdWRpZW5jZT4KPC9zYW1scDpBdWRpZW5jZVJlc3RyaWN0aW9uPgo8L3NhbWw6Q29uZGl0aW9ucz48c2FtbDpBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMTkwNjMwIDExOjEwOjQyIiBTZXNzaW9uSW5kZXg9IlBRcEE2M0RBZW1NelZiTzZBeXpqbWlQIiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDE5MDYzMCAxMToxNTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+CjxzYW1sOlN1YmplY3RMb2NhbGl0eSBBZGRyZXNzPSIxMC44OS4xMjQuNDciLz4KPHNhbWw6QXV0aG5Db250ZXh0PjxzYW1sOkF1dGhuQ29udGV4dERlY2xSZWYgLz4KPC9zYW1sOkF1dGhuQ29udGV4dD4KPC9zYW1sOkF1dGhuU3RhdGVtZW50Pjwvc2FtbDpBc3NlcnRpb24+CjxzYW1scDpTdGF0dXMgeG1sbnM6c2FtbHA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCI+CjxzYW1scDpTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIC8+Cjwvc2FtbHA6U3RhdHVzPgo8L3NhbWxwOlJlc3BvbnNlPg==",
        "SAMLResponse": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIERlc3RpbmF0aW9uPSIvcm0vU0FNTDIvU1BBc3NlcnRpb25Db25zdW1lciIgSXNzdWVJbnN0YW50PSIyMDE5MDYzMCAxMToxMDo0MiIgVmVyc2lvbj0iMi4wIj4KPHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSIwMTZiYTY1ZDA0NWM2ZDQ4IiBJc3N1ZUluc3RhbnQ9IjIwMTkwNjMwIDExOjEwOjQyIiBWZXJzaW9uPSIyLjAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+SURQPC9zYW1sOklzc3Vlcj4KPHNhbWw6U3ViamVjdCB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj48c2FtbDpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDplbnRpdHkiPkxJVUpJQU5XRU48L3NhbWw6TmFtZUlEPgo8c2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uIE1ldGhvZD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmNtOmJlYXJlciI+PHNhbWw6U3ViamVjdENvbmZpcm1hdGlvbkRhdGEgQWRkcmVzcz0iMTAuODkuMTI0LjQ3IiBOb3RPbk9yQWZ0ZXI9IjIwMTkwNjMwIDExOjE1OjQyIiBSZWNpcGllbnQ9Ii9ybS9TQU1MMi9TUEFzc2VydGlvbkNvbnN1bWVyIi8+Cjwvc2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uPjwvc2FtbDpTdWJqZWN0Pgo8c2FtbDpDb25kaXRpb25zIE5vdEJlZm9yZT0iMTU2MTg2NDI0MjI2OCIgTm90T25PckFmdGVyPSIyMDE5MDYzMCAxMToxNTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+PHNhbWxwOkF1ZGllbmNlUmVzdHJpY3Rpb24+CjxzYW1scDpBdWRpZW5jZT5WNlNQUklTPC9zYW1scDpBdWRpZW5jZT4KPC9zYW1scDpBdWRpZW5jZVJlc3RyaWN0aW9uPgo8L3NhbWw6Q29uZGl0aW9ucz48c2FtbDpBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMTkwNjMwIDExOjEwOjQyIiBTZXNzaW9uSW5kZXg9IlBRcEE2M0RBZW1NelZiTzZBeXpqbWlQIiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDE5MDYzMCAxMToxNTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+CjxzYW1sOlN1YmplY3RMb2NhbGl0eSBBZGRyZXNzPSIxMC44OS4xMjQuNDciLz4KPHNhbWw6QXV0aG5Db250ZXh0PjxzYW1sOkF1dGhuQ29udGV4dERlY2xSZWYgLz4KPC9zYW1sOkF1dGhuQ29udGV4dD4KPC9zYW1sOkF1dGhuU3RhdGVtZW50Pjwvc2FtbDpBc3NlcnRpb24+CjxzYW1scDpTdGF0dXMgeG1sbnM6c2FtbHA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCI+CjxzYW1scDpTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIC8+Cjwvc2FtbHA6U3RhdHVzPgo8L3NhbWxwOlJlc3BvbnNlPg=="
    }
    session.post(sso_resp_url, headers=headers, data=sso_resp_data)
    print("-----" + "SSO回应跳转" + "-----\n")
    print("-----" + "获取到首页" + "-----\n")

    # 案件
    case_url = "http://10.88.4.46/cm/sthome/homecmd.cmd?method=goHomePage"
    session.get(case_url, headers=headers)
    print("-----" + "请求案件模板" + "-----\n")

    # SSO跳转1
    sso_data = {
        "RelayState": "http://10.88.4.146/cm/sthome/homecmd.cmd?method=goHomePage",
        "SAMLRequest": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c2FtbHA6QXV0aG5SZXF1ZXN0IHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIEFzc2VydGlvbkNvbnN1bWVyU2VydmljZVVSTD0iL2NtL1NBTUwyL1NQQXNzZXJ0aW9uQ29uc3VtZXIiIERlc3RpbmF0aW9uPSIvdjYvU0FNTDIvUE9TVC9TU08iIElkcEVudGl0eUlEPSJJRFAiIEZvcmNlQXV0aG49ImZhbHNlIiBJc3N1ZUluc3RhbnQ9IjIwMTkwNjMwIDExOjUzOjIxIiBQcm90b2NvbEJpbmRpbmc9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpiaW5kaW5nczpIVFRQLVBPU1QiIGlzUGFzc2l2ZT0iZmFsc2UiIFZlcnNpb249IjIuMCI+PHNhbWw6SXNzdWVyIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iID5WNlNQQ01DPC9zYW1sOklzc3Vlcj4KPC9zYW1scDpBdXRoblJlcXVlc3Q+"
    }
    session.post(sso_url, headers=headers, data=sso_data)
    print("-----" + "SSO跳转——案件" + "-----\n")

    # SSO跳转2
    sso_resp_url = "http://10.88.4.46/cm/SAML2/SPAssertionConsumer"
    sso_resp_data = {
        "RelayState": "http://10.88.4.146/cm/sthome/homecmd.cmd?method=goHomePage",
        "SAMLRequest": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIERlc3RpbmF0aW9uPSIvY20vU0FNTDIvU1BBc3NlcnRpb25Db25zdW1lciIgSXNzdWVJbnN0YW50PSIyMDE5MDYzMCAxMjowODo1MiIgVmVyc2lvbj0iMi4wIj4KPHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSIwMTZiYTY5MjQ2OTU2ZDg5IiBJc3N1ZUluc3RhbnQ9IjIwMTkwNjMwIDEyOjA4OjUyIiBWZXJzaW9uPSIyLjAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+SURQPC9zYW1sOklzc3Vlcj4KPHNhbWw6U3ViamVjdCB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj48c2FtbDpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDplbnRpdHkiPkxJVUpJQU5XRU48L3NhbWw6TmFtZUlEPgo8c2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uIE1ldGhvZD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmNtOmJlYXJlciI+PHNhbWw6U3ViamVjdENvbmZpcm1hdGlvbkRhdGEgQWRkcmVzcz0iMTAuODkuMTI0LjQ3IiBOb3RPbk9yQWZ0ZXI9IjIwMTkwNjMwIDEyOjEzOjUyIiBSZWNpcGllbnQ9Ii9jbS9TQU1MMi9TUEFzc2VydGlvbkNvbnN1bWVyIi8+Cjwvc2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uPjwvc2FtbDpTdWJqZWN0Pgo8c2FtbDpDb25kaXRpb25zIE5vdEJlZm9yZT0iMTU2MTg2NzczMjYyOSIgTm90T25PckFmdGVyPSIyMDE5MDYzMCAxMjoxMzo1MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+PHNhbWxwOkF1ZGllbmNlUmVzdHJpY3Rpb24+CjxzYW1scDpBdWRpZW5jZT5WNlNQQ01DPC9zYW1scDpBdWRpZW5jZT4KPC9zYW1scDpBdWRpZW5jZVJlc3RyaWN0aW9uPgo8L3NhbWw6Q29uZGl0aW9ucz48c2FtbDpBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMTkwNjMwIDEyOjA4OjUyIiBTZXNzaW9uSW5kZXg9IjNqNXJveGRIZDhTcDV1TlA2UDNfNlcwIiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDE5MDYzMCAxMjoxMzo1MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+CjxzYW1sOlN1YmplY3RMb2NhbGl0eSBBZGRyZXNzPSIxMC44OS4xMjQuNDciLz4KPHNhbWw6QXV0aG5Db250ZXh0PjxzYW1sOkF1dGhuQ29udGV4dERlY2xSZWYgLz4KPC9zYW1sOkF1dGhuQ29udGV4dD4KPC9zYW1sOkF1dGhuU3RhdGVtZW50Pjwvc2FtbDpBc3NlcnRpb24+CjxzYW1scDpTdGF0dXMgeG1sbnM6c2FtbHA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCI+CjxzYW1scDpTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIC8+Cjwvc2FtbHA6U3RhdHVzPgo8L3NhbWxwOlJlc3BvbnNlPg==",
        "SAMLResponse": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIERlc3RpbmF0aW9uPSIvY20vU0FNTDIvU1BBc3NlcnRpb25Db25zdW1lciIgSXNzdWVJbnN0YW50PSIyMDE5MDYzMCAxMjowODo1MiIgVmVyc2lvbj0iMi4wIj4KPHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSIwMTZiYTY5MjQ2OTU2ZDg5IiBJc3N1ZUluc3RhbnQ9IjIwMTkwNjMwIDEyOjA4OjUyIiBWZXJzaW9uPSIyLjAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+SURQPC9zYW1sOklzc3Vlcj4KPHNhbWw6U3ViamVjdCB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj48c2FtbDpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDplbnRpdHkiPkxJVUpJQU5XRU48L3NhbWw6TmFtZUlEPgo8c2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uIE1ldGhvZD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmNtOmJlYXJlciI+PHNhbWw6U3ViamVjdENvbmZpcm1hdGlvbkRhdGEgQWRkcmVzcz0iMTAuODkuMTI0LjQ3IiBOb3RPbk9yQWZ0ZXI9IjIwMTkwNjMwIDEyOjEzOjUyIiBSZWNpcGllbnQ9Ii9jbS9TQU1MMi9TUEFzc2VydGlvbkNvbnN1bWVyIi8+Cjwvc2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uPjwvc2FtbDpTdWJqZWN0Pgo8c2FtbDpDb25kaXRpb25zIE5vdEJlZm9yZT0iMTU2MTg2NzczMjYyOSIgTm90T25PckFmdGVyPSIyMDE5MDYzMCAxMjoxMzo1MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+PHNhbWxwOkF1ZGllbmNlUmVzdHJpY3Rpb24+CjxzYW1scDpBdWRpZW5jZT5WNlNQQ01DPC9zYW1scDpBdWRpZW5jZT4KPC9zYW1scDpBdWRpZW5jZVJlc3RyaWN0aW9uPgo8L3NhbWw6Q29uZGl0aW9ucz48c2FtbDpBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMTkwNjMwIDEyOjA4OjUyIiBTZXNzaW9uSW5kZXg9IjNqNXJveGRIZDhTcDV1TlA2UDNfNlcwIiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDE5MDYzMCAxMjoxMzo1MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+CjxzYW1sOlN1YmplY3RMb2NhbGl0eSBBZGRyZXNzPSIxMC44OS4xMjQuNDciLz4KPHNhbWw6QXV0aG5Db250ZXh0PjxzYW1sOkF1dGhuQ29udGV4dERlY2xSZWYgLz4KPC9zYW1sOkF1dGhuQ29udGV4dD4KPC9zYW1sOkF1dGhuU3RhdGVtZW50Pjwvc2FtbDpBc3NlcnRpb24+CjxzYW1scDpTdGF0dXMgeG1sbnM6c2FtbHA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCI+CjxzYW1scDpTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIC8+Cjwvc2FtbHA6U3RhdHVzPgo8L3NhbWxwOlJlc3BvbnNlPg=="
    }
    resp = session.post(sso_resp_url, headers=headers, data=sso_resp_data)
    print("-----" + "SSO回应跳转——案件" + "-----\n")
    print(resp.text)

    # 访问案件模板
    resp = session.get(case_url, headers=headers)
    print("-----" + "获取到案件模板" + "-----\n")
    print(resp.text)

    # 详细案件列表
    case_list_url = "http://10.88.4.46/cm/registed/case_checkinit.cmd?_pagesize=9999&_currentpageindex=1&_gridinfoprimarykey="
    case_list_data = {
        "occ_datebeginSearch": startdate,
        "occ_dateendSearch": enddate,
        "_flexigridpagesizeSearch": "10",
        "hiddenInputForTitle": "v6默认layout"
    }
    session.post(case_list_url, headers=headers, data=case_list_data)
    print("-----" + "请求案件列表" + "-----\n")

    # SSO跳转1
    sso_case = "http://10.88.4.46/v6/SAML2/POST/SSO"
    sso_caseData = {
        "RelayState": "http://10.88.4.146/cm/registed/case_checkinit.cmd?_pagesize=9999&_currentpageindex=1&_gridinfoprimarykey=",
        "SAMLRequest": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c2FtbHA6QXV0aG5SZXF1ZXN0IHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIEFzc2VydGlvbkNvbnN1bWVyU2VydmljZVVSTD0iL2NtL1NBTUwyL1NQQXNzZXJ0aW9uQ29uc3VtZXIiIERlc3RpbmF0aW9uPSIvdjYvU0FNTDIvUE9TVC9TU08iIElkcEVudGl0eUlEPSJJRFAiIEZvcmNlQXV0aG49ImZhbHNlIiBJc3N1ZUluc3RhbnQ9IjIwMTkwODIxIDExOjU3OjMxIiBQcm90b2NvbEJpbmRpbmc9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpiaW5kaW5nczpIVFRQLVBPU1QiIGlzUGFzc2l2ZT0iZmFsc2UiIFZlcnNpb249IjIuMCI+PHNhbWw6SXNzdWVyIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iID5WNlNQQ01DPC9zYW1sOklzc3Vlcj4KPC9zYW1scDpBdXRoblJlcXVlc3Q+"
    }
    session.post(sso_case, headers=headers, data=sso_caseData)
    print("-----" + "SSO跳转——案件" + "-----\n")

    # SSO跳转2
    sso_caseUrl = "http://10.88.4.46/cm/SAML2/SPAssertionConsumer"
    sso_caseData2 = {
        "RelayState": "http://10.88.4.146/cm/registed/case_checkinit.cmd?_pagesize=9999&_currentpageindex=1&_gridinfoprimarykey=",
        "SAMLRequest": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIERlc3RpbmF0aW9uPSIvY20vU0FNTDIvU1BBc3NlcnRpb25Db25zdW1lciIgSXNzdWVJbnN0YW50PSIyMDE5MDgyMSAxMjowNjo0MSIgVmVyc2lvbj0iMi4wIj4KPHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSIwMTZjYjI1YWY1NzUwYzZkIiBJc3N1ZUluc3RhbnQ9IjIwMTkwODIxIDEyOjA2OjQxIiBWZXJzaW9uPSIyLjAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+SURQPC9zYW1sOklzc3Vlcj4KPHNhbWw6U3ViamVjdCB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj48c2FtbDpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDplbnRpdHkiPkxJVUpJQU5XRU48L3NhbWw6TmFtZUlEPgo8c2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uIE1ldGhvZD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmNtOmJlYXJlciI+PHNhbWw6U3ViamVjdENvbmZpcm1hdGlvbkRhdGEgQWRkcmVzcz0iMTAuODkuMTI0LjkyIiBOb3RPbk9yQWZ0ZXI9IjIwMTkwODIxIDEyOjExOjQxIiBSZWNpcGllbnQ9Ii9jbS9TQU1MMi9TUEFzc2VydGlvbkNvbnN1bWVyIi8+Cjwvc2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uPjwvc2FtbDpTdWJqZWN0Pgo8c2FtbDpDb25kaXRpb25zIE5vdEJlZm9yZT0iMTU2NjM2MDQwMTI2OSIgTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMjoxMTo0MSIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+PHNhbWxwOkF1ZGllbmNlUmVzdHJpY3Rpb24+CjxzYW1scDpBdWRpZW5jZT5WNlNQQ01DPC9zYW1scDpBdWRpZW5jZT4KPC9zYW1scDpBdWRpZW5jZVJlc3RyaWN0aW9uPgo8L3NhbWw6Q29uZGl0aW9ucz48c2FtbDpBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMTkwODIxIDEyOjA2OjQxIiBTZXNzaW9uSW5kZXg9Ik1xMjlXOFkzSE5aVy1PUldyN2o4a1F5IiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMjoxMTo0MSIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+CjxzYW1sOlN1YmplY3RMb2NhbGl0eSBBZGRyZXNzPSIxMC44OS4xMjQuOTIiLz4KPHNhbWw6QXV0aG5Db250ZXh0PjxzYW1sOkF1dGhuQ29udGV4dERlY2xSZWYgLz4KPC9zYW1sOkF1dGhuQ29udGV4dD4KPC9zYW1sOkF1dGhuU3RhdGVtZW50Pjwvc2FtbDpBc3NlcnRpb24+CjxzYW1scDpTdGF0dXMgeG1sbnM6c2FtbHA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCI+CjxzYW1scDpTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIC8+Cjwvc2FtbHA6U3RhdHVzPgo8L3NhbWxwOlJlc3BvbnNlPg==",
        "SAMLResponse": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIERlc3RpbmF0aW9uPSIvY20vU0FNTDIvU1BBc3NlcnRpb25Db25zdW1lciIgSXNzdWVJbnN0YW50PSIyMDE5MDgyMSAxMjowNjo0MSIgVmVyc2lvbj0iMi4wIj4KPHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSIwMTZjYjI1YWY1NzUwYzZkIiBJc3N1ZUluc3RhbnQ9IjIwMTkwODIxIDEyOjA2OjQxIiBWZXJzaW9uPSIyLjAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+SURQPC9zYW1sOklzc3Vlcj4KPHNhbWw6U3ViamVjdCB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj48c2FtbDpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDplbnRpdHkiPkxJVUpJQU5XRU48L3NhbWw6TmFtZUlEPgo8c2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uIE1ldGhvZD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmNtOmJlYXJlciI+PHNhbWw6U3ViamVjdENvbmZpcm1hdGlvbkRhdGEgQWRkcmVzcz0iMTAuODkuMTI0LjkyIiBOb3RPbk9yQWZ0ZXI9IjIwMTkwODIxIDEyOjExOjQxIiBSZWNpcGllbnQ9Ii9jbS9TQU1MMi9TUEFzc2VydGlvbkNvbnN1bWVyIi8+Cjwvc2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uPjwvc2FtbDpTdWJqZWN0Pgo8c2FtbDpDb25kaXRpb25zIE5vdEJlZm9yZT0iMTU2NjM2MDQwMTI2OSIgTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMjoxMTo0MSIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+PHNhbWxwOkF1ZGllbmNlUmVzdHJpY3Rpb24+CjxzYW1scDpBdWRpZW5jZT5WNlNQQ01DPC9zYW1scDpBdWRpZW5jZT4KPC9zYW1scDpBdWRpZW5jZVJlc3RyaWN0aW9uPgo8L3NhbWw6Q29uZGl0aW9ucz48c2FtbDpBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMTkwODIxIDEyOjA2OjQxIiBTZXNzaW9uSW5kZXg9Ik1xMjlXOFkzSE5aVy1PUldyN2o4a1F5IiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMjoxMTo0MSIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+CjxzYW1sOlN1YmplY3RMb2NhbGl0eSBBZGRyZXNzPSIxMC44OS4xMjQuOTIiLz4KPHNhbWw6QXV0aG5Db250ZXh0PjxzYW1sOkF1dGhuQ29udGV4dERlY2xSZWYgLz4KPC9zYW1sOkF1dGhuQ29udGV4dD4KPC9zYW1sOkF1dGhuU3RhdGVtZW50Pjwvc2FtbDpBc3NlcnRpb24+CjxzYW1scDpTdGF0dXMgeG1sbnM6c2FtbHA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCI+CjxzYW1scDpTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIC8+Cjwvc2FtbHA6U3RhdHVzPgo8L3NhbWxwOlJlc3BvbnNlPg=="
    }
    resp = session.post(sso_caseUrl, headers=headers, data=sso_caseData2)
    print("-----" + "SSO回应跳转——案件" + "-----\n")

    # 获取案件编号
    keys = re.findall(r'20\d{8}\'\)\">华烟立', resp.text)
    for i in range(len(keys)):
        keys[i] = keys[i][0:10]

    for key in keys:
        # 详细案件详情
        case_detail_url = "http://10.88.4.46/cm/registed/cmcase.cmd?method=forDetail&primaryKeys=" + key

        # POST DATA一致
        resp = session.post(case_detail_url, headers=headers, data=case_list_data)
        print("-----" + "获取到案件详情" + "-----\n")

        # 案件名称，地址
        profiles = re.findall(r'class\=\"queryCaseTd\" colspan\=\"3\">.+', resp.text)
        for i in range(len(profiles)):
            profiles[i] = profiles[i][32:-1]

        # 当事人
        name_data = re.findall(r'当事人\:<\/label><\/td>\s+<td class=\"queryCaseTd\">\s+.+', resp.text)
        name = name_data[0][68:]
        if len(name) == 1:
            name = "无主"

        # 涉案卷烟数量
        cartons = re.findall(r'name=\"QUAN\" readonly=\"readonly\" value=\".+', resp.text)
        carton_count = carton_repair(cartons)

        # 案发日期
        date = re.findall(r'<td class=\"queryCaseTd\" >\d{8}', resp.text)[0][-8:]

        # 涉案金额
        price_data = re.findall(r'font-weight\: bold\;\">.+<\/label>', resp.text)
        price  = price_data[1][20:-8]

        # 案件详情
        detail = re.findall(r'<\/textarea> -->.+', resp.text)[0][15:]

        # 案件性质
        index = profiles[1].find(name)
        nature = profiles[1][index + len(name):]

        # 统计物流、快递
        trans = re.findall(r'运输渠道\:<\/label><\/td>\s+<td class=\"queryCaseTd\">.+', resp.text)[0][-3:-1]
        trans = trans_repair(trans)


        # 新增模型实例
        new_case = CaseData()
        new_case.case_key = key                             # primarykey
        new_case.case_person = name                         # 当事人
        new_case.case_nature = nature.strip()               # 案件性质
        new_case.case_address = profiles[2]                 # 案发地址
        new_case.case_date = date                           # 案发时间
        new_case.case_carton = carton_count                 # 涉案卷烟数量
        new_case.case_trans = trans                         # 物流快递
        new_case.case_price = '%.2f' % float(price)         # 涉案金额
        new_case.case_detail = detail.strip()               # 案件详情

        print("获取案件当事人:" + new_case.case_person)

        # 更新模型
        exist_list = CaseData.objects.filter(case_key=key)
        if len(exist_list) != 0:
            exist_case = exist_list[0]
            exist_case.case_person = new_case.case_person
            exist_case.case_nature = new_case.case_nature
            exist_case.case_address = new_case.case_address
            exist_case.case_date = new_case.case_date
            exist_case.case_carton = new_case.case_carton
            exist_case.case_trans = new_case.case_trans
            exist_case.case_price = new_case.case_price
            exist_case.case_detail = new_case.case_detail
            exist_case.save()
        else:
            new_case.save()


    # 抓取零售户信息

    # 详细零售户列表
    cust_list_url = "http://10.88.4.46/lm/cust/stcust_query_init.cmd?_pagesize=9999&_currentpageindex=1"
    cust_list_data = {
        "baseTypeAllSearch": 1,
        "sale_ScopeSearch": 1,
        "sale_ScopeSearch": 2,
        "sale_ScopeSearch": 3,
        "specialTypeAllSearch": 1,
        "special_TypeSearch": "00",
        "special_TypeSearch": "01",
        "special_TypeSearch": "02",
        "special_TypeSearch": "04",
        "special_TypeSearch": "05",
        "special_TypeSearch": "06",
        "special_TypeSearch": "90",
        "comCharaAllSearch": 1,
        "com_CharaSearch": "07",
        "com_CharaSearch": "01",
        "com_CharaSearch": "02",
        "com_CharaSearch": "03",
        "com_CharaSearch": "04",
        "com_CharaSearch": "05",
        "com_CharaSearch": "06",
        "com_CharaSearch": "08",
        "com_CharaSearch": "09",
        "com_CharaSearch": "10",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "hiddenInputForTitle": "v6默认layout"

    }
    resp = session.post(cust_list_url, headers=headers)
    print("-----" + "进入零售户列表" + "-----\n")

    sso_cust = {
        "RelayState": "http://10.88.4.146/lm/cust/stcust_query_init.cmd?_pagesize=9999&_currentpageindex=1",
        "SAMLRequest": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c2FtbHA6QXV0aG5SZXF1ZXN0IHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIEFzc2VydGlvbkNvbnN1bWVyU2VydmljZVVSTD0iL2xtL1NBTUwyL1NQQXNzZXJ0aW9uQ29uc3VtZXIiIERlc3RpbmF0aW9uPSIvdjYvU0FNTDIvUE9TVC9TU08iIElkcEVudGl0eUlEPSJJRFAiIEZvcmNlQXV0aG49ImZhbHNlIiBJc3N1ZUluc3RhbnQ9IjIwMTkwODIxIDEwOjI5OjMyIiBQcm90b2NvbEJpbmRpbmc9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpiaW5kaW5nczpIVFRQLVBPU1QiIGlzUGFzc2l2ZT0iZmFsc2UiIFZlcnNpb249IjIuMCI+PHNhbWw6SXNzdWVyIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iID5WNlNQTE1DPC9zYW1sOklzc3Vlcj4KPC9zYW1scDpBdXRoblJlcXVlc3Q+"
    }
    resp = session.post(sso_url, headers=headers, data=sso_cust)
    print("-----" + "SSO跳转——零售户" + "-----\n")

    sso_custUrl = "http://10.88.4.46/lm/SAML2/SPAssertionConsumer"
    sso_cust2 = {
        "RelayState": "http://10.88.4.146/lm/cust/stcust_query_init.cmd?_pagesize=9999&_currentpageindex=1",
        "SAMLRequest": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIERlc3RpbmF0aW9uPSIvbG0vU0FNTDIvU1BBc3NlcnRpb25Db25zdW1lciIgSXNzdWVJbnN0YW50PSIyMDE5MDgyMSAxMDo1MDo0MiIgVmVyc2lvbj0iMi4wIj4KPHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSIwMTZjYjIxNTY0YzQwMDM4IiBJc3N1ZUluc3RhbnQ9IjIwMTkwODIxIDEwOjUwOjQyIiBWZXJzaW9uPSIyLjAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+SURQPC9zYW1sOklzc3Vlcj4KPHNhbWw6U3ViamVjdCB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj48c2FtbDpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDplbnRpdHkiPkxJVUpJQU5XRU48L3NhbWw6TmFtZUlEPgo8c2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uIE1ldGhvZD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmNtOmJlYXJlciI+PHNhbWw6U3ViamVjdENvbmZpcm1hdGlvbkRhdGEgQWRkcmVzcz0iMTAuODkuMTI0LjkyIiBOb3RPbk9yQWZ0ZXI9IjIwMTkwODIxIDEwOjU1OjQyIiBSZWNpcGllbnQ9Ii9sbS9TQU1MMi9TUEFzc2VydGlvbkNvbnN1bWVyIi8+Cjwvc2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uPjwvc2FtbDpTdWJqZWN0Pgo8c2FtbDpDb25kaXRpb25zIE5vdEJlZm9yZT0iMTU2NjM1NTg0MjI0NCIgTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMDo1NTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+PHNhbWxwOkF1ZGllbmNlUmVzdHJpY3Rpb24+CjxzYW1scDpBdWRpZW5jZT5WNlNQTE1DPC9zYW1scDpBdWRpZW5jZT4KPC9zYW1scDpBdWRpZW5jZVJlc3RyaWN0aW9uPgo8L3NhbWw6Q29uZGl0aW9ucz48c2FtbDpBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMTkwODIxIDEwOjUwOjQyIiBTZXNzaW9uSW5kZXg9IkJfWGhfRTNGTVRiYUhfZHlBdVg3U01DIiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMDo1NTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+CjxzYW1sOlN1YmplY3RMb2NhbGl0eSBBZGRyZXNzPSIxMC44OS4xMjQuOTIiLz4KPHNhbWw6QXV0aG5Db250ZXh0PjxzYW1sOkF1dGhuQ29udGV4dERlY2xSZWYgLz4KPC9zYW1sOkF1dGhuQ29udGV4dD4KPC9zYW1sOkF1dGhuU3RhdGVtZW50Pjwvc2FtbDpBc3NlcnRpb24+CjxzYW1scDpTdGF0dXMgeG1sbnM6c2FtbHA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCI+CjxzYW1scDpTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIC8+Cjwvc2FtbHA6U3RhdHVzPgo8L3NhbWxwOlJlc3BvbnNlPg==",
        "SAMLResponse": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIERlc3RpbmF0aW9uPSIvbG0vU0FNTDIvU1BBc3NlcnRpb25Db25zdW1lciIgSXNzdWVJbnN0YW50PSIyMDE5MDgyMSAxMDo1MDo0MiIgVmVyc2lvbj0iMi4wIj4KPHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSIwMTZjYjIxNTY0YzQwMDM4IiBJc3N1ZUluc3RhbnQ9IjIwMTkwODIxIDEwOjUwOjQyIiBWZXJzaW9uPSIyLjAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+SURQPC9zYW1sOklzc3Vlcj4KPHNhbWw6U3ViamVjdCB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj48c2FtbDpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDplbnRpdHkiPkxJVUpJQU5XRU48L3NhbWw6TmFtZUlEPgo8c2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uIE1ldGhvZD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmNtOmJlYXJlciI+PHNhbWw6U3ViamVjdENvbmZpcm1hdGlvbkRhdGEgQWRkcmVzcz0iMTAuODkuMTI0LjkyIiBOb3RPbk9yQWZ0ZXI9IjIwMTkwODIxIDEwOjU1OjQyIiBSZWNpcGllbnQ9Ii9sbS9TQU1MMi9TUEFzc2VydGlvbkNvbnN1bWVyIi8+Cjwvc2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uPjwvc2FtbDpTdWJqZWN0Pgo8c2FtbDpDb25kaXRpb25zIE5vdEJlZm9yZT0iMTU2NjM1NTg0MjI0NCIgTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMDo1NTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+PHNhbWxwOkF1ZGllbmNlUmVzdHJpY3Rpb24+CjxzYW1scDpBdWRpZW5jZT5WNlNQTE1DPC9zYW1scDpBdWRpZW5jZT4KPC9zYW1scDpBdWRpZW5jZVJlc3RyaWN0aW9uPgo8L3NhbWw6Q29uZGl0aW9ucz48c2FtbDpBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMTkwODIxIDEwOjUwOjQyIiBTZXNzaW9uSW5kZXg9IkJfWGhfRTNGTVRiYUhfZHlBdVg3U01DIiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMDo1NTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+CjxzYW1sOlN1YmplY3RMb2NhbGl0eSBBZGRyZXNzPSIxMC44OS4xMjQuOTIiLz4KPHNhbWw6QXV0aG5Db250ZXh0PjxzYW1sOkF1dGhuQ29udGV4dERlY2xSZWYgLz4KPC9zYW1sOkF1dGhuQ29udGV4dD4KPC9zYW1sOkF1dGhuU3RhdGVtZW50Pjwvc2FtbDpBc3NlcnRpb24+CjxzYW1scDpTdGF0dXMgeG1sbnM6c2FtbHA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCI+CjxzYW1scDpTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIC8+Cjwvc2FtbHA6U3RhdHVzPgo8L3NhbWxwOlJlc3BvbnNlPg=="
    }
    resp = session.post(sso_custUrl, headers=headers, data=sso_cust2)
    print("-----" + "SSO跳转2——零售户" + "-----\n")


    # 获取零售户编号   511681100010"><a
    cust_keys = re.findall(r'511681\d{6}\">511681', resp.text)

    # 获取暂停户
    cust_list_url = "http://10.88.4.46/lm/cust/stcust_pause_query_init.cmd?_pagesize=99&_currentpageindex=1"
    cust_list_data = {
        "baseTypeAllSearch": 1,
        "sale_ScopeSearch": 1,
        "sale_ScopeSearch": 2,
        "sale_ScopeSearch": 3,
        "specialTypeAllSearch": 1,
        "special_TypeSearch": "00",
        "special_TypeSearch": "01",
        "special_TypeSearch": "02",
        "special_TypeSearch": "04",
        "special_TypeSearch": "05",
        "special_TypeSearch": "06",
        "special_TypeSearch": "90",
        "comCharaAllSearch": 1,
        "com_CharaSearch": "07",
        "com_CharaSearch": "01",
        "com_CharaSearch": "02",
        "com_CharaSearch": "03",
        "com_CharaSearch": "04",
        "com_CharaSearch": "05",
        "com_CharaSearch": "06",
        "com_CharaSearch": "08",
        "com_CharaSearch": "09",
        "com_CharaSearch": "10",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "STATUS": "02",
        "hiddenInputForTitle": "v6默认layout"

    }
    resp = session.post(cust_list_url, headers=headers)
    print("-----" + "进入零售户列表" + "-----\n")

    sso_cust = {
        "RelayState": "http://10.88.4.146/lm/cust/stcust_pause_query_init.cmd?_pagesize=99&_currentpageindex=1",
        "SAMLRequest": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c2FtbHA6QXV0aG5SZXF1ZXN0IHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIEFzc2VydGlvbkNvbnN1bWVyU2VydmljZVVSTD0iL2xtL1NBTUwyL1NQQXNzZXJ0aW9uQ29uc3VtZXIiIERlc3RpbmF0aW9uPSIvdjYvU0FNTDIvUE9TVC9TU08iIElkcEVudGl0eUlEPSJJRFAiIEZvcmNlQXV0aG49ImZhbHNlIiBJc3N1ZUluc3RhbnQ9IjIwMTkwODIxIDEwOjI5OjMyIiBQcm90b2NvbEJpbmRpbmc9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpiaW5kaW5nczpIVFRQLVBPU1QiIGlzUGFzc2l2ZT0iZmFsc2UiIFZlcnNpb249IjIuMCI+PHNhbWw6SXNzdWVyIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iID5WNlNQTE1DPC9zYW1sOklzc3Vlcj4KPC9zYW1scDpBdXRoblJlcXVlc3Q+"
    }
    resp = session.post(sso_url, headers=headers, data=sso_cust)
    print("-----" + "SSO跳转——零售户" + "-----\n")

    sso_custUrl = "http://10.88.4.46/lm/SAML2/SPAssertionConsumer"
    sso_cust2 = {
        "RelayState": "http://10.88.4.146/lm/cust/stcust_pause_query_init.cmd?_pagesize=9999&_currentpageindex=1",
        "SAMLRequest": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIERlc3RpbmF0aW9uPSIvbG0vU0FNTDIvU1BBc3NlcnRpb25Db25zdW1lciIgSXNzdWVJbnN0YW50PSIyMDE5MDgyMSAxMDo1MDo0MiIgVmVyc2lvbj0iMi4wIj4KPHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSIwMTZjYjIxNTY0YzQwMDM4IiBJc3N1ZUluc3RhbnQ9IjIwMTkwODIxIDEwOjUwOjQyIiBWZXJzaW9uPSIyLjAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+SURQPC9zYW1sOklzc3Vlcj4KPHNhbWw6U3ViamVjdCB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj48c2FtbDpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDplbnRpdHkiPkxJVUpJQU5XRU48L3NhbWw6TmFtZUlEPgo8c2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uIE1ldGhvZD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmNtOmJlYXJlciI+PHNhbWw6U3ViamVjdENvbmZpcm1hdGlvbkRhdGEgQWRkcmVzcz0iMTAuODkuMTI0LjkyIiBOb3RPbk9yQWZ0ZXI9IjIwMTkwODIxIDEwOjU1OjQyIiBSZWNpcGllbnQ9Ii9sbS9TQU1MMi9TUEFzc2VydGlvbkNvbnN1bWVyIi8+Cjwvc2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uPjwvc2FtbDpTdWJqZWN0Pgo8c2FtbDpDb25kaXRpb25zIE5vdEJlZm9yZT0iMTU2NjM1NTg0MjI0NCIgTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMDo1NTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+PHNhbWxwOkF1ZGllbmNlUmVzdHJpY3Rpb24+CjxzYW1scDpBdWRpZW5jZT5WNlNQTE1DPC9zYW1scDpBdWRpZW5jZT4KPC9zYW1scDpBdWRpZW5jZVJlc3RyaWN0aW9uPgo8L3NhbWw6Q29uZGl0aW9ucz48c2FtbDpBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMTkwODIxIDEwOjUwOjQyIiBTZXNzaW9uSW5kZXg9IkJfWGhfRTNGTVRiYUhfZHlBdVg3U01DIiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMDo1NTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+CjxzYW1sOlN1YmplY3RMb2NhbGl0eSBBZGRyZXNzPSIxMC44OS4xMjQuOTIiLz4KPHNhbWw6QXV0aG5Db250ZXh0PjxzYW1sOkF1dGhuQ29udGV4dERlY2xSZWYgLz4KPC9zYW1sOkF1dGhuQ29udGV4dD4KPC9zYW1sOkF1dGhuU3RhdGVtZW50Pjwvc2FtbDpBc3NlcnRpb24+CjxzYW1scDpTdGF0dXMgeG1sbnM6c2FtbHA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCI+CjxzYW1scDpTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIC8+Cjwvc2FtbHA6U3RhdHVzPgo8L3NhbWxwOlJlc3BvbnNlPg==",
        "SAMLResponse": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIERlc3RpbmF0aW9uPSIvbG0vU0FNTDIvU1BBc3NlcnRpb25Db25zdW1lciIgSXNzdWVJbnN0YW50PSIyMDE5MDgyMSAxMDo1MDo0MiIgVmVyc2lvbj0iMi4wIj4KPHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSIwMTZjYjIxNTY0YzQwMDM4IiBJc3N1ZUluc3RhbnQ9IjIwMTkwODIxIDEwOjUwOjQyIiBWZXJzaW9uPSIyLjAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSI+SURQPC9zYW1sOklzc3Vlcj4KPHNhbWw6U3ViamVjdCB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj48c2FtbDpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDplbnRpdHkiPkxJVUpJQU5XRU48L3NhbWw6TmFtZUlEPgo8c2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uIE1ldGhvZD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmNtOmJlYXJlciI+PHNhbWw6U3ViamVjdENvbmZpcm1hdGlvbkRhdGEgQWRkcmVzcz0iMTAuODkuMTI0LjkyIiBOb3RPbk9yQWZ0ZXI9IjIwMTkwODIxIDEwOjU1OjQyIiBSZWNpcGllbnQ9Ii9sbS9TQU1MMi9TUEFzc2VydGlvbkNvbnN1bWVyIi8+Cjwvc2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uPjwvc2FtbDpTdWJqZWN0Pgo8c2FtbDpDb25kaXRpb25zIE5vdEJlZm9yZT0iMTU2NjM1NTg0MjI0NCIgTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMDo1NTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+PHNhbWxwOkF1ZGllbmNlUmVzdHJpY3Rpb24+CjxzYW1scDpBdWRpZW5jZT5WNlNQTE1DPC9zYW1scDpBdWRpZW5jZT4KPC9zYW1scDpBdWRpZW5jZVJlc3RyaWN0aW9uPgo8L3NhbWw6Q29uZGl0aW9ucz48c2FtbDpBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMTkwODIxIDEwOjUwOjQyIiBTZXNzaW9uSW5kZXg9IkJfWGhfRTNGTVRiYUhfZHlBdVg3U01DIiBTZXNzaW9uTm90T25PckFmdGVyPSIyMDE5MDgyMSAxMDo1NTo0MiIgeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiI+CjxzYW1sOlN1YmplY3RMb2NhbGl0eSBBZGRyZXNzPSIxMC44OS4xMjQuOTIiLz4KPHNhbWw6QXV0aG5Db250ZXh0PjxzYW1sOkF1dGhuQ29udGV4dERlY2xSZWYgLz4KPC9zYW1sOkF1dGhuQ29udGV4dD4KPC9zYW1sOkF1dGhuU3RhdGVtZW50Pjwvc2FtbDpBc3NlcnRpb24+CjxzYW1scDpTdGF0dXMgeG1sbnM6c2FtbHA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCI+CjxzYW1scDpTdGF0dXNDb2RlIFZhbHVlPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6c3RhdHVzOlN1Y2Nlc3MiIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIC8+Cjwvc2FtbHA6U3RhdHVzPgo8L3NhbWxwOlJlc3BvbnNlPg=="
    }
    resp = session.post(sso_custUrl, headers=headers, data=sso_cust2)
    print("-----" + "SSO跳转2——零售户" + "-----\n")

    cust_keys_pause = re.findall(r'511681\d{6}\">511681', resp.text)
    cust_keys += cust_keys_pause

    Customer.objects.all().delete()

    for i in range(len(cust_keys)):
        cust_keys[i] = cust_keys[i][0:12]



    for cust_key in cust_keys:
        cust_detail_url = "http://10.88.4.46/rm/info/rminfolm.cmd?method=getLmCustMsg&custId=" + cust_key + "&comId=null&orgType=undefined"

        # POST
        resp = session.post(cust_detail_url, headers=headers)
        print("-----" + "获取到零售户百科" + "-----\n")

        zihao = re.findall(r'企业名称（字号）：<\/td><td colspan=\"3\">.+<\/td><\/tr><tr><td class=\"td-left\">法定', resp.text)
        if zihao:
            zihao = zihao[0][30:-36]
        else:
            zihao = "企业字号空缺"

        faren = re.findall(r'法定代表人（负责人）：<\/td><td>.+<\/td><td class=\"td-left\">身份证号', resp.text)
        if faren:
            faren = faren[0][20:-29]

            if faren[-1] == '\r':
                faren = faren[0:-1]
            if faren == "李玲玲":
                print(resp.text)

        else:
            faren = "法定代表人空缺"

        idnum = re.findall(r'身份证号：<\/td><td>.+<\/td><\/tr><tr class=\"active\"><td class=\"td-left\">经营地址', resp.text)
        if idnum:
            idnum = idnum[0][14:-53]
        else:
            idnum = "身份证号空缺"

        saleaddr = re.findall(r'经营地址：<\/td><td colspan=\"3\">.+</td></tr><tr><td class=\"td-left\">许可证号', resp.text)[0][26:-38]

        contman = re.findall(r'联系人：<\/td><td>.+<\/td><td class=\"td-left\">联系电话', resp.text)
        if contman:
            contman = contman[0][13:-32]
        else:
            contman = "联系人空缺"

        contphone = re.findall(r'联系电话：<\/td><td>.+<\/td><\/tr><tr class=\"active\"><td class=\"td-left\">身份证地址', resp.text)
        if contphone:
            contphone = contphone[0][14:-54]
        else:
            contphone = "联系电话空缺"

        idaddr = re.findall(r'身份证地址：<\/td><td colspan=\"3\">.+<\/td><\/tr><\/tr><tr><td class=\"td-left\">仓储地址', resp.text)
        if idaddr:
            idaddr = idaddr[0][27:-43]
        else:
            idaddr = "身份证地址空缺"

        special = \
        re.findall(r'特殊群体：<\/td><td>.+<\/td><\/tr><tr class=\"active\"><td class=\"td-left\">所属中队', resp.text)[0][14:-53]
        # district = re.findall(r'所属管区：</td><td>.+</td></tr><tr><td class="td-left">营业面积', resp.text)[0][14:-38]

        # 新增模型实例
        new_cust = Customer()
        new_cust.cust_key = cust_key         # primarykey
        new_cust.cust_zihao = zihao          # 企业字号
        new_cust.cust_faren = faren          # 法人
        new_cust.cust_type = "零售户"
        new_cust.cust_idnum = idnum          # 身份证号
        new_cust.cust_saleaddr = saleaddr    # 经营地址
        new_cust.cust_idaddr = idaddr        # 身份住址
        new_cust.cust_contman = contman      # 联系人
        new_cust.cust_contphone = contphone  # 联系电话
        new_cust.cust_special = special      # 普通/残疾人
        # new_cust.cust_district = district     # 片区

        print("获取零售户:" + new_cust.cust_faren)

        # new_cust.save()

        # 更新模型
        exist_custs = Customer.objects.filter(cust_key=cust_key)
        if len(exist_custs) != 0:
            exist_cust = exist_custs[0]
            exist_cust.cust_key = new_cust.cust_key
            exist_cust.cust_zihao = new_cust.cust_zihao
            exist_cust.cust_faren = new_cust.cust_faren
            exist_cust.cust_idnum = new_cust.cust_idnum
            exist_cust.cust_saleaddr = new_cust.cust_saleaddr
            exist_cust.cust_idaddr = new_cust.cust_idaddr
            exist_cust.cust_contman = new_cust.cust_contman
            exist_cust.cust_contphone = new_cust.cust_contphone
            exist_cust.cust_special = new_cust.cust_special
            # exist_cust.cust_district = new_cust.cust_district
            exist_cust.save()
        else:
            # 数据中未找到，保存到数据库
            new_cust.save()


    for cust_key in cust_keys:
        cust_weihu_url = "http://10.88.4.46/lm/cust/stcust.cmd?method=forupdate"
        cust_weihu_data = {
            "license_codeSearch": "",
            "cust_idSearch": "",
            "mnemonicCodeSearch": "",
            "managerSearch": "",
            "manager_id_cardSearch": "",
            "contactTelSearch": "",
            "cust_nameSearch": "",
            "orderTelSearch": "",
            "busi_addrSearch":"",
            "regie_depSearch":"",
            "regie_areaSearch":"",
            "primaryKey": cust_key,
            "STATUS": "01",
            "STATUS": "01",
            "STATUS": "02",
            "STATUS": "02",
            "STATUS": "02",
            "STATUS": "02",
            "STATUS": "02",
            "STATUS": "02",
            "STATUS": "02",
            "STATUS": "02",
            "hiddenInputForTitle": "v6默认layout",
            "hiddenInputForTitle":"v6默认layout"
        }
        resp = session.post(cust_weihu_url, headers=headers,data=cust_weihu_data)
        print("-----" + "获取到零售户维护" + "-----\n")
        license = re.findall(r'BUSI_LICENSE_ID\" maxlength=\"25\" value=\".+\"/>', resp.text)
        licenseId = ""
        if len(license)!=0 :
            licenseId = license[0][39:-3]
        print("信用代码"+licenseId)

        new_cust = Customer()
        new_cust.cust_licenseId = licenseId

        # 更新模型
        exist_custs = Customer.objects.filter(cust_key=cust_key)
        if len(exist_custs) != 0:
            exist_cust = exist_custs[0]
            exist_cust.cust_licenseId = new_cust.cust_licenseId
            exist_cust.save()


    # 暂停零售户






if __name__ == '__main__':
    start_spider()

