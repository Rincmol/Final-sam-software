from datetime import datetime
from django.shortcuts import HttpResponse
from django.db.models.fields import DateTimeField
from django.shortcuts import render, redirect
from rest_framework.serializers import Serializer
from Sam import serializers
from Sam.models import Category, Employee,User, Company, Customer, Customer_Invoice_Receipt, Customer_Masterdata, Customer_Outstand, Customer_Receipt, Customer_Statement, CustomerInvoice, Customers, DemoPCash,  Supplier, Stock_Adjustment, Supplier_Invoice, Supplier_Invoice_Receipt, Supplier_Masterdata, Supplier_Outstand, Supplier_Statement, SupplierInvoice, job_Masterdata, job_Statement, Stock_Masterdata, Ledger_Masterdata,Item_Statement, Stock_Balance, Group, Ledger, PCredit, PCash,Ledger_Statement, Ledger_Journal, PRSales_Return, Item, Job, Liabilities, Expences, Receipt, PReceipt, Income, Cash, Credit, Sales_Return, payment_History
from Sam.serializers import  CustomerSerializer, EmployeeSerializer, GroupSerializer, ItemSerializer,  JobSerializer , SupplierSerializer, TimesheetSerializer, UserSerializer,LoginSerializer, CashSerializer, CategorySerializer, ChartofSerializer, CompanySerializer, CreditSerializer, GroupSerializer,  PCashSerializer, PCreditSerializer, PRSales_ReturnSerializer, PReceiptSerializer, ReceiptSerializer, Sales_ReturnSerializer
from .forms import ItemForm, JobForm
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http.response import Http404, JsonResponse
from django.utils import timezone
from django.db.models import Sum
from django.db.models import F
from rest_framework.renderers  import TemplateHTMLRenderer
from django.db.models import Q
import jwt
from rest_framework import generics    

def go(request):
    return render(request,'Sam/dashboard.html')


class DateListView(generics.ListAPIView):
        serializer_class = TimesheetSerializer

        def get_queryset(self):
            #get user and week_number from GET request
            user = self.request.GET.get('account')
            week_number = self.request.GET.get('total3')

            #filter and return the first result where user=user and week=week
            return Cash.objects.filter(account=user, total3=week_number)




#chart of account  Aparna 

def tablesjoin(request):
   queryset = CustomerInvoice.objects.all().select_related('customer_name').select_related('name')

def customersview(request):
    supp2 = Customers.objects.all()
    context = {'supp': supp2}
    return render(request,'Sam/chart of accounts.html', context)

def gopandl(request):
    
        df = request.POST.get('from_date')
        dt = request.POST.get('to_date')
        #nm = request.POST.get('ldg_nam')
       
         
        demoac = Cash.objects.filter(date__range=[df, dt]) 
        #l= demo5.aggregate(totals=Sum('cash'))
       
        
        demol = PCash.objects.filter(date__range=[df, dt])
        
        demo1 = Receipt.objects.filter(date__range=[df, dt])
        demo2 = PReceipt.objects.filter(date__range=[df, dt])

        return render(request,'Sam/Profit and loss.html' ,{ "demoac":demoac, "demol":demol,"demo1":demo1,"demo2":demo2 })



def gobsheet(request):

    df = request.POST.get('from_date')
    dt = request.POST.get('to_date')

    lb1 = PReceipt.objects.filter(date__range=[df, dt])
    lb5 = Cash.objects.filter(date__range=[df, dt])
    lb3 = PCash.objects.filter(date__range=[df, dt])
    lb4 = PCredit.objects.filter(date__range=[df, dt])
    as1 = Cash.objects.filter(date__range=[df, dt])
    as2 = Credit.objects.filter(date__range=[df, dt])
    as3 = Cash.objects.filter(date__range=[df, dt])

    return render(request,'Sam/Balance sheet.html',{"as1":as1,"as2":as2,"lb3":lb3,"lb4":lb4,"lb1":lb1})

def gotrialbalance(request):
    groups=Group.objects.all()
    ledgers = Ledger.objects.all()
    sundry_debtors = Customer.objects.all()
    sundry_creditors = Supplier.objects.all()
    closing_stock=Item.objects.all()
    cash_sale=Cash.objects.all()
    df = request.POST.get('from_date')
    dt = request.POST.get('to_date',)
    r = Ledger.objects.filter(created_at__range=[df, dt])
    pcash=PCash.objects.all()


    df = request.POST.get('from_date')
    dt = request.POST.get('to_date')
   
       
      
    demoac = DemoPCash.objects.filter(date__range=[df, dt]) 
       
   

    closing_bal1=2900
    closing_bal2=2900
    a=123
    b=5800
    c=(a+b)
    closing_balance=(closing_bal1+closing_bal2)
    return render(request,'Sam/Trial Balance.html',{"r":r,"c":c,"ledgers": ledgers,
        "groups":groups,"demoac":demoac,
        "sundry_debtors": sundry_debtors,
        "sundry_creditors": sundry_creditors,
        "closing_bal1": closing_bal1,
        "closing_bal2": closing_bal2,
        "closing_balance":closing_balance,
        "closing_stock": closing_stock,"cash_sale":cash_sale,"pcash":pcash,})


def gogroup(request):
    category=Category.objects.all()
    return render(request,'Sam/group.html',{"category":category})
def groupcreate(request):
    
    if request.method == "POST":

        category_id = request.POST.get('category_id', None)
        grp2 = Group(group_name=request.POST['group_name'])
        results = Group(
            group_name=request.POST['group_name'],
            category_id=category_id,
             
            status = request.POST.get('status', 1),
        )
        results.save()

        category = Category.objects.all()
        return render(request,'Sam/group.html',{"category":category})


def goledger(request):
    if request.method == "POST":
        group_id = request.POST.get('group_id', None)

        Group(group_id=group_id, group_name=request.POST['group_name'], status=1, type='dynamic').save()

        return redirect( '/Sam/goaccount')

    groups = Group.objects.all()
    ledgers=Ledger.objects.all()
    return render(request,'Sam/ledger.html',{"groups":groups,"ledgers":ledgers})

def ledgercreate(request):
  if request.method == "POST":
    group_id = request.POST.get('group_id', None)
    parent_id=request.POST.get('parent_id', None)
    
    ldg2 = Ledger(created_at=request.POST['created_at'],ledger_name=request.POST['ledger_name'],group_id=group_id,parent_id=parent_id,category=request.POST['category'],opening_bal=request.POST['opening_bal'],)
    ldg2.save()
    return redirect( '/')


def find_child_category(ledgers, parent_id, parent_index):
    children = []
    groups=[]
    ledgers=[]
    index = 1;
    for cat in groups:
        if cat.parent_id == parent_id:
            children.append({
                "sl_no": parent_index + ' . ' + str(index),
                "id": cat.id,
                "name": cat.ledger_name,
                "type": cat.type,
                "status": cat.status,
                "children": find_child_category(ledgers, cat.id, parent_index + ' . ' + str(index))
            })
            index += 1

    return ledgers


def goaccount(request):
    groups=Group.objects.all()
    category=Category.objects.all()
    ledgers = Ledger.objects.filter(parent_id__isnull=True)
    subLedgers = Ledger.objects.exclude(parent_id__isnull=True)
    sundry_debtors = Customer.objects.all()
    sundry_creditors = Supplier.objects.all()
    closing_stock=Item.objects.all()
    # ledgers=[]
    # index = 1;
    # for cat in ledgersAll:
    #     if not cat.parent_id:
    #         ledgers.append({
    #             "sl_no": index,
    #             "id": cat.id,
    #             "name": cat.ledger_name,
            
    #             "children": find_child_category(ledgers, cat.id, str(index))
    #         })
    #         index += 1;
    
    return render(request,'Sam/chart of account.html', {
        "groups": groups,
        "ledgers":ledgers,
        "subLedgers": subLedgers,
        "category":category,
        "ledgers":ledgers,
        "sundry_debtors": sundry_debtors,
        "sundry_creditors": sundry_creditors,
        "closing_stock": closing_stock,
        "blank_data": []
    })


def goasset(request):
    results=Group.objects.all()

    return render(request,'Sam/chart_of_account.html',{Group:results,})

def find_child_assets(request):
    if request.is_ajax and request.method == "GET":

        parent_id = request.GET.get("parent_id", None)
        assets = Asset.objects.filter(parent_id=parent_id)

        children = serializers.serialize('json', [assets])
        return JsonResponse({"children": children}, status=200)

    return JsonResponse({}, status = 400)

def addnewasset(request):
      if request.method == "POST":

        parent_id = request.POST.get('parent_id', None)

        results = Category(
            category_name=request.POST['category_name'],
            parent_id=parent_id,
            type = request.POST.get('type', "dynamic"), 
            status = request.POST.get('status', 1),
        )
        results.save()

      result = Category.objects.all()
      return render(request,'Sam/Add new asset.html',{"result":result})
def custinvoice(request):
    return render(request,'Sam/customer invoice.html')
def cinvocreate(request):
    c = CustomerInvoice(cusomer_id=request.POST['cusomer_id'],customer_name=request.POST['customer_name'],report_date=request.POST['report_date'],invoice_no=request.POST['invoice_no'],)
    c.save()
    return redirect( '/')


def supinvoice(request):
    return render(request,'Sam/supplier invoice.html')
def sinvocreate(request):
    c = SupplierInvoice(supplier_id=request.POST['supplier_id'],supplier_name=request.POST['supplier_name'],report_date=request.POST['report_date'],invoice_no=request.POST['invoice_no'],)
    c.save()
    return redirect( '/')
