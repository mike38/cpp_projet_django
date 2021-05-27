"""projet_cpp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from exo import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exo.urls')),
    path('search_chap', views.search_chap, name='search-chap'),
    path('register/', views.register, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
	path('interdit/', views.acces_interdit, name='interdit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#urlpatterns = [
#    url(r'^/search/?$', MySearchView.as_view(), name='search_view'),
#]
