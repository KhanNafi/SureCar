from django.contrib import admin

from .models import Car, Wants, Recommendations, RecommendationFeedback, Page

# @admin.register(Buyer)
# class BuyerAdmin(admin.ModelAdmin):
#     list_display = ['id','first_name','last_name','email','password','phoneno','slug']
#     prepopulated_fields = {'slug': ('id',)}

# @admin.register(Seller)
# class SellerAdmin(admin.ModelAdmin):
#     list_display = ['id','first_name','last_name','seller_type','company_name','email','password','phoneno','slug']
#     prepopulated_fields = {'slug': ('id',)}

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['car_id','seller','name','year','price','km_driven','mileage','engine','transmission','fuel_type','seller_type','owner','seats','running_cost','image','slug']
    prepopulated_fields = {'slug': ('car_id',)}

@admin.register(Wants)
class WantsAdmin(admin.ModelAdmin):
    list_display = ['buyer','wanted_car_id','recommended_car_id','year','price','km_driven','mileage','engine','transmission','fuel_type','seller_type','owner','seats']
    # prepopulated_fields = {'slug': ('buyer',)}

@admin.register(Recommendations)
class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ['buyer','car_id','seller','name','year','price','km_driven','mileage','engine','transmission','fuel_type','seller_type','owner','seats','running_cost','image','score']

@admin.register(RecommendationFeedback)
class RecommendationFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id','year','price','km_driven','mileage','engine']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name','page_link']