def edit_asset(request):
    
 
    result= Ledger(ledger_name=request.POST.get('ledger_name',None))
    result.save()
    results = Ledger.objects.all()
    
    return render(request,'Sam/edit_asset.html', {"results": results,})

def delete_asset(request, id):
    Category.objects.filter(parent_id=id).delete()
    Category.objects.filter(id=id).delete()

    return redirect( '/Sam/goaccount')

def assetcreate(request):
    ast2 = Asset(asset_parent=request.POST['asset_parent'],asset_child=request.POST['asset_child'],new_child=request.POST['new_child'],child=request.POST['child'])
    ast2.save()
    return redirect( '/')


class CategoryClass():

    serializer_class = CategorySerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user is not None:
                if user.is_active and user.is_superuser:
                    return Category.objects.all()

class SubCategory():

  def get_queryset(self):
    id_child = self.request.query_params.get('id_child')
    queryset = super().get_queryset()
    if id_child:
        queryset = queryset.filter(id_parent=id_child)
    return queryset
class ChildCategory():

  def get_queryset(self):
    id_child = self.request.query_params.get('id_child')
    queryset = super().get_queryset()
    if id_child:
        queryset = queryset.filter(id_child=id_child)
    return queryset


    serializer_class = SubCategorySerializer


def goledgerstmt(request):
   
        groups=Group.objects.all()
        category=Category.objects.all()
        ledgers = Ledger.objects.filter(parent_id__isnull=True)
        subLedgers = Ledger.objects.exclude(parent_id__isnull=True)
        sundry_debtors = Customer.objects.all()
        sundry_creditors = Supplier.objects.all()
        cash_sale=Cash.objects.all()
        
        pcash=PCash.objects.all()
        closing_stock=Item.objects.all()


        df = request.POST.get('from_date')
        dt = request.POST.get('to_date')
        nm = request.POST.get('ldg_nam')
       
        demop=DemoPCash.objects.filter(account=nm )  
        demoac = demop.filter(date__range=[df, dt]) 
       
        dmo = DemoPCash.objects.filter(ledger_name =nm ) 
        demol = dmo.filter(date__range=[df, dt])

        # demodb = DemoPCash.objects.all()
         # r = Ledger.objects.filter(created_at__range=[df, dt])
        #demo1=demop.annotate(Sum(F('cash')) )

        
        #job.objects.filter(query)
       
        ##  DemoPCash.objects.filter(ledger_name=nm )
        #demol=demo.filter(account = nm) , demo.filter(ledger_name = nm)
       
        #demol=
        ledger=request.POST.get('opening_bal')
        a=123
        b=12
        c=(a+b)
        return render(request,'Sam/ledger statement.html',{"c":c,"groups": groups,
        "ledgers":ledgers,
        "subLedgers": subLedgers,
        "category":category,
        "ledgers":ledgers,
        "sundry_debtors": sundry_debtors,
        "sundry_creditors": sundry_creditors,
        "cash_sale":cash_sale,
        "pcash":pcash,
        "demoac":demoac,
        #"demo":demo,
        "demol":demol,
        #"demodb":demodb,
        
        #"demop":demop,
        #"demo1":demo1,
        #"demo":demo3,
        #"closing_stock": closing_stock,"r":r
        })




        







def gocust(request):
    return render(request,'Sam/customer.html')
def goreports(request):
    return render(request,'Sam/Report.html')
# def goledgerstmt(request):
#     return render(request,'Sam/ledger statement.html')
def ldgrstmtcreate(request):
    ldgr2 = Ledger_Statement(date=request.POST['date'],ledger_name=request.POST['ledger_name'],ledger_id=request.POST['ledger_id'],period=request.POST['period'],)
    ldgr2.save()
    return redirect( '/')
def goledgerjournal(request):
    return render(request,'Sam/All Journal Entry.html')
def ldgrjournalcreate(request):
    ldgr2 = Ledger_Journal(date=request.POST['date'],reportdate=request.POST['reportdate'],)
    ldgr2.save()
    return redirect( '/')
def goledgermasterdata(request):
    return render(request,'Sam/Ledger Marsterdata.html')
def ldgrmasterdatacreate(request):
    ldgr2 = Ledger_Masterdata(date=request.POST['date'],reportdate=request.POST['reportdate'],)
    ldgr2.save()
    return redirect( '/')
def gostockbalance(request):
    return render(request,'Sam/Stock Balance.html')
def stkbalanceacreate(request):
    stk2 = Stock_Balance(date=request.POST['date'],reportdate=request.POST['reportdate'],)
    stk2.save()
    return redirect( '/')
def goitemstms(request):
    return render(request,'Sam/Item Statement.html')
def itemstmtcreate(request):
    itm2 = Item_Statement(date=request.POST['date'],item_id=request.POST['item_id'],item_name=request.POST['item_name'],period=request.POST['period'],)
    itm2.save()
    return redirect( '/')
def gostockadj(request):
    return render(request,'Sam/Stock Adjustment.html')
def stockadjcreate(request):
    stk2 = Stock_Adjustment(date=request.POST['date'], reportdate=request.POST['reportdate'], )
    stk2.save()
    return redirect('/')
def gostockmaster(request):
    return render(request,'Sam/Stock Masterdata.html')
def stockmastercreate(request):
    stk2 = Stock_Masterdata(date=request.POST['date'], reportdate=request.POST['reportdate'], )
    stk2.save()
    return redirect('/')
def gojobstms(request):
    return render(request,'Sam/Job Statement.html')
def jobstmtcreate(request):
    job2 = job_Statement(date=request.POST['date'],job=request.POST['job'],job_id=request.POST['job_id'],period=request.POST['period'],)
    job2.save()
    return redirect( '/')
def gojobmaster(request):
    return render(request,'Sam/Job Masterdate.html')
def jobmastercreate(request):
    job2 = job_Masterdata(date=request.POST['date'], reportdate=request.POST['reportdate'], )
    job2.save()
    return redirect('/')


def gocuststms(request):
    return render(request,'Sam/Customer AccountStatement.html')
def custstmscreate(request):
    # cus1 = Customer_Statement(date=request.POST['date'], report_period=request.POST['report_period'],customer_name= request.POST['customer_name'],customer_id=request.POST['customer_id'],)
    # cus1.save()
    # return redirect('/')

        df = request.POST.get('from_date')
        dt = request.POST.get('to_date')
        cid = request.POST.get('customer_id')
        cnm = request.POST.get('customer_name')
       

        demop = Receipt.objects.filter(date__range=[dt,df])  
        demoac = demop.filter(customer_name=cnm,customer_id=cid)
        context = {'demoac': demoac}
        return render(request,'Sam/Customer AccountStatement.html', context)


    # custid = request.POST.get('customer_id')
    # # custnm = request.POST.get('customer_name')
    # report1 = Receipt.objects.all()
    # report = report1.filter(customer_id = custid)
    # context = {'report': report}
    #return render(request,'Sam/Customer AccountStatement.html', context)


def gocustouts(request):
    return render(request,'Sam/Customer Outstanding.html')
def custoutscreate(request):
    # cus1 = Customer_Outstand(date=request.POST['date'], report_date=request.POST['report_date'],customer_name= request.POST['customer_name'],customer_id=request.POST['customer_id'],)
    # cus1.save()
    # return redirect('/')

        df = request.POST.get('from_date')
        dt = request.POST.get('to_date')
        cid = request.POST.get('customer_id')
        cnm = request.POST.get('customer_name')
       

        demop = Receipt.objects.filter(date__range=[df,dt])  
        demoac = demop.filter(customer_name=cnm,customer_id=cid)
        context = {'demoac': demoac}
        return render(request,'Sam/Customer Outstanding.html', context)


    # custid = request.POST.get('customer_id')
    # # custnm = request.POST.get('customer_name')
    # report1 = Receipt.objects.all()
    # report = report1.filter(customer_id = custid)
    # context = {'report': report}
    # return render(request,'Sam/Customer Outstanding.html', context)


def gocustinvo(request):
    return render(request,'Sam/Customer InvoiceHistory.html')
def custinvocreate(request):


        df = request.POST.get('report_date')
        invon = request.POST.get('invoice_no')
        cid = request.POST.get('customer_id')
        cnm = request.POST.get('customer_name')
       

        demop = Cash.objects.filter(date=df)  
        demoac = demop.filter(customer_name=cnm,customer_id=cid,invoice_number=invon)
        context = {'demoac': demoac}
        return render(request,'Sam/Customer InvoiceHistory.html', context)

    # cus1 = Customer_Invoice(invoice_no=request.POST['invoice_no'], report_date=request.POST['report_date'],customer_name= request.POST['customer_name'],customer_id=request.POST['customer_id'],)
    # cus1.save()
    #return redirect('/')
def gocustrecpt(request):
    return render(request,'Sam/Customer ReceiptHistory.html')
def custrecptcreate(request):

        df = request.POST.get('report_date')
        recn = request.POST.get('receipt_no')
        cid = request.POST.get('customer_id')
        cnm = request.POST.get('customer_name')
       

        demop = Cash.objects.filter(date=df)  
        demoac = demop.filter(customer_name=cnm,customer_id=cid)
        context = {'demoac': demoac}
        return render(request,'Sam/Customer ReceiptHistory.html', context)

    # cus1 = Customer_Receipt(receipt_no=request.POST['receipt_no'], report_date=request.POST['report_date'],customer_name= request.POST['customer_name'],customer_id=request.POST['customer_id'],)
    # cus1.save()
    # return redirect('/')
def gocustinvorecpt(request):
    return render(request,'Sam/CustomerInvoice ReceiptsReg.html')
