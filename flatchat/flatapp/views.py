from django.shortcuts import render,get_object_or_404,reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from flatapp.models import Contact_Us,Category,register_table,add_prperty,Single_Property_msg
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from flatapp.forms import add_property_form
from django.db.models import Q
from datetime import datetime
from django.core.mail import EmailMessage
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

def home_pg(request):
    if "user_id" in request.COOKIES:
        uid = request.COOKIES["user_id"]
        usr = get_object_or_404(User,id=uid)
        login(request,usr)
        if usr.is_superuser:
            return HttpResponseRedirect("/admin")
        if usr.is_active:
            return HttpResponseRedirect("/customer_dashboard")
    recent = Contact_Us.objects.all().order_by("-id")[:5]
    cats = Category.objects.all().order_by("cat_name")
    all_properties = add_prperty.objects.all().order_by("property_name")[:6]

    return render(request,"home.html",{"messages":recent,"category":cats,"properties":all_properties,})

def about_pg(request):
    cats = Category.objects.all().order_by("cat_name")
    return render(request,"about.html",{"category":cats})

def view_property(request):
    cats = Category.objects.all().order_by("cat_name")
    return render(request,"pg_hostels.html",{"category":cats})

def add_property(request):
    cats = Category.objects.all().order_by("cat_name")
    return render(request,"add_property.html",{"category":cats})

def bnglor_pg(request):
    cats = Category.objects.all().order_by("cat_name")
    return render(request,"bnglor_pg.html",{"category":cats})

def contct_pg(request):
    cats = Category.objects.all().order_by("cat_name")
    if request.method=="POST":
        nm = request.POST["name"]
        con = request.POST["contact"]
        eml = request.POST["email"]
        sub = request.POST["subject"]
        msz = request.POST["message"]

        data = Contact_Us(name=nm,contact_number=con,email=eml,subject=sub,message=msz)
        data.save()
        res = "Dear {} Thanks For Your Feedback.!!!".format(nm)
        return render(request,"contact.html",{"status":res,"category":cats})
    return render(request,"contact.html",{"category":cats})



def signup_pg(request):
    cats = Category.objects.all().order_by("cat_name")
    if request.method=="POST":
        fname = request.POST["first"]
        lname = request.POST["last"]
        un = request.POST["uname"]
        pwd = request.POST["password"]
        cpwd = request.POST["cpassword"]
        em = request.POST["email"]
        con = request.POST["contact"]
        tp = request.POST["utype"]

        usr = User.objects.create_user(un,em,pwd)
        usr.first_name = fname
        usr.last_name = lname
        #usr.cnfrm_pas = cpwd
        usr.save()
        if tp=="sell":
            usr.is_staff = True
        usr.save()

        reg = register_table(user=usr,contact_number=con)
        reg.save()
        return render(request,"signup.html",{"status":" Mr/Miss. {} Your Account Created Successfully".format(fname)})
        
    return render(request,"signup.html",{"category":cats})


def check_user(request):
    if request.method=="GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check)==1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")


def user_login(request):
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]

        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            else:
                res = HttpResponseRedirect("/customer_dashboard")
                if "rememberme" in request.POST:
                    res.set_cookie("user_id",user.id)
                    res.set_cookie("date_login",datetime.now)
                return res

                             
        else:
            return render(request,"home.html",{"status":"Invalid Username or Password"})
    return HttpResponse("Called")


def process_payment(request):
    context={}
    if request.user.is_authenticated:
         if request.method=="POST":
             pid = request.POST["pid"]
             #amt = request.POST["amt"]
             #pnm = request.POST["pnm"]
             user = register_table.objects.get(user__id=request.user.id)
             property = add_prperty.objects.get(id=pid)
             amt = property.booking_amount
             pnm = property.property_name
             

             paypal_dict = {
             'business': settings.PAYPAL_RECEIVER_EMAIL,
             'amount': str(amt),
             'item_name': pnm,
             'invoice': pid,
             'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                                reverse('paypal-ipn')),
             'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                                reverse('payment_done'),pid),
             'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                                reverse('payment_cancelled')),

              }



             request.session["property_id"] = pid
    
             form = PayPalPaymentsForm(initial=paypal_dict)
             return render(request, 'process_payment.html', {'form': form,'property':property})
 
       
    else:
        context["status"] = "Please Login First To Book Property"
    return render(request,"allproperties.html",context)

