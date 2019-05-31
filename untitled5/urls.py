"""untitled5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from board import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_board/<name>', views.add_board),
    path('', views.home),
    path('reg/', views.registration),
    path('log/', views.log_in, ),
    path('logout/', views.log_out),
    path('delete_board/<board>/', views.del_board),
    path('delete_thread/<board>/<thread>/', views.del_thread),
    path('delete_answer/<board>/<thread>/<answer>/', views.del_answer),
    path('edit_answer/<board>/<topic>/<answer>/', views.edit_answer),
    path('edit_thread/<board>/<thread>/', views.edit_thread),
    path('<string>/', views.board),
    path('<string>/create_thread/', views.create_thread),
    path('<string>/<integer>/', views.thread),
    path('<board>/<integer>/reply/', views.reply),
    path('add_section', views.add_section),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

"""
if settings.DEBUG:
    urlpatterns += patterns(‘’,
        (r’^debuginfo/$’, views.debug),
        )
"""

#  if settings.DEBUG:
#     urlpatterns += ('debuginfo/', views.debug)
