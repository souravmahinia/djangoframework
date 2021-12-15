from django.contrib import admin
from flatapp.models import Contact_Us,Category,register_table,add_prperty,Single_Property_msg

admin.site.site_header = "Flatchat Project Database"

class Contact_UsAdmin(admin.ModelAdmin):
    list_display = ["id","name","contact_number","email","subject","message","added_on"]
    search_fields = ["name"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id","cat_name","cover_pic","description","added_on"]


# Register your models here.
admin.site.register(Contact_Us,Contact_UsAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(register_table)
admin.site.register(add_prperty)
admin.site.register(Single_Property_msg)



