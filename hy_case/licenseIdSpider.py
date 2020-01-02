# -*- coding:utf-8 -*-
import io
import os
import sys
import django
import xlwt



pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
# 连接django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hylg_web.settings")
django.setup()
# 导入models
from hy_case.models import CaseData, Customer


def yyzz_spider():

    lists = []
    for cust in Customer.objects.all():
        dict = {
            "id": cust.cust_key,
            "faren": cust.cust_faren,
            "dist": cust.cust_district,
            "zihao": cust.cust_zihao,
            "licenseId": cust.cust_licenseId,
            "saleaddr": cust.cust_saleaddr,
            "idnum": cust.cust_idnum
        }
        lists.append(dict)

    print(len(lists))
    print("匹配完成")
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')
    sheet.write(1, 0, "许可证号")
    sheet.write(1, 1, "法人")
    sheet.write(1, 2, "片区")
    sheet.write(1, 3, "企业字号")
    sheet.write(1, 4, "工商信用代码")
    sheet.write(1, 5, "经营地址")
    sheet.write(1, 6, "身份证号")


    for i in range(len(lists)):
        sheet.write(i + 2, 0, lists[i]["id"])
        sheet.write(i + 2, 1, lists[i]["faren"])
        sheet.write(i + 2, 2, lists[i]["dist"])
        sheet.write(i + 2, 3, lists[i]["zihao"])
        sheet.write(i + 2, 4, lists[i]["licenseId"])
        sheet.write(i + 2, 5, lists[i]["saleaddr"])
        sheet.write(i + 2, 6, lists[i]["idnum"])

    print("写入excel完成")
    book.save('维护信息表' + ".xls")


if __name__ == '__main__':
    yyzz_spider()
