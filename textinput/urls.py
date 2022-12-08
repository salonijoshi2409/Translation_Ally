from django.urls import path
from . import views
# from django.conf.urls import handler404, handler500
# from django.contrib import admin
# from django.urls import path, include
urlpatterns = [
    path('',views.home),
    #  path('admin/', admin.site.urls),
    # path('', include('demo.urls'))
    path('audio/', views.audiohome),
    path('downloadfile/',views.downloadfile, name='downloadfile')
     
]
