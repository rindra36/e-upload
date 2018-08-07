"""eboutique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, re_path
from django.contrib.auth import views as authViews
from backoffice import views as backofficeView, forms as backofficeForms

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^backoffice/', include('backoffice.urls')),
    re_path(
        r'^login/$',
        authViews.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=backofficeForms.LogForm,
            redirect_authenticated_user=True
        ),
        name='login'
    ),
    re_path(
        r'^logout/$',
        authViews.LogoutView.as_view(next_page='/login'),
        name='logout'
    ),
    re_path(r'^signup/$', backofficeView.signup, name='signup')
]
