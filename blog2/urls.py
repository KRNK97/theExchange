from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog_app.urls')),
    # accepting all auth urls such as login, logout, register
    # the urls will by default go to registration/register.html and registration/login.html as templates
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('blog_members.urls')),
    path('djrichtextfield/', include('djrichtextfield.urls')),
]

handler404 = 'blog_app.views.handler404'
