from django.db import models
import datetime
import os
from django.db.models.fields import DateField
from django.utils import timezone

# Create your models here.


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('Sam/uploads/', filename)


class Item(models.Model):
    item_name       =   models.TextField(max_length=100)
    item_desc       =   models.TextField(max_length=500, null=True)
    item_barcode    =   models.TextField(max_length=50)
    item_category   =   models.TextField(max_length=50)
    item_unit_prim  =   models.TextField(max_length=100)
    item_unit_sec   =   models.TextField(max_length=100)
    open_balance    =   models.TextField(max_length=100)
    buying_price    =   models.TextField(max_length=50)
    sell_price      =   models.TextField(max_length=50)
    image1          =   models.ImageField(upload_to=filepath, null=True,blank=True)
    image2          =   models.ImageField(upload_to=filepath, null=True,blank=True)
    image3          =   models.ImageField(upload_to=filepath, null=True,blank=True)
    image4          =   models.ImageField(upload_to=filepath, null=True,blank=True)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)
    class Meta:  
        db_table = "sam_item" 

class Customer(models.Model):
    customer_name   =   models.TextField(max_length=100)
    vat_reg_no      =   models.TextField(max_length=100)
    cr_no           =   models.TextField(max_length=100)
    expired_on      =   models.TextField(max_length=100)
    land_phone      =   models.TextField(max_length=100)
    mobile          =   models.TextField(max_length=100)
    contact_person  =   models.TextField(max_length=100)
    contact_mobile  =   models.TextField(max_length=100)
    email           =   models.TextField(max_length=100)
    address         =   models.TextField(max_length=100)
    open_balance    =   models.TextField(max_length=100)
    credit_lim_am   =   models.TextField(max_length=100)
    credit_lim_dur  =   models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)

class Supplier(models.Model):
    customer_name   =   models.TextField(max_length=100)
    vat_reg_no      =   models.TextField(max_length=100)
    cr_no           =   models.TextField(max_length=100)
    expired_on      =   models.TextField(max_length=100)
    land_phone      =   models.TextField(max_length=100)
    mobile          =   models.TextField(max_length=100)
    contact_person  =   models.TextField(max_length=100)
    contact_mobile  =   models.TextField(max_length=100)
    email           =   models.TextField(max_length=100)
    address         =   models.TextField(max_length=100)
    open_balance    =   models.TextField(max_length=100)
    credit_lim_am   =   models.TextField(max_length=100)
    credit_lim_dur  =   models.TextField(max_length=100)
    bank_acc_name   =   models.TextField(max_length=100)
    bank_acc_no     =   models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)


class User(models.Model):
    mobile_no   =   models.TextField(max_length=100)
    username    =   models.TextField(max_length=100)
    password    =   models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)

class Login(models.Model):
    username    =   models.TextField(max_length=100)
    password    =   models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)

class Job(models.Model):
    job_name    =   models.TextField(max_length=100)
    job_desc    =   models.TextField(max_length=500,null=True)
    imag1       =   models.ImageField(upload_to=filepath, null=True,blank=True)
    imag2       =   models.ImageField(upload_to=filepath, null=True,blank=True)
    imag3       =   models.ImageField(upload_to=filepath, null=True,blank=True)
    imag4       =   models.ImageField(upload_to=filepath, null=True,blank=True)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)

class Employee(models.Model):
    emp_name     =    models.TextField(max_length=100)
    nationality  =    models.TextField(max_length=100)
    birth_date   =    models.TextField(max_length=100)
    joining_date =    models.TextField(max_length=100)
    designation  =    models.TextField(max_length=100)
    department   =    models.TextField(max_length=100)
    salary_categ =    models.TextField(max_length=100)
    passport_no  =    models.TextField(max_length=100)
    expir        =    models.TextField(max_length=100)
    id_no        =    models.TextField(max_length=100)
    id_expir     =    models.TextField(max_length=100)
    img1         =   models.ImageField(upload_to=filepath, null=True,blank=True)
    img2         =   models.ImageField(upload_to=filepath, null=True,blank=True)
    img3         =   models.ImageField(upload_to=filepath, null=True,blank=True)
    img4         =   models.ImageField(upload_to=filepath, null=True,blank=True)
    basic        =    models.TextField(max_length=100)
    housing      =    models.TextField(max_length=100)
    transportation =    models.TextField(max_length=100)
    food         =    models.TextField(max_length=100)
    mobile       =    models.TextField(max_length=100)
    other        =    models.TextField(max_length=100)
    netpay       =    models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(auto_now=True,null=True)

