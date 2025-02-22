from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("get_naani", views.get_naani, name="get_naani"),
    path("cry_detection", views.cry_detection, name="cry_detection"),
    path("parenting_tips", views.parenting_tips, name="parenting_tips"),
    path("discussion_forum", views.discussion_forum, name="discussion_forum"),
    path("telehealth", views.telehealth, name="telehealth"),
    path("memory_book", views.memory_book, name="memory_book"),
    path("growth_track", views.growth_track, name="growth_track"),
    path("about", views.about, name="about"),
    path("milestone_tracker", views.milestone_tracker, name="milestone_tracker"),
    path("moms_corner", views.moms_corner, name="moms_corner"),
    path("contact", views.contact, name="contact"),
    path("profile", views.profile, name="profile"),
     path("health_tips", views.health_tips, name="health_tips"),
    path('book_naani', views.book_naani, name='book_naani'),
    path('discussion_forum', views.discussion_forum, name='discussion_forum'),
    path('thread/<int:pk>/', views.discussion_detail, name='discussion_detail'),
    path('create/', views.discussion_create, name='discussion_create'),
    path('prediction', views.predict_cry, name='prediction'),
    path('play_audio', views.play_audio, name='play_audio'),
     path('emergency_care', views.emergency_care, name='emergency_care'),


    

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)