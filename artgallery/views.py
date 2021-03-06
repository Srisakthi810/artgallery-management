from django.shortcuts import render,redirect
from artgallery.forms import *
from django.db.models import Sum
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from artgallery.models import *
from django.core.mail import send_mail
from art.settings import EMAIL_HOST_USER



# Create your views here.
def home(request):
    return render(request, 'artgallery/firstpage.html', {})

# def register(request):
#     return render(request,'artgallery/register.html')
def home1(request):
    return render(request, 'artgallery/home1.html')
def firstpage(request):
    return render(request, 'artgallery/firstpage.html')

def base(request):
    return render(request, 'artgallery/base.html')

@login_required
def customerLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def registerCustomer(request):
    registered=False
    if request.method=='POST':
        var_customerForm=customerForm(request.POST)
        if var_customerForm.is_valid():
            customerprimary=var_customerForm.save()
            customerprimary.set_password(customerprimary.password)
            customerprimary.save()
            registered=True
            # return redirect('userLogin')
    else:
        var_customerForm=customerForm()
    return render(request,'artgallery/customerreg.html',{'var_customerForm':var_customerForm,'registered':registered})

def customerLogin(request):
    invalidlogin=False
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('customerdetail'))
            else:
                return HttpResponse('Account not active')
        else:
            invalidlogin=True
            return redirect('registercustomer')
    else:
        return render(request,'artgallery/customerlogin.html',{'invalidlogin':invalidlogin})




def customisedproduct(request):
        submitted = False
        if request.method == "POST":
            form = custproduct(request.POST)


            print(request.user)

            if form.is_valid():

                cuspro = form.save(commit=False)
                use = Customer.objects.get(cus_name=request.user)
                cuspro.customer = use
                print(use)
                cuspro.save()
                submitted = True

        else:
            form = custproduct()
        return render(request, 'artgallery/customisedproduct.html', {'form': form, 'submitted': submitted})


def customerdetail(request):
    if request.method == "POST":
        form = customerdetailform(request.POST)
        if form.is_valid():
            cus = form.save(commit=False)
            cus.save()
            return redirect('customeractions')
    else:
        form = customerdetailform()

    return render(request, 'artgallery/customerdetail.html', {'form': form})

def adminLogin(request):
    invalidlogin=False
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('adminactions'))
            else:
                return HttpResponse('Account not active')
        else:
            invalidlogin=True
            return redirect('home')
    else:
        return render(request,'artgallery/adminlogin.html',{'invalidlogin':invalidlogin})

def orderlistcustomer(request):
    order_list=Custpro.objects.all()
    context={'cust':order_list}
    return render(request,'artgallery/orderlistcustomer.html',context)

def customeractions(request):
    return render(request, 'artgallery/customeractions.html')

def adminactions(request):
    return render(request, 'artgallery/adminactions.html')


def adminstock(request):
    return render(request, 'artgallery/adminstock.html')

def adminsales(request):
    ord = Orders.objects.all()
    lis = []
    for o in ord:
        if o.status=='accepted':
            lis.append(o)

    context = {'admods': lis}
    return render(request, 'artgallery/adminsales.html', context)


def sendmail(request):

    pas = Orders.objects.get(order_id = request.POST["orderid"])
    use = pas.customer
    strg = ''
    strg += pas.p_name[:2]
    strg += str(pas.psize_w)
    strg += str(pas.psize_h)


    stk = Purchase.objects.get(stock_id = strg)
    stk.s_quantity = int(stk.s_quantity) - int(pas.p_quantity)
    stk.save()

    if request.method == 'POST':
        if 'accept' in request.POST["decision"]:
            pas.status = 'accepted'
            pas.save()
        mai = use.mail_id
        subject = 'Order approval'
        message = 'Hello, '+use.cus_name+'\nYour order has been approved and has been dispatched!!Happy shopping\nThank you \nregards\n-'+'.'
        recepient = mai
        send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)

        return render(request, 'artgallery/mailsent.html', {'recepient': recepient})
    return render(request, 'artgallery/orderlistadmin.html')