# class Group(models.Model):
#     group_name    =    models.TextField(max_length=100)
#     category      =    models.TextField(max_length=100)
#     created_at = models.DateField(default=datetime.datetime.now,editable=False)
#     updated_at = models.DateField(null=True)


    

# class Ledger(models.Model):
#     ledger_name    =    models.TextField(max_length=100)
#     group_name     =    models.TextField(max_length=100)
#     category       =    models.TextField(max_length=100)
#     opening_bal    =    models.TextField(max_length=100)
#     created_at = models.DateField(default=datetime.datetime.now,editable=False)
#     updated_at = models.DateField(null=True)

# class Asset(models.Model):
#     asset_parent   =   models.TextField(max_length=100)
#     asset_child    =   models.TextField(max_length=100)
#     created_at = models.DateField(default=datetime.datetime.now,editable=False)
#     updated_at = models.DateField(null=True)
class Liabilities(models.Model):
    liability_parent   =   models.TextField(max_length=100)
    liability_child    =   models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.datetime.now,editable=False)
    updated_at = models.DateField(null=True)
class Income(models.Model):
    income_parent   =   models.TextField(max_length=100)
    income_child    =   models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.datetime.now,editable=False)
    updated_at = models.DateField(null=True)
class Expences(models.Model):
    expenses_parent   =   models.TextField(max_length=100)
    expenses_child    =   models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.datetime.now,editable=False)
    updated_at = models.DateField(null=True)

class Cash(models.Model):
    invoice_number = models.TextField(max_length=100)
    date = models.DateField(max_length=100)
    internal_ref_no = models.TextField(max_length=100)
    cash = models.TextField(max_length=100)
    user_id = models.TextField(max_length=100)
    account = models.TextField(max_length=100)
    customer_id = models.TextField(max_length=100)
    customer_name = models.TextField(max_length=100)
    item_id1 = models.TextField(max_length=100)
    item_id2 = models.TextField(max_length=100)
    item_details1 = models.TextField(max_length=100)
    item_details2 = models.TextField(max_length=100)
    price = models.TextField(max_length=100)
    price1_2 = models.TextField(max_length=100)
    price2_1 = models.TextField(max_length=100)
    price2_2 = models.TextField(max_length=100)
    qty = models.TextField(max_length=100)
    quantity2 = models.TextField(max_length=100)
    quantity3 = models.TextField(max_length=100)
    quantity4 = models.TextField(max_length=100)
    total = models.TextField(max_length=100)
    amount2 = models.TextField(max_length=100)
    sales_ex1 = models.TextField(max_length=100)
    sales_ex2 = models.TextField(max_length=100)
    job1 = models.TextField(max_length=100)
    job2 = models.TextField(max_length=100)
    labour_charge = models.TextField(max_length=100)
    other_charge = models.TextField(max_length=100)
    total1 = models.TextField(max_length=100)
    total2 = models.TextField(max_length=100)
    total3 = models.TextField(max_length=100)
    total4 = models.TextField(max_length=100)
    total5 = models.TextField(max_length=100)
    total6 = models.TextField(max_length=100)
    discount = models.TextField(max_length=100)
    tax = models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)

