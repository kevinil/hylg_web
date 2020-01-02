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


    ids = None
    lists = []
    with open('yyzz.txt', 'r', encoding='utf-8') as f:
        ids = f.readlines()
        print(len(ids))
    for idNum in ids:
        cust = Customer.objects.filter(cust_key=idNum[0:-1])

        if (len(cust)) != 0:
            dict = {
                "id": idNum,
                "faren": cust[0].cust_faren,
                "dist": cust[0].cust_district
            }
            lists.append(dict)
        else:
            dict = {
                "id": idNum,
                "faren": "注销",
                "dist": "注销"
            }
            lists.append(dict)

    print(len(lists))
    print("匹配完成")
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')
    sheet.write(1, 0, "许可证号")
    sheet.write(1, 1, "法人")
    sheet.write(1, 2, "片区")


    for i in range(len(lists)):
        sheet.write(i + 2, 0, lists[i]["id"])
        sheet.write(i + 2, 1, lists[i]["faren"])
        sheet.write(i + 2, 2, lists[i]["dist"])

    print("写入excel完成")
    book.save('营业执照表' + ".xls")


if __name__ == '__main__':
    yyzz_spider()
