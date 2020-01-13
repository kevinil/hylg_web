from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from . import models
from . import forms
import hashlib
from . import wordCloudGenerate

user_name = ''


# Create your views here.
@csrf_exempt
def user(request):
    if request.method == "POST":
        obj = json.loads(request.body)
        if obj["getData"] == "psd":
            u_name = obj['name']
            u_psd = obj['psd']
            existUser = models.User.objects.get(name=u_name)
            existUser.password = u_psd
            existUser.save()
        else:
            res = []
            res.append(user_name)
            return HttpResponse(json.dumps(res))
    else:
        pass


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def page_error(request):
    return render(request, 'hy_case/404.html', status=404)

def page_not_found(request, exception):
    return render(request, 'hy_case/404.html', status=500)


def redirect_view(request):
    # response = redirect('http://127.0.0.1:8000/#/')
    response = redirect('/index/')
    return response


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'hy_case/login.html', locals())

            if user.password == password:  # hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                global user_name
                user_name = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'hy_case/login.html', locals())
        else:
            return render(request, 'hy_case/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'hy_case/login.html', locals())


@csrf_exempt
def logout(request):
    print(111111)
    print(request.session.get('is_login', None))
    # if not request.session.get('is_login', None):
    #     return redirect('/login/')

    # if request.method == 'POST':
    #     request.session.flush()

    request.session.flush()
    return redirect("/login/")

    # return render(request, 'login/')


@csrf_exempt
def case(request):
    if request.method == 'POST':
        obj = json.loads(request.body)
        words = []
        if obj["show"] == "wordCloud":
            for o in models.Customer.objects.all():
                words.append(o.cust_faren)
        cloud = " ".join(words)
        # caseWcGenerate()
        # wcGenerate(cloud)
        return HttpResponse(json.dumps(cloud), content_type="application/json")
    else:
        return render(request, 'index.html')


@csrf_exempt
def data(request):
    if request.method == 'POST':
        print('请求数据')
        obj = json.loads(request.body)
        # print(obj) {'getData': 'customers'}   {'getData': 'oneCustomer'}
        res = []
        if obj["getData"] == "customers":
            for cust in models.Customer.objects.all():
                dict = {
                    "faren": cust.cust_faren,
                    "certId": cust.cust_key,
                    "zihao": cust.cust_zihao
                }
                res.append(dict)
        else:
            lists = models.Customer.objects.filter(cust_key=obj["getData"])
            if len(lists) != 0:
                cust = lists[0]
                clueArray = []
                for clue in cust.cust_clue.all():
                    cd = {
                        "car": clue.c_car,
                        "maddr": clue.c_main_addr,
                        "daddr": clue.c_detail_addr,
                        "raddr": clue.c_relate_addr,
                        "time": clue.c_get_time,
                        "caseTypes": clue.c_case_type,
                        "caseAmount": clue.c_case_amount,
                        "caseInfo": clue.c_info
                    }
                    clueArray.append(cd)

                dict = {
                    "key": cust.cust_key,
                    "zihao": cust.cust_zihao,
                    "faren": cust.cust_faren,
                    "idNum": cust.cust_idnum,
                    "saleaddr": cust.cust_saleaddr,
                    "idaddr": cust.cust_idaddr,
                    "contman": cust.cust_contman,
                    "contphone": cust.cust_contphone,
                    "special": cust.cust_special,
                    # "district": cust.cust_district,
                    "clues": clueArray
                }

                res.append(dict)
                print(res)
                print("准备发回详细数据")
        return HttpResponse(json.dumps(res))
    else:
        return render(request, 'index.html')


@csrf_exempt
def report(request):
    return render(request, 'index.html')


@csrf_exempt
def clue(request):

    if request.method == 'POST':
        print("上传线索数据")
        obj = json.loads(request.body)
        res = "上传完成"

        print(obj)

        if obj["custType"] == "新客户":
            print("创建新无证户")
            # 新无证户
            nn = models.NoCert()
            nn.n_name = obj["custName"]
            nn.save()

            # 加入客户总表
            new_cust = models.Customer()
            new_cust.cust_key = 1000000 + nn.n_id
            obj["custId"] = new_cust.cust_key
            new_cust.cust_faren = obj["custName"]
            new_cust.cust_type = "无证户"
            new_cust.save()

        # 以客户为基准，导入线索数据
        nc = models.Clues()
        nc.customer = models.Customer.objects.get(cust_key=obj["custId"])
        nc.c_clue_type = obj["clueType"]
        nc.c_car = obj["caseCars"]
        nc.c_main_addr = obj["mainAddr"]
        nc.c_detail_addr = obj["detailAddr"]
        nc.c_relate_addr = obj["relateAddr"]
        nc.c_get_time = obj["getDate"]
        nc.c_case_type = obj["caseTypes"]
        nc.c_case_amount = obj["caseAmount"]
        nc.c_info = obj["caseInfos"]
        nc.save()

        return HttpResponse(res)
    else:
        return render(request, 'index.html')


@csrf_exempt
def reportRequest(request):
    if request.method == 'POST':
        print('请求来了')

    # 总计
    all_case = 0
    all_carton = 0
    all_price = 0

    # 物流
    logistics_case = 0
    logistics_carton = 0
    logistics_price = 0

    # 寄递
    express_case = 0
    express_carton = 0
    express_price = 0

    # 地点匹配
    local_case = 0
    local_carton = 0
    local_price = 0

    obj = json.loads(request.body)
    d1 = obj['d1']
    d2 = obj['d2']
    locations = obj['locations']
    wuliu = obj['wl']
    jidi = obj['jd']
    print(d1)
    print(d2)
    for local in locations:
        print(local)
    print(wuliu)
    print(jidi)

    for o in models.CaseData.objects.all():
        if d1 <= o.case_date <= d2:
            print("案件" + o.case_person + "   " + o.case_key)
            all_case += 1
            all_carton += float(o.case_carton)
            all_price += float(o.case_price)

            # 统计物流
            if wuliu == True:
                if o.case_trans == "物流":
                    logistics_case += 1
                    logistics_carton += float(o.case_carton)
                    logistics_price += float(o.case_price)

            # 统计寄递
            if jidi == True:
                if o.case_trans == "快递":
                    express_case += 1
                    express_carton += float(o.case_carton)
                    express_price += float(o.case_price)

            # 统计指定地点
            for local in locations:
                if o.case_address.find(local) != -1:
                    local_case += 1
                    local_carton += float(o.case_carton)
                    local_price += float(o.case_price)

    res = [{
        "type": "总计",
        "case": all_case,
        "carton": '%.2f' % float(all_carton / 50),
        "price": '%.2f' % float(all_price / 50),
    },
        {
            "type": "物流",
            "case": logistics_case,
            "carton": '%.2f' % float(logistics_carton / 50),
            "price": '%.2f' % float(logistics_price / 50),
        },
        {
            "type": "寄递",
            "case": express_case,
            "carton": '%.2f' % float(express_carton / 50),
            "price": '%.2f' % float(express_price / 50),
        },
        {
            "type": "指定地点",
            "case": local_case,
            "carton": '%.2f' % float(local_carton / 50),
            "price": '%.2f' % float(local_price / 50),
        }]
    print(res)
    return HttpResponse(json.dumps(res), content_type="application/json")