class Credit(models.Model):
    invoice_number = models.TextField(max_length=100)
    date = models.DateField(max_length=100)
    internal_ref_no = models.TextField(max_length=100)
    due_on = models.DateField()
    user_id = models.TextField(max_length=100)
    credit_limit_amt = models.TextField(max_length=100)
    account = models.TextField(max_length=100)
    customer_id = models.TextField(max_length=100)
    customer_name = models.TextField(max_length=100)
    item_id1 = models.TextField(max_length=100)
    item_id2 = models.TextField(max_length=100)
    item_details1 = models.TextField(max_length=100)
    item_details2 = models.TextField(max_length=100)
    price = models.TextField(max_length=100)
    price1_2 = models.TextField(max_length=100)
    price2_1 = models.TextField(max_length=100)
    price2_2 = models.TextField(max_length=100)
    qty = models.TextField(max_length=100)
    quantity2 = models.TextField(max_length=100)
    quantity3 = models.TextField(max_length=100)
    quantity4 = models.TextField(max_length=100)
    total = models.TextField(max_length=100)
    amount2 = models.TextField(max_length=100)
    sales_ex1 = models.TextField(max_length=100)
    sales_ex2 = models.TextField(max_length=100)
    job1 = models.TextField(max_length=100)
    job2 = models.TextField(max_length=100)
    labour_charge = models.TextField(max_length=100)
    other_charge = models.TextField(max_length=100)
    total1 = models.TextField(max_length=100)
    total2 = models.TextField(max_length=100)
    total3 = models.TextField(max_length=100)
    total4 = models.TextField(max_length=100)
    total5 = models.TextField(max_length=100)
    total6 = models.TextField(max_length=100)
    discount = models.TextField(max_length=100)
    tax = models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)

class Sales_Return(models.Model):
    invoice_number = models.TextField(max_length=100)
    date = models.DateField()
    internal_ref_no = models.TextField(max_length=100)
    user_id = models.TextField(max_length=100)
    customer_id = models.TextField(max_length=100)
    customer_name = models.TextField(max_length=100)
    item_id1 = models.TextField(max_length=100)
    item_id2 = models.TextField(max_length=100)
    item_details1 = models.TextField(max_length=100)
    item_details2 = models.TextField(max_length=100)
    price = models.TextField(max_length=100)
    price1_2 = models.TextField(max_length=100)
    price2_1 = models.TextField(max_length=100)
    price2_2 = models.TextField(max_length=100)
    quantity1 = models.TextField(max_length=100)
    qty = models.TextField(max_length=100)
    quantity3 = models.TextField(max_length=100)
    quantity4 = models.TextField(max_length=100)
    total = models.TextField(max_length=100)
    amount2 = models.TextField(max_length=100)
    sales_ex1 = models.TextField(max_length=100)
    sales_ex2 = models.TextField(max_length=100)
    job1 = models.TextField(max_length=100)
    job2 = models.TextField(max_length=100)
    labour_charge = models.TextField(max_length=100)
    other_charge = models.TextField(max_length=100)
    total1 = models.TextField(max_length=100)
    total2 = models.TextField(max_length=100)
    total3 = models.TextField(max_length=100)
    total4 = models.TextField(max_length=100)
    total5 = models.TextField(max_length=100)
    total6 = models.TextField(max_length=100)
    discount = models.TextField(max_length=100)
    tax = models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)


class Receipt(models.Model):
    receipt_number = models.TextField(max_length=100)
    date = models.DateField()
    internal_ref_no = models.TextField(max_length=100)
    due_on = models.DateField()
    credit_limit_amt = models.TextField(max_length=100)
    user_id = models.TextField(max_length=100)
    customer_id = models.TextField(max_length=100)
    customer_name = models.TextField(max_length=100)
    si_no1 = models.TextField(max_length=100)
    si_no2 = models.TextField(max_length=100)
    si_no3 = models.TextField(max_length=100)
    invoice_no1 = models.TextField(max_length=100)
    invoice_no2 = models.TextField(max_length=100)
    invoice_no3 = models.TextField(max_length=100)
    invoice_date1 = models.TextField(max_length=100)
    invoice_date2 = models.TextField(max_length=100)
    invoice_date3 = models.TextField(max_length=100)
    duedate1 = models.TextField(max_length=100)
    duedate2 = models.TextField(max_length=100)
    duedate3 = models.TextField(max_length=100)
    invoice_amt1 = models.TextField(max_length=100)
    invoice_amt2 = models.TextField(max_length=100)
    invoice_amt3 = models.TextField(max_length=100)
    received_amt1 = models.TextField(max_length=100)
    received_amt2 = models.TextField(max_length=100)
    received_amt3 = models.TextField(max_length=100)
    outstanding1 = models.TextField(max_length=100)
    outstanding2 = models.TextField(max_length=100)
    outstanding3 = models.TextField(max_length=100)
    discount1 = models.TextField(max_length=100)
    discount2 = models.TextField(max_length=100)
    discount3 = models.TextField(max_length=100)
    balance_amt1 = models.TextField(max_length=100)
    balance_amt2 = models.TextField(max_length=100)
    balance_amt3 = models.TextField(max_length=100)
    tick_space1 = models.TextField(max_length=100)
    tick_space2 = models.TextField(max_length=100)
    tick_space3 = models.TextField(max_length=100)
    partial1 = models.TextField(max_length=100)
    partial2 = models.TextField(max_length=100)
    partial3 = models.TextField(max_length=100)
    total1 = models.TextField(max_length=100)
    account = models.TextField(max_length=100)
    total3 = models.TextField(max_length=100)
    total4 = models.TextField(max_length=100)
    total5 = models.TextField(max_length=100)
    total6 = models.TextField(max_length=100)
    on_account = models.TextField(max_length=100)
    discount = models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)