def about(request):
    return render(request, 'artgallery/about.html')

def updateorder(request,order_id):
    # form = ordersadmin()
    if request.method== 'GET':
        order = Orders.objects.get(order_id = order_id)
        form = ordersadmin(instance=order)
        if form.is_valid():
            form.save()
        return render(request, 'artgallery/orderinsert.html',{'form':form})
    else:
        order = Orders.objects.get(order_id=order_id)
        form = ordersadmin(request.POST,instance=order)
        if form.is_valid():
            form.save()
        return redirect('orderlistadmin')



def orderinsert(request):
    submitted = False
    if request.method == "POST":
        form = ordersadmin(request.POST)
        if form.is_valid():
            admod = form.save(commit=False)
            admod.save()
            submitted = True
            return redirect('adminactions')
    else:
        form = ordersadmin()

    return render(request, 'artgallery/orderinsert.html', {'form': form, 'submitted': submitted})


def orderlistadmin(request):
    order_list_admin=Orders.objects.all()
    context={'admod':order_list_admin}
    return render(request,'artgallery/orderlistadmin.html',context)

def stockinsert(request):
    submitted = False
    if request.method == "POST":
        form = stockadmin(request.POST)
        if form.is_valid():
            stod = form.save(commit=False)
            stod.save()
            submitted = True
            return redirect('adminactions')
    else:
        form = stockadmin()

    return render(request, 'artgallery/stockinsert.html', {'form': form, 'submitted': submitted})

def stockview(request):
    stock_view=Stock.objects.all()
    context={'stod':stock_view}
    return render(request,'artgallery/stockview.html',context)

def purchaseinsert(request):
    submitted = False
    if request.method == "POST":
        form = purchaseadmin(request.POST)
        if form.is_valid():
            ptod = form.save(commit=False)
            ptod.save()
            submitted = True
            return redirect('adminactions')
    else:
        form = purchaseadmin()

    return render(request, 'artgallery/purchaseinsert.html', {'form': form, 'submitted': submitted})

def purchaseview(request):
    purchase_view=Purchase.objects.all()
    context={'ptod':purchase_view}
    return render(request,'artgallery/purchaseview.html',context)

def updatestock(request,stock_id):
    # form = ordersadmin()
    if request.method== 'GET':
        stock = Purchase.objects.get(stock_id = stock_id)
        form = purchaseadmin(instance=stock)
        if form.is_valid():
            form.save()
        return render(request, 'artgallery/purchaseinsert.html',{'form':form})
    else:
        stock = Purchase.objects.get(stock_id = stock_id)
        form = purchaseadmin(request.POST,instance=stock)
        if form.is_valid():
            form.save()
        return redirect('purchaseview')


def viewreports(request):
        disp = Stock.objects.all()
        order = Orders.objects.filter(status='accepted')
        data = 0
        data1 = 0
        profit = 0
        loss = 0
        for o in order:
            temp_total = o.p_totalprice
            data1 += temp_total
        for d in disp:
            temp_total = d.s_totalprice
            data += temp_total
        if data1 > data:
            profit = data1 - data
        else:
            loss = data - data1

        return render(request, 'artgallery/viewreports.html',{'total': data, 'total1': data1, 'profit': profit, 'loss': loss})

def deleteorder(request,order_id):
    # form = ordersadmin()

    order = Orders.objects.get(order_id = order_id)
    order.delete()
    # return HttpResponse("Deleted!")

    return redirect('orderlistadmin')

def deletestock(request,purchase_id):
    # form = ordersadmin()

    order1 = Stock.objects.get(purchase_id = purchase_id)
    order1.delete()
    # return HttpResponse("Deleted!")

    return redirect('stockview')

def deletepurchase(request,stock_id):
    # form = ordersadmin()

    order2 = Purchase.objects.get(stock_id = stock_id)
    order2.delete()
    # return HttpResponse("Deleted!")

    return redirect('purchaseview')