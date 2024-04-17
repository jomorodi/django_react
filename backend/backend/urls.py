"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base.api.urls')),
    path ('shop/', include ('base.urls')),
    path ("" , views.homePage , name = "homePage" ),
    path ('testUserCreation/' , views.generate_test_users , name="generate_test_users")
]

urlpatterns += [
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path('accounts/my-items/', views.user_items, name='my_items'),
    
    path('accounts/change-password/', views.change_password, name='change_password'),
    path('accounts/', include('django.contrib.auth.urls')),
]



# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)