class DemoPCash(models.Model):
    account = models.TextField(max_length=100)
    cash = models.TextField(max_length=100)
    date = models.DateField(max_length=100)
    ledger_name = models.CharField(max_length=100)



class PCash(models.Model):
    invoice_number = models.TextField(max_length=100)
    date = models.DateField()
    internal_ref_no = models.TextField(max_length=100)
    cash = models.TextField(max_length=100)
    user_id = models.TextField(max_length=100)
    account = models.TextField(max_length=100)
    supp_id = models.TextField(max_length=100)
    supp_name = models.TextField(max_length=100)
    item_id1 = models.TextField(max_length=100)
    item_id2 = models.TextField(max_length=100)
    item_details1 = models.TextField(max_length=100)
    item_details2 = models.TextField(max_length=100)
    price = models.TextField(max_length=100)
    price1_2 = models.TextField(max_length=100)
    price2_1 = models.TextField(max_length=100)
    price2_2 = models.TextField(max_length=100)
    qty = models.TextField(max_length=100)
    quantity2 = models.TextField(max_length=100)
    quantity3 = models.TextField(max_length=100)
    quantity4 = models.TextField(max_length=100)
    total = models.TextField(max_length=100)
    amount2 = models.TextField(max_length=100)
    sales_ex1 = models.TextField(max_length=100)
    sales_ex2 = models.TextField(max_length=100)
    job1 = models.TextField(max_length=100)
    job2 = models.TextField(max_length=100)
    labour_charge = models.TextField(max_length=100)
    other_charge = models.TextField(max_length=100)
    total1 = models.TextField(max_length=100)
    total2 = models.TextField(max_length=100)
    total3 = models.TextField(max_length=100)
    total4 = models.TextField(max_length=100)
    total5 = models.TextField(max_length=100)
    total6 = models.TextField(max_length=100)
    discount = models.TextField(max_length=100)
    tax = models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)

class PCredit(models.Model):
    invoice_number = models.TextField(max_length=100)
    date = models.DateField(max_length=100)
    internal_ref_no = models.TextField(max_length=100)
    due_on = models.DateField()
    user_id = models.TextField(max_length=100)
    credit_limit_amt = models.TextField(max_length=100)
    account = models.TextField(max_length=100)
    supp_id = models.TextField(max_length=100)
    supp_name = models.TextField(max_length=100)
    item_id1 = models.TextField(max_length=100)
    item_id2 = models.TextField(max_length=100)
    item_details1 = models.TextField(max_length=100)
    item_details2 = models.TextField(max_length=100)
    price = models.TextField(max_length=100)
    price1_2 = models.TextField(max_length=100)
    price2_1 = models.TextField(max_length=100)
    price2_2 = models.TextField(max_length=100)
    qty = models.TextField(max_length=100)
    quantity2 = models.TextField(max_length=100)
    quantity3 = models.TextField(max_length=100)
    quantity4 = models.TextField(max_length=100)
    total = models.TextField(max_length=100)
    amount2 = models.TextField(max_length=100)
    sales_ex1 = models.TextField(max_length=100)
    sales_ex2 = models.TextField(max_length=100)
    job1 = models.TextField(max_length=100)
    job2 = models.TextField(max_length=100)
    labour_charge = models.TextField(max_length=100)
    other_charge = models.TextField(max_length=100)
    total1 = models.TextField(max_length=100)
    total2 = models.TextField(max_length=100)
    total3 = models.TextField(max_length=100)
    total4 = models.TextField(max_length=100)
    total5 = models.TextField(max_length=100)
    total6 = models.TextField(max_length=100)
    discount = models.TextField(max_length=100)
    tax = models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)


