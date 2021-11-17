from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import DateField

from Sam.models import Customer, Employee, Group, Item, Job, Supplier, User, Cash, Category, Company, Credit, Group, Ledger, Login,  PCash, PCredit, PRSales_Return, PReceipt, Receipt, Sales_Return, SubCategory


class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cash
        # specify the fields that you want API to return below
        fields = ('amount', 'total3')




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Login
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = '__all__'


class CashSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cash

        fields =   '__all__'

class CreditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Credit

        fields =   '__all__'

class Sales_ReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sales_Return

        fields =   '__all__'

class ReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt

        fields =   '__all__'


class PCashSerializer(serializers.ModelSerializer):

    class Meta:
        model = PCash

        fields =   '__all__'

class PCreditSerializer(serializers.ModelSerializer):

    class Meta:
        model = PCredit

        fields =   '__all__'

class PRSales_ReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = PRSales_Return

        fields =   '__all__'

class PReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = PReceipt

        fields =   ['receipt_number', 'date', 'internal_ref_no', 'due_on' ,  'credit_limit_amt',   'user_id' ,  'supp_id' ,  'supp_name'  , 'si_no1' , 'si_no2' ,  'si_no3' ,  'invoice_no1' ,  'invoice_no2' ,  'invoice_no3',   'invoice_date1'  , 'invoice_date2' , 'invoice_date3' ,  'duedate1' ,   'duedate2' ,  'duedate3' ,  'invoice_amt1' ,  'invoice_amt2' , 'invoice_amt3' , 'received_amt1',  'received_amt2',  'received_amt3' , 'outstanding1' , 'outstanding2' , 'outstanding3',  'discount1'  , 'discount2' ,  'discount3',  'balance_amt1' , 'balance_amt2' , 'balance_amt3' , 'tick_space1' , 'tick_space2',  'tick_space3' ,  'partial1' ,  'partial2' ,  'partial3' ,  'total1',  'total2',  'total3' , 'total4' ,  'total5', 'total6' , 'on_account', 'discount' ]

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = [ 'group_name', 'category' ]



class ChartofSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ledger
        fields = [ 'ledger_name', 'category' ]



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
    lookup_field = 'id_child'



class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