def custinvorecptcreate(request):

    
        df = request.POST.get('from_date')
        dt = request.POST.get('to_date')
        demoac =  Cash.objects.filter(date__range=[df,dt]) 
        context = {'demoac': demoac}
        return render(request,'Sam/CustomerInvoice ReceiptsReg.html', context)



    # cus1 = Customer_Invoice_Receipt(date=request.POST['date'], report_date=request.POST['report_date'],)
    # cus1.save()
    # return redirect('/')
def gocustrmasterdata(request):
    return render(request,'Sam/Customer Masterdata.html')
def custrmasterdatacreate(request):
    # ldgr2 = Customer_Masterdata(date=request.POST['date'],report_date=request.POST['report_date'],)
    # ldgr2.save()

        df = request.POST.get('from_date')
        dt = request.POST.get('to_date')
        demoac =  Customer.objects.filter(created_at__range=[df,dt]) 
        context = {'demoac': demoac}
        return render(request,'Sam/Customer Masterdata.html', context)
    
    #   if request.method == 'POST':
    #     dat = request.GET.get('date')
    #     # ldgr2 = Customer_Masterdata(date=request.POST['date'],report_date=request.POST['report_date'],)
    # # ldgr2.save()
    # # return redirect( 'CustomerMasterdataReport')
    
    # # ldgr2.date = request.POST.get['date']
    
    
    #     report = Customer.objects.filter(created_at=dat)
    #     # cust = Customer.objects.filter(created_at=date).first()
    #     if dat == Customer.created_at:
            
    #         # context = {'report':report}
    #         return render(request,'Sam/Customer Masterdata.html',{'report':report})  
    #     #     return render(request,'Sam/Customer Masterdata.html', {'report':report})
       
          
    #     return HttpResponse('Admin Login Successfully')

   


def gosupstms(request):
    return render(request,'Sam/Supplier AccountStatement.html')
def supstmscreate(request):
    # cus1 = Supplier_Statement(date=request.POST['date'], report_period=request.POST['report_period'],Supplier_name= request.POST['Supplier_name'],Supplier_id=request.POST['Supplier_id'],)
    # cus1.save()
    # return redirect('/')

    custid = request.POST.get('Supplier_id')
    # custnm = request.POST.get('customer_name')
    report1 = PReceipt.objects.all()
    report = report1.filter(supp_id = custid)
    context = {'report': report}
    return render(request,'Sam/Supplier AccountStatement.html', context)


def gosupouts(request):
    return render(request,'Sam/Supplier Outstanding.html')
def supoutscreate(request):
    # cus1 = Supplier_Outstand(date=request.POST['date'], report_date=request.POST['report_date'],Supplier_name= request.POST['Supplier_name'],Supplier_id=request.POST['Supplier_id'],)
    # cus1.save()
    # return redirect('/')

    custid = request.POST.get('Supplier_id')
    # custnm = request.POST.get('customer_name')
    report1 = PReceipt.objects.all()
    report = report1.filter(supp_id = custid)
    context = {'report': report}
    return render(request,'Sam/Supplier Outstanding.html', context)


def gosupinvo(request):
    return render(request,'Sam/Supplier InvoiceHistory.html')
def supinvocreate(request):
    cus1 = Supplier_Invoice(invoice_no=request.POST['invoice_no'], report_date=request.POST['report_date'],Supplier_name= request.POST['Supplier_name'],Supplier_id=request.POST['Supplier_id'],)
    cus1.save()
    return redirect('/')
def gosuprecpt(request):
    return render(request,'Sam/Payment History.html')
def suprecptcreate(request):
    cus1 = payment_History(voucher_no=request.POST['voucher_no'], report_date=request.POST['report_date'],Supplier_name= request.POST['Supplier_name'],Supplier_id=request.POST['Supplier_id'],)
    cus1.save()
    return redirect('/')
def gosupinvorecpt(request):
    return render(request,'Sam/SupplierInvoice ReceiptReg.html')
def supinvorecptcreate(request):
    cus1 = Supplier_Invoice_Receipt(date=request.POST['date'], report_date=request.POST['report_date'],)
    cus1.save()
    return redirect('/')
def gosupmasterdata(request):
    return render(request,'Sam/Supplier Masterdata.html')
def supmasterdatacreate(request):
    # ldgr2 = Supplier_Masterdata(date=request.POST['date'],report_date=request.POST['report_date'],)
    # ldgr2.save()

    dt = request.POST.get('date')
    report1 = Supplier.objects.all()
    report = report1.filter(created_at = dt)
    context = {'report': report}
    return render(request,'Sam/Supplier Masterdata.html', context)

# def CustomerMasterdataReport(request):
#     report = Customer.objects.all()
#     if request.method == 'POST':
#         date = request.POST.get['date']
#         cust = Customer.objects.filter(created_at=date).first()
#         if cust is None:
#             raise AuthenticationFailed('No data')
        
#     context = {'report':report}

#     return render(request,'Sam/Customer Masterdata.html', context)

# if request.method == 'POST':
#         ldgr2.date = request.POST.get['date']
#         report = Customer.objects.all()
       
#         cust = Customer.objects.filter(created_at=ldgr2.date ).first()
#         if cust is None:
#             raise AuthenticationFailed('No data')
#         else:
#             context = {'report':report}

#     return render(request,'Sam/Customer Masterdata.html', context)



# API 

# class LiabilityApi(APIView):
#     serializer_class = LiabilitySerializer
    
#     def post(self,request):
#         Serializer = LiabilitySerializer(data=request.data)
#         if Serializer.is_valid():
#             Serializer.save()
#             return Response(Serializer.data, status=status.HTTP_201_CREATED)

#         return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class LiabilityEditApi(APIView):
#     def get_object (self,id):
#         try:
#             return Liabilities.objects.get(id=id)
#         except:
#             raise Http404
    
#     def get(self,request,id,format =None):
#         L_data = self.get_object(id)
#         Serializer =LiabilitySerializer(L_data)
#         return Response(Serializer.data)
    
#     def patch(self,request,id,format =None):
#          L_data = self.get_object(id)
#          Serializer =LiabilitySerializer(L_data,data=request.data)
#          if Serializer.is_valid():
#             Serializer.save()
#             return Response(Serializer.data, status=status.HTTP_201_CREATED)
#          return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id, format=None):
#         L_data = self.get_object(id)
#         L_data.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT) 


# 
#         
       
#         demop=DemoPCash.objects.filter(account=nm )  
#         demoac = demop.filter(date__range=[df, dt]) 
       
#         dmo = DemoPCash.objects.filter(ledger_name =nm ) 
#         demol = dmo.filter(date__range=[df, dt])

#         # demodb = DemoPCash.objects.all()
#          # r = Ledger.objects.filter(created_at__range=[df, dt])
#         #demo1=demop.annotate(Sum(F('cash')) )

        
#         #job.objects.filter(query)
       
#         ##  DemoPCash.objects.filter(ledger_name=nm )
#         #demol=demo.filter(account = nm) , demo.filter(ledger_name = nm)
       
#         #demol=
#         ledger=request.POST.get('opening_bal')
#         a=123
#         b=12
#         c=(a+b)
#         return render(request,'Sam/ledger statement.html',{"c":c,"groups": groups,
#         "ledgers":ledgers,
#         "subLedgers": subLedgers,
#         "category":category,
#         "ledgers":ledgers,
#         "sundry_debtors": sundry_debtors,
#         "sundry_creditors": sundry_creditors,
#         "cash_sale":cash_sale,
#         "pcash":pcash,
#         "demoac":demoac,
#         #"demo":demo,
#         "demol":demol,
#         #"demodb":demodb,
        
#         #"demop":demop,
#         #"demo1":demo1,
#         #"demo":demo3,
#         #"closing_stock": closing_stock,"r":r
#         })


####  API ######


       


class RegisterApi(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApi(APIView):
    serializer_class = LoginSerializer
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
       
        
        user = User.objects.filter(username=username).first()
        user1 = User.objects.filter(password=password).first()
        #user2 = User.objects.filter(username='admin', password='Admin@1234').first()
        
        if (username == 'admin' and password == 'Admin@1234') :
            return HttpResponse('Admin Login Successfully')
        
        else :
            if user is None :
                raise AuthenticationFailed('User not found!')

        
            if not user1:
                raise AuthenticationFailed('Incorrect password!')
        
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            return HttpResponse('User Login Successfully')
            token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')


            response = Response()

            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
             'jwt': token
             }
            return response