class PRSales_Return(models.Model):
    invoice_number = models.TextField(max_length=100)
    date = models.DateField()
    internal_ref_no = models.TextField(max_length=100)
    user_id = models.TextField(max_length=100)
    due_on = models.DateField()
    credit_limit_amt = models.TextField(max_length=100)
    supp_id = models.TextField(max_length=100)
    supp_name = models.TextField(max_length=100)
    item_id1 = models.TextField(max_length=100)
    item_id2 = models.TextField(max_length=100)
    item_details1 = models.TextField(max_length=100)
    item_details2 = models.TextField(max_length=100)
    price = models.TextField(max_length=100)
    price1_2 = models.TextField(max_length=100)
    price2_1 = models.TextField(max_length=100)
    price2_2 = models.TextField(max_length=100)
    qty = models.TextField(max_length=100)
    quantity2 = models.TextField(max_length=100)
    quantity3 = models.TextField(max_length=100)
    quantity4 = models.TextField(max_length=100)
    total = models.TextField(max_length=100)
    amount2 = models.TextField(max_length=100)
    sales_ex1 = models.TextField(max_length=100)
    sales_ex2 = models.TextField(max_length=100)
    job1 = models.TextField(max_length=100)
    job2 = models.TextField(max_length=100)
    labour_charge = models.TextField(max_length=100)
    other_charge = models.TextField(max_length=100)
    total1 = models.TextField(max_length=100)
    total2 = models.TextField(max_length=100)
    total3 = models.TextField(max_length=100)
    total4 = models.TextField(max_length=100)
    total5 = models.TextField(max_length=100)
    total6 = models.TextField(max_length=100)
    discount = models.TextField(max_length=100)
    tax = models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)

class PReceipt(models.Model):
    receipt_number = models.TextField(max_length=100)
    date = models.DateField()
    internal_ref_no = models.TextField(max_length=100)
    due_on = models.DateField()
    credit_limit_amt = models.TextField(max_length=100)
    user_id = models.TextField(max_length=100)
    supp_id = models.TextField(max_length=100)
    supp_name = models.TextField(max_length=100)
    si_no1 = models.TextField(max_length=100)
    si_no2 = models.TextField(max_length=100)
    si_no3 = models.TextField(max_length=100)
    invoice_no1 = models.TextField(max_length=100)
    invoice_no2 = models.TextField(max_length=100)
    invoice_no3 = models.TextField(max_length=100)
    invoice_date1 = models.TextField(max_length=100)
    invoice_date2 = models.TextField(max_length=100)
    invoice_date3 = models.TextField(max_length=100)
    duedate1 = models.TextField(max_length=100)
    duedate2 = models.TextField(max_length=100)
    duedate3 = models.TextField(max_length=100)
    invoice_amt1 = models.TextField(max_length=100)
    invoice_amt2 = models.TextField(max_length=100)
    invoice_amt3 = models.TextField(max_length=100)
    received_amt1 = models.TextField(max_length=100)
    received_amt2 = models.TextField(max_length=100)
    received_amt3 = models.TextField(max_length=100)
    outstanding1 = models.TextField(max_length=100)
    outstanding2 = models.TextField(max_length=100)
    outstanding3 = models.TextField(max_length=100)
    discount1 = models.TextField(max_length=100)
    discount2 = models.TextField(max_length=100)
    discount3 = models.TextField(max_length=100)
    balance_amt1 = models.TextField(max_length=100)
    balance_amt2 = models.TextField(max_length=100)
    balance_amt3 = models.TextField(max_length=100)
    tick_space1 = models.TextField(max_length=100)
    tick_space2 = models.TextField(max_length=100)
    tick_space3 = models.TextField(max_length=100)
    partial1 = models.TextField(max_length=100)
    partial2 = models.TextField(max_length=100)
    partial3 = models.TextField(max_length=100)
    total1 = models.TextField(max_length=100)
    account = models.TextField(max_length=100)
    total3 = models.TextField(max_length=100)
    total4 = models.TextField(max_length=100)
    total5 = models.TextField(max_length=100)
    total6 = models.TextField(max_length=100)
    on_account = models.TextField(max_length=100)
    discount = models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at = models.DateField(null=True)
    
