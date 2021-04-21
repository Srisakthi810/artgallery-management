from django.urls import path
from artgallery import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home1/',views.home1, name='home1'),
    path('register/',views.registerCustomer,name='registercustomer'),
    path('login/',views.customerLogin,name='customerLogin'),
    path('customised/', views.customisedproduct, name='customisedproduct'),
    path('logout/', views.customerLogout, name='logout'),
    path('customerdetail/', views.customerdetail, name='customerdetail'),
    path('login_admin/', views.adminLogin, name='adminLogin'),
    path('orderlistcustomer/', views.orderlistcustomer, name='orderlistcustomer'),
    path('customeractions/',views.customeractions,name='customeractions'),
    path('adminactions/',views.adminactions,name='adminactions'),
    path('adminsales/',views.adminsales,name='adminsales'),
    path('adminstock/',views.adminstock,name='adminstock'),
    path('sendmail/', views.sendmail, name='sendmail'),
    path('about/',views.about,name='about'),
    path('orderinsert/',views.orderinsert,name='orderinsert'),
    path('orderlistadmin/',views.orderlistadmin,name='orderlistadmin'),
    path('stockinsert/',views.stockinsert,name='stockinsert'),
    path('stockview/',views.stockview,name='stockview'),
    path('firstpage/', views.firstpage, name='firstpage'),
    path('base/', views.base, name='base'),
    path('updateorder/(?P<order_id>[0-9]+)',views.updateorder,name = 'updateorder'),
    path('purchaseinsert/',views.purchaseinsert,name='purchaseinsert'),
    path('purchaseview/',views.purchaseview,name='purchaseview'),
    path('updatestock/(?P<stock_id>\d+)/$',views.updatestock,name = 'updatestock'),
    path('viewreports/',views.viewreports,name='viewreports'),
    path('deleteorder/(?P<order_id>[0-9]+)',views.deleteorder,name = 'deleteorder'),
    path('deletestock/(?P<purchase_id>[0-9]+)',views.deletestock,name = 'deletestock'),
    path('deletepurchase/(?P<stock_id>\d+)/$',views.deletepurchase,name = 'deletepurchase'),



]

