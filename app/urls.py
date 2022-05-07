from django.urls import path
from app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',views.home),
    path('home', views.home),
    path('signup', views.signup),
    path('signin', views.signin),
    path('signout', views.signout),
    path('browse', views.browse, name="browse"),
    path('car/<str:id>', views.car),
    path('carcontact/<str:id>', views.carcontact),
    path('smartrecommender', views.smartrecommender),
    path('recommendations', views.recommendations),
    path('singlerecommendation/<str:id>', views.singlerecommendation),
    path('singlerecommendationcontact/<str:id>', views.singlerecommendationcontact),
    path('sell', views.sell),
    path('about', views.about),
    path('analytics', views.analytics)
]

urlpatterns += staticfiles_urlpatterns()