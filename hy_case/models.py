from django.db import models

# Create your models here.


class NoCert(models.Model):
    n_id = models.AutoField(primary_key=True)
    n_name = models.CharField(max_length=16)


    def __str__(self):
        return str(self.n_id) + ":   " + self.n_name

    class Meta:
        ordering = ["-n_id"]
        verbose_name = "无证户"
        verbose_name_plural = "无证户"


class Customer(models.Model):
    cust_key = models.CharField(max_length=32,unique=True,default=0)
    cust_licenseId = models.CharField(max_length=64,default="")
    cust_type = models.CharField(max_length=16,default="")
    cust_zihao = models.CharField(max_length=64)
    cust_faren = models.CharField(max_length=32)
    cust_idnum = models.CharField(max_length=32)
    cust_saleaddr = models.CharField(max_length=128)
    cust_idaddr = models.CharField(max_length=128)
    cust_contman = models.CharField(max_length=32)
    cust_contphone = models.CharField(max_length=32)
    cust_special = models.CharField(max_length=32)
    # cust_district = models.CharField(max_length=32,default="")


    def __str__(self):
        return self.cust_faren + ":   " + self.cust_key + "---" + self.cust_zihao

    class Meta:
        ordering = ["-cust_key"]
        verbose_name = "零售户"
        verbose_name_plural = "零售户"

class Clues(models.Model):
    cid = models.AutoField(primary_key=True)
    c_clue_type = models.CharField(max_length=16,default="")
    customer = models.ForeignKey(Customer, related_name="cust_clue",on_delete=models.CASCADE)
    c_car = models.CharField(max_length=64,default="")
    c_main_addr = models.CharField(max_length=128,default="")
    c_detail_addr = models.CharField(max_length=128,default="")
    c_relate_addr = models.CharField(max_length=128,default="")
    c_get_time = models.CharField(max_length=32,default="")
    c_case_type = models.CharField(max_length=32,default="")
    c_case_amount = models.CharField(max_length=32,default="")
    c_info = models.CharField(max_length=256,default="")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cid) + ":   " + self.c_clue_type + "---" + self.customer.cust_faren

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "线索"
        verbose_name_plural = "线索"


class CaseData(models.Model):
    case_key = models.CharField(max_length=32,unique=True,default=0)
    case_person = models.CharField(max_length=32)
    case_nature = models.CharField(max_length=128)          # 违法性质
    case_address = models.CharField(max_length=128)         # 地址
    case_carton = models.CharField(max_length=32,default=0) # 烟数量
    case_trans = models.CharField(max_length=32,default=0)  # 物流寄递方式
    case_date = models.CharField(max_length=32)             # 立案日期
    case_price = models.CharField(max_length=32)            # 案值金额
    case_detail = models.CharField(max_length=512)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.case_date + ":   " + self.case_person + "---" + self.case_nature + "===" + self.case_address

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "案件"
        verbose_name_plural = "案件"


class User(models.Model):

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256,default=0)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "网站用户"
        verbose_name_plural = "网站用户"