# class Ledger_Statement(models.Model):
#     date   =   models.TextField(max_length=100)
#     ledger_name    =   models.TextField(max_length=100)
#     ledger_id = models.TextField(max_length=100)
#     period = models.TextField(max_length=100)
class Ledger_Journal(models.Model):
    date   =   models.TextField(max_length=100)
    reportdate    =   models.TextField(max_length=100)
class Ledger_Masterdata(models.Model):
    date   =   models.TextField(max_length=100)
    reportdate    =   models.TextField(max_length=100)
class Stock_Balance(models.Model):
    date   =   models.TextField(max_length=100)
    reportdate    =   models.TextField(max_length=100)
class Item_Statement(models.Model):
    date   =   models.TextField(max_length=100)
    item_id    =   models.TextField(max_length=100)
    item_name = models.TextField(max_length=100)
    period = models.TextField(max_length=100)
class Stock_Adjustment(models.Model):
    date = models.TextField(max_length=100)
    reportdate = models.TextField(max_length=100)
class Stock_Masterdata(models.Model):
    date = models.TextField(max_length=100)
    reportdate = models.TextField(max_length=100)
class job_Statement(models.Model):
    date = models.TextField(max_length=100)
    job = models.TextField(max_length=100)
    job_id = models.TextField(max_length=100)
    period = models.TextField(max_length=100)
class job_Masterdata(models.Model):
    date = models.TextField(max_length=100)
    reportdate = models.TextField(max_length=100)
    
class Customer_Statement(models.Model):
    date   =   models.TextField(max_length=100)
    report_period = models.TextField(max_length=100)
    customer_name    =   models.TextField(max_length=100)
    customer_id = models.TextField(max_length=100)
class Customer_Outstand(models.Model):
    date   =   models.TextField(max_length=100)
    report_date = models.TextField(max_length=100)
    customer_name    =   models.TextField(max_length=100)
    customer_id = models.TextField(max_length=100)
# class Customer_Invoice(models.Model):
#     report_date = models.TextField(max_length=100)
#     invoice_no   =   models.TextField(max_length=100)
#     customer_id = models.TextField(max_length=100)
#     customer_name    =   models.TextField(max_length=100)
class Customer_Receipt(models.Model):
    customer_id = models.TextField(max_length=100)
    report_date = models.TextField(max_length=100)
    customer_name    =   models.TextField(max_length=100)
    receipt_no   =   models.TextField(max_length=100)
class Customer_Invoice_Receipt(models.Model):
    date = models.TextField(max_length=100)
    report_date = models.TextField(max_length=100)
class Customer_Masterdata(models.Model):
    date = models.TextField(max_length=100)
    report_date = models.TextField(max_length=100)
class Supplier_Statement(models.Model):
    Supplier_name    =   models.TextField(max_length=100)
    Supplier_id = models.TextField(max_length=100)
    date   =   models.TextField(max_length=100)
    report_period = models.TextField(max_length=100)
class Supplier_Outstand(models.Model):
    date   =   models.TextField(max_length=100)
    report_date = models.TextField(max_length=100)
    Supplier_name    =   models.TextField(max_length=100)
    Supplier_id = models.TextField(max_length=100)
class Supplier_Invoice(models.Model):
    report_date = models.TextField(max_length=100)
    invoice_no   =   models.TextField(max_length=100)
    Supplier_name    =   models.TextField(max_length=100)
    Supplier_id = models.TextField(max_length=100)