@login_required
def customer_dashboard(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,"customer_dashboard.html",context)
    

@login_required
def user_logout(request):
    logout(request)
    res =  HttpResponseRedirect("/")
    res.delete_cookie("user_id")
    res.delete_cookie("date_login")
    return res

def edit_profile(request):
    context = {}
    check = register_table.objects.filter(user_id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    
    if request.method=="POST":
        fn = request.POST["fname"]
        ln = request.POST["lname"]
        em = request.POST["email"]
        con = request.POST["contact"]
        faddrs = request.POST["faddrs"]
        ct = request.POST["city"]
        gen = request.POST["gender"]
        abt = request.POST["about"]

        if request.user.is_staff:
            twtr = request.POST["twitr"]
            fb = request.POST["fb"]
            insta = request.POST["insta"]
            qualifictn = request.POST["qualfctn"]

            data.fb = fb
            data.twitr = twtr
            data.insta = insta
            data.qualifictn = qualifictn
            data.save()
        else:
            occ = request.POST["occ"]
            if "proof" in request.FILES:
                prf = request.FILES["proof"]
                data.id_proof = prf
            data.occupation = occ
            data.save()
            
                   
        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        data.contact_number = con
        data.city = ct
        data.gender = gen
        data.about = abt
        data.full_address = faddrs
        data.save()

        if "image" in request.FILES:
            img = request.FILES["image"]
            data.profile_pic = img
            data.save()

        context["status"]="Changes Saved Successfully.!!!"

    return render(request,"edit_profile.html",context)


def change_password(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]

        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully.!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"] = "Incorrect Current Password.!!!"
            context["col"] = "alert-danger"

    return render(request,"change_password.html",context)



def add_property_view(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    form = add_property_form
    if request.method=="POST":
        form = add_property_form(request.POST,request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            login_user = User.objects.get(username=request.user.username)
            data.seller = login_user
            data.save()
            context["msz"] = '"{}" Property Added Successfully.!!!'.format(data.property_name)
            context["col"] = "alert-success"
            
    context["form"] = form
    return render(request,"addproperty.html",context)



def my_properties(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    all = add_prperty.objects.filter(seller__id=request.user.id).order_by("-id")
    context["properties"] = all
    return render(request,"myproperties.html",context)



def single_property(request):
    context = {}
    id = request.GET["pid"]
    obj = add_prperty.objects.get(id=id)
    context["property"] = obj

    
    if request.method=="POST":
        nm = request.POST["name"]
        eml = request.POST["email"]
        con = request.POST["contact"]
        msz = request.POST["message"]
        data = Single_Property_msg(name=nm,email=eml,contact_number=con,message=msz)
        data.save()  
        return render(request,"single_property.html",context)
    
    cats = Category.objects.all().order_by("cat_name")
    return render(request,"single_property.html",context)



def update_property(request):
    context = {}
    cats = Category.objects.all().order_by("cat_name")
    context["category"] = cats

    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data

    pid = request.GET["pid"]
    property = add_prperty.objects.get(id=pid)
    context["property"] = property

    if request.method=="POST":
        pn = request.POST["pname"]
        pa = request.POST["addr"]
        ps = request.POST["pstts"]
        pp = request.POST["pp"]
        ba = request.POST["bp"]
        pbth = request.POST["pbath"]
        pbd = request.POST["pbed"]
        par = request.POST["parea"]
        plndry = request.POST["plr"]
        pac = request.POST["pac"]
        pgym = request.POST["pgym"]
        ptv = request.POST["ptv"]
        pwifi = request.POST["pwifi"] 
        pprkg = request.POST["pprkg"]
        pswmgpl = request.POST["pswmgpl"]
        des = request.POST["des"]
        ct_id = request.POST["pcat"]

        cat_obj = Category.objects.get(id=ct_id)

        property.property_name = pn
        property.address = pa
        property.property_status = ps
        property.property_price = pp
        property.booking_amount = ba
        property.no_of_bathrooms = pbth
        property.no_of_bedrooms = pbd
        property.area = par
        property.is_Laundry_room = plndry
        property.is_Air_Conditioning = pac
        property.is_Gym = pgym
        property.is_TV_Cable = ptv
        property.is_Wifi = pwifi
        property.is_Parking = pprkg
        property.is_Swimming_Pool = pswmgpl
        property.description = des
        property.property_type = cat_obj

        if "pimg1" in request.FILES:
            img = request.FILES["pimg1"]
            property.property_image1 = img

        if "pimg2" in request.FILES:
            img = request.FILES["pimg2"]
            property.property_image2 = img

        if "pimg3" in request.FILES:
            img = request.FILES["pimg3"]
            property.property_image3 = img

        if "pimg4" in request.FILES:
            img = request.FILES["pimg4"]
            property.property_image4 = img

        
        property.save()
        context["status"] = "Changes Saved Successfully.!!!"
        context["id"] = pid
    return render(request,"update_property.html",context)


def delete_property(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
        
    if "pid" in request.GET:
        pid = request.GET["pid"]
        prp = get_object_or_404(add_prperty, id=pid)
        context["property"] = prp

        if "action" in request.GET:
            prp.delete()
            context["status"]= str(prp.property_name)+" Removed Successfully.!!!"
    return render(request,"deleteproperty.html",context)



def all_properties(request):
    context = {}
    cats = Category.objects.all().order_by("cat_name")
    context["category"] = cats
    all_properties = add_prperty.objects.all().order_by("property_name")
    context["properties"] = all_properties

    if "qry" in request.GET:
        q = request.GET["qry"]
        #p = request.GET["loctn"]
        #prp = add_prperty.objects.filter(Q(property_type__cat_name__contains=q))
        #prp = add_prperty.objects.filter(Q(property_type__cat_name__contains=q)|Q(property_name__contains=q))
        prp = add_prperty.objects.filter(Q(address__icontains=q))
        context["properties"] = prp
        context["abcd"] = "search"


    if "cat" in request.GET:
        cid = request.GET["cat"]
        prp = add_prperty.objects.filter(property_type__id=cid)
        context["properties"] = prp   
        context["abcd"]="search"

    return render(request,"allproperties.html",context)



def sendemail(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data

    if request.method=="POST":
        rec = request.POST["to"].split(",")
        sub = request.POST["sub"]
        msz = request.POST["msz"]
        try:
            em = EmailMessage("sub","msz",to=rec)
            em.send()
            context["message"] = "Email Sent Successfully.!!!"
            context["cls"] = "alert-success text-center font-weight-bold"
        except:
            context["message"] = "Could Not Send, Please Check your Internet Connection/Email ID"
            context["cls"] = "alert-danger text-center font-weight-bold"

    return render(request,"sendemail.html",context)



def forgotpass(request):
    context = {}
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]

        user = get_object_or_404(User,username=un)
        user.set_password(pwd)
        user.save()

        login(request,user)
        if user.is_superuser:
            return HttpResponseRedirect("/admin")
        else:
            return HttpResponseRedirect("/customer_dashboard")

        #context["status"] = "Password Changed Successfully.!!!"
    return render(request,"forgot_pass.html",context)



import random
def reset_password(request):
    un = request.GET["username"]
    try:
        user = get_object_or_404(User,username=un)
        otp = random.randint(1000,9999)
        msz = "Dear {} \n{} is your One Time Password (OTP) \n Do Not share it with others \n Thanks & Regards \n Flatchat".format(user.username,otp)
        try:
            email = EmailMessage("Account Verification",msz,to=[user.email])
            email.send()
            return JsonResponse({"status":"sent","email":user.email,"rotp":otp})
        except:
            return JsonResponse({"status":"error","email":user.email})
    except:
        return JsonResponse({"status":"failed"})




def payment_done(request):
    if "property_id" in request.session:
        pid = request.session["property_id"]
        prop = get_object_or_404(add_prperty,id=pid)
        prop.status = "Confirmed"
        prop.save()
    return render(request,"payment_success.html")

def payment_cancelled(request):
     return render(request,"payment_failed.html")