class UserApi(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutApi(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class ItemApi(APIView):
    serializer_class = ItemSerializer
    
    def post(self,request):
        Serializer = ItemSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ItemEditApi(APIView):
    def get_object (self,id):
        try:
            return Item.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        item_data = self.get_object(id)
        Serializer =ItemSerializer(item_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
         item_data = self.get_object(id)
         Serializer =ItemSerializer(item_data,data=request.data)
         if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)
         return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        item_data = self.get_object(id)
        item_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

  




class CustomerApi(APIView):
    serializer_class = CustomerSerializer
    def post(self,request):
        Serializer = CustomerSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerEditApi(APIView):
    def get_object (self,id):
        try:
            return Customer.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        cust_data = self.get_object(id)
        Serializer =CustomerSerializer(cust_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
        cust_data = self.get_object(id)
        Serializer =CustomerSerializer(cust_data,data=request.data)
        if Serializer.is_valid():
           Serializer.save()
           return Response(Serializer.data, status=status.HTTP_201_CREATED)
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        cust_data = self.get_object(id)
        cust_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class SupplierApi(APIView):
    serializer_class = SupplierSerializer
    def post(self,request):
        Serializer = SupplierSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierEditApi(APIView):
    def get_object (self,id):
        try:
            return Supplier.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        sup_data = self.get_object(id)
        Serializer =SupplierSerializer(sup_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
        sup_data = self.get_object(id)
        Serializer =SupplierSerializer(sup_data,data=request.data)
        if Serializer.is_valid():
           Serializer.save()
           return Response(Serializer.data, status=status.HTTP_201_CREATED)
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        sup_data = self.get_object(id)
        sup_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

class JobApi(APIView):
    serializer_class = JobSerializer
    def post(self,request):
        Serializer = JobSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobEditApi(APIView):
    def get_object (self,id):
        try:
            return Job.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        job_data = self.get_object(id)
        Serializer =JobSerializer(job_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
        job_data = self.get_object(id)
        Serializer =JobSerializer(job_data,data=request.data)
        if Serializer.is_valid():
           Serializer.save()
           return Response(Serializer.data, status=status.HTTP_201_CREATED)
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        job_data = self.get_object(id)
        job_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 



class EmployeeApi(APIView):
    serializer_class = EmployeeSerializer
    def post(self,request):
        Serializer = EmployeeSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeEditApi(APIView):
    def get_object (self,id):
        try:
            return Employee.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        emp_data = self.get_object(id)
        Serializer =EmployeeSerializer(emp_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
        emp_data = self.get_object(id)
        Serializer =EmployeeSerializer(emp_data,data=request.data)
        if Serializer.is_valid():
           Serializer.save()
           return Response(Serializer.data, status=status.HTTP_201_CREATED)
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        emp_data = self.get_object(id)
        emp_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


       

class CompanyApi(APIView):
    serializer_class = CompanySerializer
    
    def post(self,request):
        Serializer = CompanySerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CompanyEditApi(APIView):
    def get_object (self,id):
        try:
            return Company.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        L_data = self.get_object(id)
        Serializer =CompanySerializer(L_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
         L_data = self.get_object(id)
         Serializer =CompanySerializer(L_data,data=request.data)
         if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)
         return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        L_data = self.get_object(id)
        L_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 







class CashApi(APIView):
    serializer_class = CashSerializer
    
    def post(self,request):
        Serializer = CashSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CashEditApi(APIView):
    def get_object (self,id):
        try:
            return Cash.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        L_data = self.get_object(id)
        Serializer =CashSerializer(L_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
         L_data = self.get_object(id)
         Serializer =CashSerializer(L_data,data=request.data)
         if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)
         return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        L_data = self.get_object(id)
        L_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 





class CreditApi(APIView):
    serializer_class = CreditSerializer
    
    def post(self,request):
        Serializer = CreditSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreditEditApi(APIView):
    def get_object (self,id):
        try:
            return Credit.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        L_data = self.get_object(id)
        Serializer =CreditSerializer(L_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
         L_data = self.get_object(id)
         Serializer =CreditSerializer(L_data,data=request.data)
         if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)
         return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        L_data = self.get_object(id)
        L_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class Sales_ReturnApi(APIView):
    serializer_class = Sales_ReturnSerializer
    
    def post(self,request):
        Serializer = Sales_ReturnSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Sales_ReturnEditApi(APIView):
    def get_object (self,id):
        try:
            return Sales_Return.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        L_data = self.get_object(id)
        Serializer =Sales_ReturnSerializer(L_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
         L_data = self.get_object(id)
         Serializer =Sales_ReturnSerializer(L_data,data=request.data)
         if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)
         return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        L_data = self.get_object(id)
        L_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 



class ReceiptApi(APIView):
    serializer_class = ReceiptSerializer
    
    def post(self,request):
        Serializer = ReceiptSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReceiptEditApi(APIView):
    def get_object (self,id):
        try:
            return Receipt.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        L_data = self.get_object(id)
        Serializer =ReceiptSerializer(L_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
         L_data = self.get_object(id)
         Serializer =ReceiptSerializer(L_data,data=request.data)
         if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)
         return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        L_data = self.get_object(id)
        L_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 



class PCashApi(APIView):
    serializer_class = PCashSerializer
    
    def post(self,request):
        Serializer = PCashSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PCashEditApi(APIView):
    def get_object (self,id):
        try:
            return PCash.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        L_data = self.get_object(id)
        Serializer =PCashSerializer(L_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
         L_data = self.get_object(id)
         Serializer =PCashSerializer(L_data,data=request.data)
         if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)
         return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        L_data = self.get_object(id)
        L_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class PCreditApi(APIView):
    serializer_class = PCreditSerializer
    
    def post(self,request):
        Serializer = PCreditSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class  PCreditEditApi(APIView):
    def get_object (self,id):
        try:
            return PCredit.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        L_data = self.get_object(id)
        Serializer =PCreditSerializer(L_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
         L_data = self.get_object(id)
         Serializer =PCreditSerializer(L_data,data=request.data)
         if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)
         return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        L_data = self.get_object(id)
        L_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 



class PRSales_ReturnApi(APIView):
    serializer_class = PRSales_ReturnSerializer
    
    def post(self,request):
        Serializer = PRSales_ReturnSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class  PRSales_ReturnEditApi(APIView):
    def get_object (self,id):
        try:
            return PRSales_Return.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        L_data = self.get_object(id)
        Serializer =PRSales_ReturnSerializer(L_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
         L_data = self.get_object(id)
         Serializer =PRSales_ReturnSerializer(L_data,data=request.data)
         if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)
         return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        L_data = self.get_object(id)
        L_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 




class PReceiptApi(APIView):
    serializer_class = PReceiptSerializer
    
    def post(self,request):
        Serializer = PReceiptSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class  PReceiptEditApi(APIView):
    def get_object (self,id):
        try:
            return PReceipt.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        L_data = self.get_object(id)
        Serializer =PReceiptSerializer(L_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
         L_data = self.get_object(id)
         Serializer =PRSales_ReturnSerializer(L_data,data=request.data)
         if Serializer.is_valid():
            Serializer.save()
            self.updated_at = timezone.now()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)
         return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # def save(self, *args, **kwargs):
        #     self.updated_at = timezone.now()
        #     return super().save(*args, **kwargs)

    def delete(self, request, id, format=None):
        L_data = self.get_object(id)
        L_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 




class GroupApi(APIView):
    serializer_class = GroupSerializer
    def post(self,request):
        Serializer = GroupSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupEditApi(APIView):
    def get_object (self,id):
        try:
            return Group.objects.get(id=id)
        except:
            raise Http404
    
    def get(self,request,id,format =None):
        group_data = self.get_object(id)
        Serializer =GroupSerializer(group_data)
        return Response(Serializer.data)
    
    def patch(self,request,id,format =None):
        group_data = self.get_object(id)
        Serializer =GroupSerializer(group_data,data=request.data)
        if Serializer.is_valid():
           Serializer.save()
           return Response(Serializer.data, status=status.HTTP_201_CREATED)
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        group_data = self.get_object(id)
        group_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
        






def cutomercreate(request):
    cust2 = Customer(customer_name=request.POST['customer_name'],vat_reg_no=request.POST['vat_reg_no'],cr_no=request.POST['cr_no'],expired_on=request.POST['expired_on'],land_phone=request.POST['land_phone'],mobile=request.POST['mobile'],contact_person=request.POST['contact_person'],contact_mobile=request.POST['contact_mobile'],email=request.POST['email'],address=request.POST['address'],open_balance=request.POST['open_balance'],credit_lim_am=request.POST['credit_lim_am'],credit_lim_dur=request.POST['credit_lim_dur'],)
    cust2.save()
    return redirect( '/')
def custview(request):
    cust1 = Customer.objects.all()
    context = {'cust': cust1}
    return render(request,'Sam/customer view.html', context)
def editcust(request,id):
    cust1 = Customer.objects.get(id=id)
    context = {'cust': cust1}
    return render(request,'Sam/edit customer.html',context)
def updatecust(request,id):
    cust = Customer.objects.get(id=id)
    cust.customer_name=request.POST['customer_name']
    cust.vat_reg_no = request.POST['vat_reg_no']
    cust.cr_no = request.POST['cr_no']
    cust.expired_on = request.POST['expired_on']
    cust.land_phone = request.POST['land_phone']
    cust.mobile = request.POST['mobile']
    cust.contact_person = request.POST['contact_person']
    cust.contact_mobile = request.POST['contact_mobile']
    cust.email = request.POST['email']
    cust.address = request.POST['address']
    cust.open_balance = request.POST['open_balance']
    cust.credit_lim_am = request.POST['credit_lim_am']
    cust.credit_lim_dur = request.POST['credit_lim_dur']
    cust.updated_at = datetime.now().replace(microsecond=0)
    cust.save()
    
    return render(request, 'Sam/dashboard.html')
def deletecust(request, id):
    cust = Customer.objects.get(id=id)
    cust.delete()
    return render(request, 'Sam/dashboard.html')




def gosupp(request):
    return render(request,'Sam/supplier.html')
def suppcreate(request):
    supp2 = Supplier(customer_name=request.POST['customer_name'],vat_reg_no=request.POST['vat_reg_no'],cr_no=request.POST['cr_no'],expired_on=request.POST['expired_on'],land_phone=request.POST['land_phone'],mobile=request.POST['mobile'],contact_person=request.POST['contact_person'],contact_mobile=request.POST['contact_mobile'],email=request.POST['email'],address=request.POST['address'],open_balance=request.POST['open_balance'],credit_lim_am=request.POST['credit_lim_am'],credit_lim_dur=request.POST['credit_lim_dur'],bank_acc_name=request.POST['bank_acc_name'],bank_acc_no=request.POST['bank_acc_no'],)
    supp2.save()
    return redirect( '/')
def suppview(request):
    supp1 = Supplier.objects.all()
    context = {'supp': supp1}
    return render(request,'Sam/supplier view.html', context)
def editsupp(request,id):
    supp1 = Supplier.objects.get(id=id)
    context = {'supp': supp1}
    return render(request,'Sam/edit supplier.html', context)
def updatesupp(request,id):
    supp = Supplier.objects.get(id=id)
    supp.customer_name=request.POST['customer_name']
    supp.vat_reg_no = request.POST['vat_reg_no']
    supp.cr_no = request.POST['cr_no']
    supp.expired_on = request.POST['expired_on']
    supp.land_phone = request.POST['land_phone']
    supp.mobile = request.POST['mobile']
    supp.contact_person = request.POST['contact_person']
    supp.contact_mobile = request.POST['contact_mobile']
    supp.email = request.POST['email']
    supp.address = request.POST['address']
    supp.open_balance = request.POST['open_balance']
    supp.credit_lim_am = request.POST['credit_lim_am']
    supp.credit_lim_dur = request.POST['credit_lim_dur']
    supp.bank_acc_name = request.POST['bank_acc_name']
    supp.bank_acc_no = request.POST['bank_acc_no']
    supp.updated_at = datetime.now().replace(microsecond=0)
    supp.save()
    return render(request, 'Sam/dashboard.html')
def deletesupp(request, id):
    supp = Supplier.objects.get(id=id)
    supp.delete()
    return render(request, 'Sam/dashboard.html')


def goitem(request):
    return render(request,'Sam/item.html')
def createitem(request):
    if request.method == "POST":
        item_name = request.POST['item_name']
        item_desc = request.POST['item_desc']
        item_barcode = request.POST['item_barcode']
        item_category = request.POST['item_category']
        item_unit_prim = request.POST['item_unit_prim']
        item_unit_sec = request.POST['item_unit_sec']
        open_balance = request.POST['open_balance']
        buying_price = request.POST['buying_price']
        sell_price = request.POST['sell_price']
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')

        itm = Item.objects.create(item_name=item_name, item_desc=item_desc, item_barcode=item_barcode,
                                     item_category=item_category, item_unit_prim=item_unit_prim,item_unit_sec=item_unit_sec,
                                  open_balance=open_balance, buying_price=buying_price,
                                     sell_price=sell_price, image1=image1, image2=image2, image3=image3, image4=image4,)

        return redirect('go')





def itemview(request):
    itm = Item.objects.all()
    return render(request, 'Sam/item view.html', {'itmview': itm})
def edititem(request,id):
    itm = Item.objects.get(id=id)
    context = {'itmview': itm}
    return render(request,'Sam/edit item.html', context)
def updateitem(request,id):
    itm = Item.objects.get(id=id)
    form = ItemForm(request.POST, instance=itm)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'Sam/dashboard.html', {'itmview': itm})
def deleteitem(request, id):
    itm = Item.objects.get(id=id)
    itm.delete()
    return render(request, 'Sam/dashboard.html')



def gojob(request):
    return render(request,'Sam/job.html')
def createjob(request):
    if request.method == "POST":
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect(request, 'Sam/dashboard.html')
            except:
                pass

    else:
        form = JobForm()
    return render(request, 'Sam/dashboard.html', {'form': form})
def jobview(request):
    job = Job.objects.all()
    return render(request, 'Sam/job view.html', {'jobview': job})
def editjob(request,id):
    job = Job.objects.get(id=id)
    context = {'jobview': job}
    return render(request,'Sam/edit job.html', context)
def updatejob(request,id):
    job = Job.objects.get(id=id)
    form = JobForm(request.POST, instance=job)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'Sam/dashboard.html', {'jobview': job})
def deletejob(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return render(request, 'Sam/dashboard.html')




def groupview(request):
    grp1 = Group.objects.all()
    context = {'grp': grp1}
    return render(request,'Sam/group view.html', context)
def editgroup(request,id):
    grp1 = Group.objects.get(id=id)
    context = {'grp': grp1}
    return render(request,'Sam/edit group.html', context)
def updategroup(request,id):
    grp = Group.objects.get(id=id)
    grp.group_name=request.POST['group_name']
    grp.category = request.POST['category']

    grp.save()
    return render(request, 'Sam/dashboard.html')
def deletegroup(request, id):
    grp = Group.objects.get(id=id)
    grp.delete()
    return render(request, 'Sam/dashboard.html')




# def goledger(request):
#     return render(request,'Sam/ledger.html')
# def ledgercreate(request):
#     ldg2 = Ledger(ledger_name=request.POST['ledger_name'],group_name=request.POST['group_name'],category=request.POST['category'],opening_bal=request.POST['opening_bal'],)
#     ldg2.save()
#     return redirect( '/')
def ledgerview(request):
    ldg1 = Ledger.objects.all()
    context = {'ldg': ldg1}
    return render(request,'Sam/ledger view.html', context)
def editledger(request,id):
    ldg1 = Ledger.objects.get(id=id)
    context = {'ldg': ldg1}
    return render(request,'Sam/edit ledger.html', context)
def updateledger(request,id):
    ldg = Ledger.objects.get(id=id)
    ldg.ledger_name = request.POST['ledger_name']
    ldg.group_name = request.POST['group_name']
    ldg.category = request.POST['category']
    ldg.opening_bal = request.POST['opening_bal']

    ldg.save()
    return render(request, 'Sam/dashboard.html')
def deleteledger(request, id):
    ldg = Ledger.objects.get(id=id)
    ldg.delete()
    return render(request, 'Sam/dashboard.html')



def goemp(request):
    return render(request,'Sam/employee.html')
# def goaccount(request):
#     return render(request,'Sam/chart of account.html')


def assetcreate(request):
    ast2 = Asset(asset_parent=request.POST['asset_parent'],asset_child=request.POST['asset_child'],)
    ast2.save()
    return redirect( '/')

def assetview(request):
    return render(request,'Sam/Add new asset.html')

def goliability(request):
    return render(request,'Sam/Add new liability.html')
def liabilitycreate(request):
    lbt2 = Liabilities(liability_parent=request.POST['liability_parent'],liability_child=request.POST['liability_child'],)
    lbt2.save()
    return redirect( '/')
def goincome(request):
    return render(request,'Sam/Add new income.html')
def incomecreate(request):
    inm2 = Income(income_parent=request.POST['income_parent'],income_child=request.POST['income_child'],)
    inm2.save()
    return redirect( '/')
def goexpences(request):
    return render(request,'Sam/Add new expences.html')
def expencescreate(request):
    exp2 = Expences(expenses_parent=request.POST['expenses_parent'],expenses_child=request.POST['expenses_child'],)
    exp2.save()
    return redirect( '/')


########################################################
def gosales(request):
    return render(request, 'Sam/Sales.html')
def gocashsale(request):
    return render(request, 'Sam/cash sale.html')
def cashcreate(request):
    csh2 = Cash(invoice_number=request.POST['invoice_number'],date=request.POST['date'],
                internal_ref_no=request.POST['internal_ref_no'],cash=request.POST['cash'],
                user_id=request.POST['user_id'],account=request.POST['account'],
                customer_id=request.POST['customer_id'],customer_name=request.POST['customer_name'],
                item_id1=request.POST['item_id1'],item_id2=request.POST['item_id2'],
                item_details1=request.POST['item_details1'],item_details2=request.POST['item_details2'],price=request.POST['price'],price1_2=request.POST['price1_2'],
                quantity2=request.POST['quantity2'],
                amount2=request.POST['amount2'],qty=request.POST['qty'],total=request.POST['total'],
                sales_ex1=request.POST['sales_ex1'], sales_ex2=request.POST['sales_ex2'],
                job1=request.POST['job1'], job2=request.POST['job2'],
                labour_charge=request.POST['labour_charge'], other_charge=request.POST['other_charge'],
                total1=request.POST['total1'], total2=request.POST['total2'],
                total3=request.POST['total3'], total4=request.POST['total4'],discount=request.POST['discount'],)
    csh2.save()
    democash = DemoPCash(account=request.POST['account'],cash=request.POST['cash'],date=request.POST['date'],ledger_name='Sales Ledger')
    democash.save()


    return redirect( '/')
def cashview(request):
    csh1 = Cash.objects.all()
    context = {'csh': csh1}
    return render(request,'Sam/show cash sales.html', context)
def editcash(request,id):
    csh1 = Cash.objects.get(id=id)
    context = {'csh': csh1}
    return render(request,'Sam/edit cash sales.html', context)
def updatecash(request,id):
    csh = Cash.objects.get(id=id)
    csh.invoice_number = request.POST['invoice_number']
    csh.date = request.POST['date']
    csh.internal_ref_no = request.POST['internal_ref_no']
    csh.cash = request.POST['cash']
    csh.user_id = request.POST['user_id']
    csh.account = request.POST['account'],
    csh.customer_id = request.POST['customer_id']
    csh.customer_name = request.POST['customer_name']
    csh.item_id1 = request.POST['item_id1']
    csh.item_id2 = request.POST['item_id2']
    csh.item_details1 = request.POST['item_details1']
    csh.item_details2 = request.POST['item_details2']
    csh.price = request.POST['price']
    csh.price1_2 = request.POST['price1_2']
    csh.qty = request.POST['qty']
    csh.quantity2 = request.POST['quantity2']
    csh.total = request.POST['total']
    csh.amount2 = request.POST['amount2']
    csh.sales_ex1 = request.POST['sales_ex1']
    csh.sales_ex2 = request.POST['sales_ex2']
    csh.job1 = request.POST['job1']
    csh.job2 = request.POST['job2']
    csh.labour_charge = request.POST['labour_charge']
    csh.other_charge = request.POST['other_charge']
    csh.total1 = request.POST['total1']
    csh.total2 = request.POST['total2']
    csh.total3 = request.POST['total3']
    csh.total4 = request.POST['total4']
    csh.discount = request.POST['discount']
    csh.save()
    return render(request, 'Sam/Sales.html')
def deletecash(request, id):
    csh = Cash.objects.get(id=id)
    csh.delete()
    return render(request, 'Sam/Sales.html')


def gocreditsale(request):
    return render(request, 'Sam/credit sales.html')
def creditcreate(request):
    crd2 = Credit(invoice_number=request.POST['invoice_number'],date=request.POST['date'],
                internal_ref_no=request.POST['internal_ref_no'],due_on=request.POST['due_on'],
                user_id=request.POST['user_id'],credit_limit_amt=request.POST['credit_limit_amt'],
                account=request.POST['account'],
                customer_id=request.POST['customer_id'],customer_name=request.POST['customer_name'],
                item_id1=request.POST['item_id1'],item_id2=request.POST['item_id2'],
                item_details1=request.POST['item_details1'],item_details2=request.POST['item_details2'],
                price=request.POST['price'],price1_2=request.POST['price1_2'],
                qty=request.POST['qty'],quantity2=request.POST['quantity2'],
                total=request.POST['total'], amount2=request.POST['amount2'],
                sales_ex1=request.POST['sales_ex1'], sales_ex2=request.POST['sales_ex2'],
                job1=request.POST['job1'], job2=request.POST['job2'],
                labour_charge=request.POST['labour_charge'], other_charge=request.POST['other_charge'],
                total1=request.POST['total1'], total2=request.POST['total2'],
                total3=request.POST['total3'], total4=request.POST['total4'],
                discount=request.POST['discount'],)
    crd2.save()
    democash = DemoPCash(account=request.POST['account'],cash=request.POST['total3'],date=request.POST['date'],ledger_name='Customer-ledger')
    democash.save()
    return redirect( '/')
def creditview(request):
    crd1 = Credit.objects.all()
    context = {'crd': crd1}
    return render(request,'Sam/show credit sales.html', context)
def editcredit(request,id):
    crd1 = Credit.objects.get(id=id)
    context = {'crd': crd1}
    return render(request,'Sam/edit credit sales.html', context)
def updatecredit(request,id):
    crd = Credit.objects.get(id=id)
    crd.invoice_number = request.POST['invoice_number']
    crd.date = request.POST['date']
    crd.internal_ref_no = request.POST['internal_ref_no']
    crd.due_on = request.POST['due_on']
    crd.user_id = request.POST['user_id']
    crd.credit_limit_amt = request.POST['credit_limit_amt'],
    crd.customer_id = request.POST['customer_id']
    crd.customer_name = request.POST['customer_name']
    crd.item_id1 = request.POST['item_id1']
    crd.item_id2 = request.POST['item_id2']
    crd.item_details1 = request.POST['item_details1']
    crd.item_details2 = request.POST['item_details2']
    crd.price = request.POST['price']
    crd.price1_2 = request.POST['price1_2']
    crd.qty = request.POST['qty']
    crd.quantity2 = request.POST['quantity2']
    crd.total = request.POST['total']
    crd.amount2 = request.POST['amount2']
    crd.sales_ex1 = request.POST['sales_ex1']
    crd.sales_ex2 = request.POST['sales_ex2']
    crd.job1 = request.POST['job1']
    crd.job2 = request.POST['job2']
    crd.labour_charge = request.POST['labour_charge']
    crd.other_charge = request.POST['other_charge']
    crd.total1 = request.POST['total1']
    crd.total2 = request.POST['total2']
    crd.total3 = request.POST['total3']
    crd.total4 = request.POST['total4']
    crd.discount = request.POST['discount']
    crd.save()
    return render(request, 'Sam/Sales.html')
def deletecredit(request, id):
    crd = Credit.objects.get(id=id)
    crd.delete()
    return render(request, 'Sam/Sales.html')


def gosreturnsale(request):
    return render(request, 'Sam/sales return.html')
def sreturncreate(request):
    rtn2 = Sales_Return(invoice_number=request.POST['invoice_number'],date=request.POST['date'],
                internal_ref_no=request.POST['internal_ref_no'],user_id=request.POST['user_id'],
                customer_id=request.POST['customer_id'],customer_name=request.POST['customer_name'],
                item_id1=request.POST['item_id1'],item_id2=request.POST['item_id2'],
                item_details1=request.POST['item_details1'],item_details2=request.POST['item_details2'],
                price=request.POST['price'],price1_2=request.POST['price1_2'],
                qty=request.POST['qty'],quantity2=request.POST['quantity2'],
                total=request.POST['total'], amount2=request.POST['amount2'],
                sales_ex1=request.POST['sales_ex1'], sales_ex2=request.POST['sales_ex2'],
                job1=request.POST['job1'], job2=request.POST['job2'],
                labour_charge=request.POST['labour_charge'], other_charge=request.POST['other_charge'],
                total1=request.POST['total1'], total2=request.POST['total2'],
                total3=request.POST['total3'], total4=request.POST['total4'],
                discount=request.POST['discount'],)
    rtn2.save()
    return redirect( '/')
def sreturnview(request):
    rtn1 = Sales_Return.objects.all()
    context = {'rtn': rtn1}
    return render(request,'Sam/show sales return.html', context)
def editsreturn(request,id):
    rtn1 = Sales_Return.objects.get(id=id)
    context = {'rtn': rtn1}
    return render(request,'Sam/edit sales return.html', context)
def updatesreturn(request,id):
    rtn = Sales_Return.objects.get(id=id)
    rtn.invoice_number = request.POST['invoice_number']
    rtn.date = request.POST['date']
    rtn.internal_ref_no = request.POST['internal_ref_no']
    rtn.user_id = request.POST['user_id']
    rtn.customer_id = request.POST['customer_id']
    rtn.customer_name = request.POST['customer_name']
    rtn.item_id1 = request.POST['item_id1']
    rtn.item_id2 = request.POST['item_id2']
    rtn.item_details1 = request.POST['item_details1']
    rtn.item_details2 = request.POST['item_details2']
    rtn.price = request.POST['price']
    rtn.price1_2 = request.POST['price1_2']
    rtn.qty = request.POST['qty']
    rtn.quantity2 = request.POST['quantity2']
    rtn.total = request.POST['total']
    rtn.amount2 = request.POST['amount2']
    rtn.sales_ex1 = request.POST['sales_ex1']
    rtn.sales_ex2 = request.POST['sales_ex2']
    rtn.job1 = request.POST['job1']
    rtn.job2 = request.POST['job2']
    rtn.labour_charge = request.POST['labour_charge']
    rtn.other_charge = request.POST['other_charge']
    rtn.total1 = request.POST['total1']
    rtn.total2 = request.POST['total2']
    rtn.total3 = request.POST['total3']
    rtn.total4 = request.POST['total4']
    rtn.discount = request.POST['discount']
    rtn.save()
    return render(request, 'Sam/Sales.html')
def deletesreturn(request, id):
    rtn = Sales_Return.objects.get(id=id)
    rtn.delete()
    return render(request, 'Sam/Sales.html')


def goreceipt(request):
    return render(request, 'Sam/Receipt.html')
def receiptcreate(request):
    rpt2 = Receipt(receipt_number=request.POST['receipt_number'], date=request.POST['date'], internal_ref_no=request.POST['internal_ref_no'],
    due_on=request.POST['due_on'], credit_limit_amt=request.POST['credit_limit_amt'], user_id=request.POST['user_id'],
    customer_id=request.POST['customer_id'], customer_name = request.POST['customer_name'],invoice_no1 = request.POST['invoice_no1'],
    invoice_no2 = request.POST['invoice_no2'],invoice_no3 = request.POST['invoice_no3'],invoice_date1 = request.POST['invoice_date1'],
    invoice_date2 = request.POST['invoice_date2'],invoice_date3 = request.POST['invoice_date3'],duedate1 = request.POST['duedate1'],
    duedate2 = request.POST['duedate2'],duedate3 = request.POST['duedate3'],invoice_amt1 = request.POST['invoice_amt1'],
    invoice_amt2 = request.POST['invoice_amt2'],invoice_amt3 = request.POST['invoice_amt3'],received_amt1 = request.POST['received_amt1'],
    received_amt2 = request.POST['received_amt2'],received_amt3 = request.POST['received_amt3'],outstanding1 = request.POST['outstanding1'],
    outstanding2 = request.POST['outstanding2'],outstanding3 = request.POST['outstanding3'],discount1 = request.POST['discount1'],discount2 = request.POST['discount2'],
    discount3 = request.POST['discount3'],balance_amt1 = request.POST['balance_amt1'],balance_amt2 = request.POST['balance_amt2'],balance_amt3 = request.POST['balance_amt3'],
    tick_space1 = request.POST['tick_space1'],tick_space2 = request.POST['tick_space2'],tick_space3 = request.POST['tick_space3'],partial1 = request.POST['partial1'],
    partial2 = request.POST['partial2'],partial3 = request.POST['partial3'],total1 = request.POST['total1'],account = request.POST['account'],
    total3 = request.POST['total3'],total4 = request.POST['total4'],total5 = request.POST['total5'],total6 = request.POST['total6'],
    on_account = request.POST['on_account'],discount = request.POST['discount'],)
    rpt2.save()
    democash = DemoPCash(account=request.POST['account'],cash=request.POST['total5'],date=request.POST['date'],ledger_name='Sales Ledger')
    democash.save()
    return redirect('/')


def receiptview(request):
    rpt1 = Receipt.objects.all()
    context = {'rpt': rpt1}
    return render(request,'Sam/Show receipt.html', context)
def editreceipt(request,id):
    rpt1 = Receipt.objects.get(id=id)
    context = {'rpt': rpt1}
    return render(request,'Sam/edit receipt.html', context)
def updatereceipt(request,id):
    rpt = Receipt.objects.get(id=id)
    rpt.receipt_number=request.POST['receipt_number']
    rpt.date = request.POST['date']
    rpt.internal_ref_no = request.POST['internal_ref_no']
    rpt.due_on = request.POST['due_on']
    rpt.credit_limit_amt = request.POST['credit_limit_amt']
    rpt.user_id = request.POST['user_id']
    rpt.customer_id = request.POST['customer_id']
    rpt.customer_name = request.POST['customer_name']
    rpt.invoice_no1 = request.POST['invoice_no1']
    rpt.invoice_no2 = request.POST['invoice_no2']
    rpt.invoice_no3 = request.POST['invoice_no3']
    rpt.invoice_date1 = request.POST['invoice_date1']
    rpt.invoice_date2 = request.POST['invoice_date2']
    rpt.invoice_date3 = request.POST['invoice_date3']
    rpt.duedate1 = request.POST['duedate1']
    rpt.invoice_amt2 = request.POST['invoice_amt2']
    rpt.invoice_amt3 = request.POST['invoice_amt3']
    rpt.received_amt1 = request.POST['received_amt1']
    rpt.received_amt2 = request.POST['received_amt2']
    rpt.received_amt3 = request.POST['received_amt3']
    rpt.outstanding1 = request.POST['outstanding1']
    rpt.outstanding2 = request.POST['outstanding2']
    rpt.outstanding3 = request.POST['outstanding3']
    rpt.discount1 = request.POST['discount1']
    rpt.discount2 = request.POST['discount2']
    rpt.discount3 = request.POST['discount3']
    rpt.balance_amt1 = request.POST['balance_amt1']
    rpt.balance_amt2 = request.POST['balance_amt2']
    rpt.balance_amt3 = request.POST['balance_amt3']
    rpt.tick_space1 = request.POST['tick_space1']
    rpt.tick_space2 = request.POST['tick_space2']
    rpt.tick_space3 = request.POST['tick_space3']
    rpt.partial1 = request.POST['partial1']
    rpt.partial2 = request.POST['partial2']
    rpt.partial3 = request.POST['partial3']
    rpt.total1 = request.POST['total1']
    rpt.total2 = request.POST['total2']
    rpt.total3 = request.POST['total3']
    rpt.total4 = request.POST['total4']
    rpt.total5 = request.POST['total5']
    rpt.total6 = request.POST['total6']
    rpt.on_account = request.POST['on_account']
    rpt.discount = request.POST['discount']

    rpt.save()
    return render(request, 'Sam/Sales.html')
def deletereceipt(request, id):
    rpt = Receipt.objects.get(id=id)
    rpt.delete()
    return render(request, 'Sam/Sales.html')






def gopsales(request):
    return render(request, 'Sam/purchase.html')
def gopcashsale(request):
    return render(request, 'Sam/cash purchase.html')
def pcashcreate(request):
    csh2 = PCash(invoice_number=request.POST['invoice_number'],date=request.POST['date'],
                internal_ref_no=request.POST['internal_ref_no'],cash=request.POST['cash'],
                user_id=request.POST['user_id'],account=request.POST['account'],
                supp_id=request.POST['supp_id'],supp_name=request.POST['supp_name'],
                item_id1=request.POST['item_id1'],item_id2=request.POST['item_id2'],
                item_details1=request.POST['item_details1'],item_details2=request.POST['item_details2'],price=request.POST['price'],price1_2=request.POST['price1_2'],
                quantity2=request.POST['quantity2'],
                amount2=request.POST['amount2'],qty=request.POST['qty'],total=request.POST['total'],
                sales_ex1=request.POST['sales_ex1'], sales_ex2=request.POST['sales_ex2'],
                job1=request.POST['job1'], job2=request.POST['job2'],
                labour_charge=request.POST['labour_charge'], other_charge=request.POST['other_charge'],
                total1=request.POST['total1'], total2=request.POST['total2'],
                total3=request.POST['total3'], total4=request.POST['total4'],discount=request.POST['discount'],)
    csh2.save()

    democash = DemoPCash(account=request.POST['account'],cash=request.POST['cash'],date=request.POST['date'],ledger_name='Cash-in-hand')
    democash.save()

    
    return redirect( '/')
def pcashview(request):
    csh1 = PCash.objects.all()
    context = {'csh': csh1}
    return render(request,'Sam/show cash purchase.html', context)
def editpcash(request,id):
    csh1 = PCash.objects.get(id=id)
    context = {'csh': csh1}
    return render(request,'Sam/edit cash purchase.html', context)
def updatepcash(request,id):
    csh = PCash.objects.get(id=id)
    csh.invoice_number = request.POST['invoice_number']
    csh.date = request.POST['date']
    csh.internal_ref_no = request.POST['internal_ref_no']
    csh.cash = request.POST['cash']
    csh.user_id = request.POST['user_id']
    csh.account = request.POST['account'],
    csh.supp_id = request.POST['supp_id']
    csh.supp_name = request.POST['supp_name']
    csh.item_id1 = request.POST['item_id1']
    csh.item_id2 = request.POST['item_id2']
    csh.item_details1 = request.POST['item_details1']
    csh.item_details2 = request.POST['item_details2']
    csh.price = request.POST['price']
    csh.price1_2 = request.POST['price1_2']
    csh.qty = request.POST['qty']
    csh.quantity2 = request.POST['quantity2']
    csh.total = request.POST['total']
    csh.amount2 = request.POST['amount2']
    csh.sales_ex1 = request.POST['sales_ex1']
    csh.sales_ex2 = request.POST['sales_ex2']
    csh.job1 = request.POST['job1']
    csh.job2 = request.POST['job2']
    csh.labour_charge = request.POST['labour_charge']
    csh.other_charge = request.POST['other_charge']
    csh.total1 = request.POST['total1']
    csh.total2 = request.POST['total2']
    csh.total3 = request.POST['total3']
    csh.total4 = request.POST['total4']
    csh.discount = request.POST['discount']
    csh.save()
    return render(request, 'Sam/purchase.html')
def deletepcash(request, id):
    csh = PCash.objects.get(id=id)
    csh.delete()
    return render(request, 'Sam/purchase.html')


def gopcreditsale(request):
    return render(request, 'Sam/credit purchase.html')
def pcreditcreate(request):
    crd2 = PCredit(invoice_number=request.POST['invoice_number'],date=request.POST['date'],
                internal_ref_no=request.POST['internal_ref_no'],due_on=request.POST['due_on'],
                user_id=request.POST['user_id'],credit_limit_amt=request.POST['credit_limit_amt'],account=request.POST['account'],
                supp_id=request.POST['supp_id'],supp_name=request.POST['supp_name'],
                item_id1=request.POST['item_id1'],item_id2=request.POST['item_id2'],
                item_details1=request.POST['item_details1'],item_details2=request.POST['item_details2'],
                price=request.POST['price'],price1_2=request.POST['price1_2'],
                qty=request.POST['qty'],quantity2=request.POST['quantity2'],
                total=request.POST['total'], amount2=request.POST['amount2'],
                sales_ex1=request.POST['sales_ex1'], sales_ex2=request.POST['sales_ex2'],
                job1=request.POST['job1'], job2=request.POST['job2'],
                labour_charge=request.POST['labour_charge'], other_charge=request.POST['other_charge'],
                total1=request.POST['total1'], total2=request.POST['total2'],
                total3=request.POST['total3'], total4=request.POST['total4'],
                discount=request.POST['discount'],)
    crd2.save()
    democash = DemoPCash(account=request.POST['account'],cash=request.POST['total3'],date=request.POST['date'],ledger_name='Supplier-ledger')
    democash.save()
    return redirect( '/')
def pcreditview(request):
    crd1 = PCredit.objects.all()
    context = {'crd': crd1}
    return render(request,'Sam/show credit puchase.html', context)
def editpcredit(request,id):
    crd1 = PCredit.objects.get(id=id)
    context = {'crd': crd1}
    return render(request,'Sam/edit credit purchase.html', context)
def updatepcredit(request,id):
    crd = PCredit.objects.get(id=id)
    crd.invoice_number = request.POST['invoice_number']
    crd.date = request.POST['date']
    crd.internal_ref_no = request.POST['internal_ref_no']
    crd.due_on = request.POST['due_on']
    crd.user_id = request.POST['user_id']
    crd.credit_limit_amt = request.POST['credit_limit_amt'],
    crd.supp_id = request.POST['supp_id']
    crd.supp_name = request.POST['supp_name']
    crd.item_id1 = request.POST['item_id1']
    crd.item_id2 = request.POST['item_id2']
    crd.item_details1 = request.POST['item_details1']
    crd.item_details2 = request.POST['item_details2']
    crd.price = request.POST['price']
    crd.price1_2 = request.POST['price1_2']
    crd.qty = request.POST['qty']
    crd.quantity2 = request.POST['quantity2']
    crd.total = request.POST['total']
    crd.amount2 = request.POST['amount2']
    crd.sales_ex1 = request.POST['sales_ex1']
    crd.sales_ex2 = request.POST['sales_ex2']
    crd.job1 = request.POST['job1']
    crd.job2 = request.POST['job2']
    crd.labour_charge = request.POST['labour_charge']
    crd.other_charge = request.POST['other_charge']
    crd.total1 = request.POST['total1']
    crd.total2 = request.POST['total2']
    crd.total3 = request.POST['total3']
    crd.total4 = request.POST['total4']
    crd.discount = request.POST['discount']
    crd.save()
    return render(request, 'Sam/purchase.html')
def deletepcredit(request, id):
    crd = PCredit.objects.get(id=id)
    crd.delete()
    return render(request, 'Sam/purchase.html')


def gopsreturnsale(request):
    return render(request, 'Sam/purchase return.html')
def psreturncreate(request):
    rtn2 = PRSales_Return(invoice_number=request.POST['invoice_number'],date=request.POST['date'],
                internal_ref_no=request.POST['internal_ref_no'],due_on=request.POST['due_on'],
                user_id=request.POST['user_id'],credit_limit_amt=request.POST['credit_limit_amt'],
                supp_id=request.POST['supp_id'],supp_name=request.POST['supp_name'],
                item_id1=request.POST['item_id1'],item_id2=request.POST['item_id2'],
                item_details1=request.POST['item_details1'],item_details2=request.POST['item_details2'],
                price=request.POST['price'],price1_2=request.POST['price1_2'],
                qty=request.POST['qty'],quantity2=request.POST['quantity2'],
                total=request.POST['total'], amount2=request.POST['amount2'],
                sales_ex1=request.POST['sales_ex1'], sales_ex2=request.POST['sales_ex2'],
                job1=request.POST['job1'], job2=request.POST['job2'],
                labour_charge=request.POST['labour_charge'], other_charge=request.POST['other_charge'],
                total1=request.POST['total1'], total2=request.POST['total2'],
                total3=request.POST['total3'], total4=request.POST['total4'],
                discount=request.POST['discount'],)
    rtn2.save()
    return redirect( '/')
def psreturnview(request):
    rtn1 = PRSales_Return.objects.all()
    context = {'rtn': rtn1}
    return render(request,'Sam/show purchase return.html', context)
def editpsreturn(request,id):
    rtn1 = PRSales_Return.objects.get(id=id)
    context = {'rtn': rtn1}
    return render(request,'Sam/edit purchase return.html', context)
def updatepsreturn(request,id):
    rtn = PRSales_Return.objects.get(id=id)
    rtn.invoice_number = request.POST['invoice_number']
    rtn.date = request.POST['date']
    rtn.internal_ref_no = request.POST['internal_ref_no']
    rtn.user_id = request.POST['user_id']
    rtn.due_on = request.POST['due_on']
    rtn.credit_limit_amt = request.POST['credit_limit_amt'],
    rtn.supp_id = request.POST['supp_id']
    rtn.supp_name = request.POST['supp_name']
    rtn.item_id1 = request.POST['item_id1']
    rtn.item_id2 = request.POST['item_id2']
    rtn.item_details1 = request.POST['item_details1']
    rtn.item_details2 = request.POST['item_details2']
    rtn.price = request.POST['price']
    rtn.price1_2 = request.POST['price1_2']
    rtn.qty = request.POST['qty']
    rtn.quantity2 = request.POST['quantity2']
    rtn.total = request.POST['total']
    rtn.amount2 = request.POST['amount2']
    rtn.sales_ex1 = request.POST['sales_ex1']
    rtn.sales_ex2 = request.POST['sales_ex2']
    rtn.job1 = request.POST['job1']
    rtn.job2 = request.POST['job2']
    rtn.labour_charge = request.POST['labour_charge']
    rtn.other_charge = request.POST['other_charge']
    rtn.total1 = request.POST['total1']
    rtn.total2 = request.POST['total2']
    rtn.total3 = request.POST['total3']
    rtn.total4 = request.POST['total4']
    rtn.discount = request.POST['discount']
    rtn.save()
    return render(request, 'Sam/purchase.html')
def deletepsreturn(request, id):
    rtn = PRSales_Return.objects.get(id=id)
    rtn.delete()
    return render(request, 'Sam/purchase.html')


def gopreceipt(request):
    return render(request, 'Sam/purchase receipt.html')
def preceiptcreate(request):
    rpt2 = PReceipt(receipt_number=request.POST['receipt_number'], date=request.POST['date'], internal_ref_no=request.POST['internal_ref_no'],
    due_on=request.POST['due_on'], credit_limit_amt=request.POST['credit_limit_amt'], user_id=request.POST['user_id'],
    supp_id=request.POST['supp_id'], supp_name = request.POST['supp_name'],invoice_no1 = request.POST['invoice_no1'],
    invoice_no2 = request.POST['invoice_no2'],invoice_no3 = request.POST['invoice_no3'],invoice_date1 = request.POST['invoice_date1'],
    invoice_date2 = request.POST['invoice_date2'],invoice_date3 = request.POST['invoice_date3'],duedate1 = request.POST['duedate1'],
    duedate2 = request.POST['duedate2'],duedate3 = request.POST['duedate3'],invoice_amt1 = request.POST['invoice_amt1'],
    invoice_amt2 = request.POST['invoice_amt2'],invoice_amt3 = request.POST['invoice_amt3'],received_amt1 = request.POST['received_amt1'],
    received_amt2 = request.POST['received_amt2'],received_amt3 = request.POST['received_amt3'],outstanding1 = request.POST['outstanding1'],
    outstanding2 = request.POST['outstanding2'],outstanding3 = request.POST['outstanding3'],discount1 = request.POST['discount1'],discount2 = request.POST['discount2'],
    discount3 = request.POST['discount3'],balance_amt1 = request.POST['balance_amt1'],balance_amt2 = request.POST['balance_amt2'],balance_amt3 = request.POST['balance_amt3'],
    tick_space1 = request.POST['tick_space1'],tick_space2 = request.POST['tick_space2'],tick_space3 = request.POST['tick_space3'],partial1 = request.POST['partial1'],
    partial2 = request.POST['partial2'],partial3 = request.POST['partial3'],total1 = request.POST['total1'],account = request.POST['account'],
    total3 = request.POST['total3'],total4 = request.POST['total4'],total5 = request.POST['total5'],total6 = request.POST['total6'],
    on_account = request.POST['on_account'],discount = request.POST['discount'],)
    rpt2.save()
    democash = DemoPCash(account=request.POST['account'],cash=request.POST['total5'],date=request.POST['date'],ledger_name='Cash Ledger')
    democash.save()
    return redirect('/')


def preceiptview(request):
    rpt1 = PReceipt.objects.all()
    context = {'rpt': rpt1}
    return render(request,'Sam/show purchase receipt.html', context)
def editpreceipt(request,id):
    rpt1 = PReceipt.objects.get(id=id)
    context = {'rpt': rpt1}
    return render(request,'Sam/edit purchase receipt.html', context)
def updatepreceipt(request,id):
    rpt = PReceipt.objects.get(id=id)
    rpt.receipt_number=request.POST['receipt_number']
    rpt.date = request.POST['date']
    rpt.internal_ref_no = request.POST['internal_ref_no']
    rpt.due_on = request.POST['due_on']
    rpt.credit_limit_amt = request.POST['credit_limit_amt']
    rpt.user_id = request.POST['user_id']
    rpt.supp_id = request.POST['supp_id']
    rpt.supp_name = request.POST['supp_name']
    rpt.invoice_no1 = request.POST['invoice_no1']
    rpt.invoice_no2 = request.POST['invoice_no2']
    rpt.invoice_no3 = request.POST['invoice_no3']
    rpt.invoice_date1 = request.POST['invoice_date1']
    rpt.invoice_date2 = request.POST['invoice_date2']
    rpt.invoice_date3 = request.POST['invoice_date3']
    rpt.duedate1 = request.POST['duedate1']
    rpt.invoice_amt2 = request.POST['invoice_amt2']
    rpt.invoice_amt3 = request.POST['invoice_amt3']
    rpt.received_amt1 = request.POST['received_amt1']
    rpt.received_amt2 = request.POST['received_amt2']
    rpt.received_amt3 = request.POST['received_amt3']
    rpt.outstanding1 = request.POST['outstanding1']
    rpt.outstanding2 = request.POST['outstanding2']
    rpt.outstanding3 = request.POST['outstanding3']
    rpt.discount1 = request.POST['discount1']
    rpt.discount2 = request.POST['discount2']
    rpt.discount3 = request.POST['discount3']
    rpt.balance_amt1 = request.POST['balance_amt1']
    rpt.balance_amt2 = request.POST['balance_amt2']
    rpt.balance_amt3 = request.POST['balance_amt3']
    rpt.tick_space1 = request.POST['tick_space1']
    rpt.tick_space2 = request.POST['tick_space2']
    rpt.tick_space3 = request.POST['tick_space3']
    rpt.partial1 = request.POST['partial1']
    rpt.partial2 = request.POST['partial2']
    rpt.partial3 = request.POST['partial3']
    rpt.total1 = request.POST['total1']
    rpt.total2 = request.POST['total2']
    rpt.total3 = request.POST['total3']
    rpt.total4 = request.POST['total4']
    rpt.total5 = request.POST['total5']
    rpt.total6 = request.POST['total6']
    rpt.on_account = request.POST['on_account']
    rpt.discount = request.POST['discount']

    rpt.save()
    return render(request, 'Sam/purchase.html')
def deletepreceipt(request, id):
    rpt = PReceipt.objects.get(id=id)
    rpt.delete()
    return render(request, 'Sam/purchase.html')


