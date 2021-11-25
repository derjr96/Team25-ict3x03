"""djangotaurus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<int:user_id>', views.portfolio, name='portfolio-staff'),
    path('history/', views.history, name='history'),
    path('history/<int:user_id>', views.history, name='history-staff'),
    path('favourites/', views.favourites, name='favourites'),
    path('profile/', views.profile, name='profile'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('users/', views.users, name='users'),
    path('staffUserProfile/<int:user_id>', views.staffUserProfile, name='staffUserProfile'),
    path('logout/', views.logout, name='logout'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('verifyEmail/', views.verifyEmail, name='verifyEmail'),
    path('verifyCheck/<str:access_token>', views.verifyCheck, name='verifyCheck'),
    path('stockDetails/<int:stock_id>', views.stockDetails, name='stockDetails'),
    path('buyStock/', views.buyStock, name='buyStock'),
    path('sellStock/', views.sellStock, name='sellStock'),
    path('resetPassword/<str:access_token>', views.resetPassword, name='resetPassword'),
    path('otp/<str:next>', views.otp, name='otp'),
    path('error', views.error, name='error'),
    path('error<str:error_code>', views.error, name='error'),
    path('', include('pwa.urls'))
    
]
urlpatterns+= staticfiles_urlpatterns()
