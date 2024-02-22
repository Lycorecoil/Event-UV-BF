from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('',views.home,name='home'),
	path('login/',views.loginPage,name='login'),
	path('logout/',views.logoutUser,name='logout'),
	path('event/<str:pk>/',views.event,name='event'),
	path('register/',views.registerPage,name='register'),
	
	path('create-event/',views.createEvent,name='create-event'),
    path('profile/<str:pk>/',views.userProfile,name='user-profile'),
	path('update-event/<str:pk>/',views.updateEvent,name='update-event'),
	path('delete-event/<str:pk>/',views.deleteEvent,name='delete-event'),
	path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),
    path('update-user/',views.updateUser,name='update-user'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)