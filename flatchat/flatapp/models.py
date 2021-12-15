from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact_Us(models.Model):
    name = models.CharField(max_length=250)
    contact_number = models.IntegerField(unique=True)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Us"


class Single_Property_msg(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=200)
    contact_number = models.IntegerField(unique=True)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Send Message To Owner"



class Category(models.Model):
    cat_name = models.CharField(max_length=250)
    cover_pic = models.FileField(upload_to="categories/%Y/%m/%d")
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name


class add_prperty(models.Model):
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    property_name = models.CharField(max_length=250)
    property_price = models.FloatField()
    booking_amount = models.FloatField()
    address = models.CharField(max_length=250,null=True,blank=True)
    property_image1 = models.ImageField(upload_to="property/%Y/%m/%d")
    property_image2 = models.ImageField(upload_to="property/%Y/%m/%d")
    property_image3 = models.ImageField(upload_to="property/%Y/%m/%d")
    property_image4 = models.ImageField(upload_to="property/%Y/%m/%d")
    property_type = models.ForeignKey(Category,on_delete=models.CASCADE)
    property_status = models.CharField(max_length=250)
    area = models.FloatField()
    no_of_bedrooms = models.IntegerField()
    no_of_bathrooms = models.IntegerField()
    is_Air_Conditioning = models.BooleanField()
    is_Gym = models.BooleanField()
    is_Laundry_room = models.BooleanField()
    is_TV_Cable = models.BooleanField()
    is_Wifi = models.BooleanField()
    is_Parking = models.BooleanField()
    is_Swimming_Pool = models.BooleanField()
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property_name


class register_table(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact_number = models.IntegerField()

    fb = models.URLField(max_length=250,null=True,blank=True)
    twitr = models.URLField(max_length=250,null=True,blank=True)
    insta = models.URLField(max_length=250,null=True,blank=True)
    qualifictn = models.CharField(max_length=250,null=True,blank=True)
    full_address = models.CharField(max_length=250,null=True,blank=True)
    id_proof = models.FileField(upload_to="proof/%Y/%m/%d",null=True,blank=True)
    profile_pic = models.ImageField(upload_to="profiles/%Y/%m/%d",null=True,blank=True)
    age = models.CharField(max_length=250,null=True,blank=True)
    city = models.CharField(max_length=250,null=True,blank=True)
    gender = models.CharField(max_length=250,blank=True,default="Male")
    occupation = models.CharField(max_length=250,null=True,blank=True)
    about = models.TextField(blank=True,null=True)
    added_on = models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.username