class payment_History(models.Model):
    Supplier_name    =   models.TextField(max_length=100)
    Supplier_id = models.TextField(max_length=100)
    report_date = models.TextField(max_length=100)
    voucher_no   =   models.TextField(max_length=100)
class Supplier_Invoice_Receipt(models.Model):
    date = models.TextField(max_length=100)
    report_date = models.TextField(max_length=100)
class Supplier_Masterdata(models.Model):
    date = models.TextField(max_length=100)
    report_date = models.TextField(max_length=100)
    created_at = models.DateField(auto_now_add=True,auto_now=False)
    updated_at = models.DateTimeField(null=True)


class ledgerStatem(models.Model):
    From_Date = models.DateField()
    To_Date = models.DateField()
    Ledger_Name = models.CharField(max_length=50)


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_regno = models.IntegerField()
    app_regdate   = models.DateField()
    reg_mobno = models.BigIntegerField()
    email = models.CharField(max_length=50)
    admin_usernm = models.CharField(max_length=100)
    admin_password = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    mobile  = models.BigIntegerField()
    user_access = models.CharField(max_length=50)
    imag1       =   models.ImageField(upload_to=filepath, null=True,blank=True)
    imag2       =   models.ImageField(upload_to=filepath, null=True,blank=True)
    created_at = models.DateField(default=datetime.date.today,editable=False)



#model from chart of account

class Suppliers(models.Model):
    supplier_name   =   models.TextField(max_length=100)
    supplier_id = models.IntegerField()
    invoice_no=models.IntegerField()
    reportDate=models.DateField(max_length=100)

class SupplierInvoice(models.Model):
    supplier_id   =   models.TextField(max_length=100)
    supplier_name      =   models.TextField(max_length=100)
    report_date           =   models.TextField(max_length=100)
    invoice_no      =   models.TextField(max_length=100)

class Customers(models.Model):
    customer_name   =   models.TextField(max_length=100)
    customer_id = models.IntegerField()
    invoice_no=models.IntegerField()
    reportDate=models.DateField(max_length=100)

class CustomerInvoice(models.Model):
    report_date      =   models.TextField(max_length=100)
    invoice_no           =   models.TextField(max_length=100)
    cusomer_id      =   models.TextField(max_length=100)
    customer_name      =   models.TextField(max_length=100)

class Category(models.Model):
    category_name = models.CharField(max_length=254, unique=True, 
        blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    type = models.CharField(max_length=15, default='dynamic', null=True,
        blank=True)
    status = models.BooleanField(default=True, null=True,
        blank=True)

    def __str__(self):
        return self.category_name

class Ledger_Statement(models.Model):
    created_at = models.DateField(default=datetime.date.today,editable=False)
    to_date=models.DateField(null=True)
    
    ledger_name = models.TextField(max_length=100)

class SubCategory(models.Model):
    name = models.CharField(max_length=254, unique=True)
    price = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ChildCategory(models.Model):
    name = models.CharField(max_length=254, unique=True)
    id_child = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name



from django.db import IntegrityError

class Ledger(models.Model):
    created_at = models.DateField(default=datetime.date.today,editable=False)
    updated_at=models.DateField(null=True)
    ledger_name    =    models.CharField(max_length=100)
    group    =    models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    category       =    models.TextField(max_length=100)
    opening_bal    =    models.TextField(max_length=100)
    parent    =    models.ForeignKey(
        'Ledger',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
class Group(models.Model):
    group_name    =    models.TextField(max_length=100)
    category    =    models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
    
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.group_name
    



class Trial_Balance(models.Model):
    date = models.DateField()
    reportdate = models.TextField(max_length=100)
    ledger_id=models.IntegerField()
    ledger_name=models.TextField(max_length=100)
    ledger_category=models.TextField(max_length=100)
    opening_bal    =    models.TextField(max_length=100)
    debit_amount=models.TextField(max_length=100)
    credit_amount=models.TextField(max_length=100)
    closing_bal=models.TextField(max_length=100)


# class Asset(models.Model):
#     name  =   models.TextField(max_length=250, null=True)
#     parent =   models.ForeignKey(
#         'self',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True)
#     def _str_(self):
#       return self.name
#     class Meta:
#         ordering =('name',)
#         verbose_name_plural='Assets'