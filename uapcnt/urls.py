"""
URL configuration for uapcnt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import settings
from django.conf.urls.static import static

from authenticate import views as acc_views

urlpatterns = [
        path('admin/', admin.site.urls),
        path('', acc_views.login, name="login"),
        path('signup/', acc_views.signup, name="signup"),
        path('logout/', acc_views.logout_view, name="logout"),
        path('home/',acc_views.home,name="home"),
        path('profile/',acc_views.profile,name="profile"),
        path('edit_profile/', acc_views.edit_profile, name='edit_profile'),
        path('resources/',acc_views.resources,name="resources"),
        path('forum/',acc_views.forum,name="forum"),
        path('createpost/', acc_views.createpost, name="createpost"),
        path('upload_post/', acc_views.upload_post, name="upload_post"),
        path('update_post/<str:id>', acc_views.update_post, name="update_post"),
        path('delete_post/<str:id>', acc_views.delete_post, name="delete_post"),
        path('upload_query/', acc_views.upload_query, name="upload_query"),
        path('update_query/<str:id>', acc_views.update_query, name="update_query"),
        path('delete_query/<str:id>', acc_views.delete_query, name="delete_query"),
        path('upload_resource/', acc_views.upload_resource, name="upload_resource"),
        path('update_resource/<str:id>',acc_views.update_resource,name="update_resource"),
        path('delete_resource/<str:id>',acc_views.delete_resource,name="delete_resource"),
        path('clubdetails/', acc_views.clubdetails, name="clubdetails"),
        path('alumni/', acc_views.alumni_section, name='alumni_section'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
