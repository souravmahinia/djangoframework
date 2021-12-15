"""flatchat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from flatapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home_pg,name="home"),
    path("about/",views.about_pg,name="about"),
    path("contact/",views.contct_pg,name="contact"),
    path("signup/",views.signup_pg,name="signup"),
    path("view_property/",views.view_property,name="view_property"),
    path("add_property/",views.add_property,name="add_property"),
    path("bnglor_pg/",views.bnglor_pg,name="bnglor_pg"),
    path("check_user/",views.check_user,name="check_user"),
    path('user_login/',views.user_login,name="user_login"),
    path('customer_dashboard/',views.customer_dashboard,name="customer_dashboard"),
    path('user_logout/',views.user_logout,name="user_logout"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path("change_password/",views.change_password,name="change_password"),
    path("addd_property/",views.add_property_view,name="add_property_view"),
    path("my_properties/",views.my_properties,name="my_properties"),
    path("single_property/",views.single_property,name="single_property"),
    path("update_property/",views.update_property,name="update_property"),
    path("delete_property/",views.delete_property,name="delete_property"),
    path('all_properties/',views.all_properties,name="all_properties"),
    path('sendemail',views.sendemail,name="sendemail"),
    path('forgotpass',views.forgotpass,name="forgotpass"),
    path('reset_password',views.reset_password,name="reset_password"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process_payment',views.process_payment,name="process_payment"),
    path('payment_done',views.payment_done,name="payment_done"),
    path('payment_cancelled',views.payment_cancelled,name="payment_cancelled"),
   
   

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
