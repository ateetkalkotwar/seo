from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "person/<slug:slug>/",
        views.person_detail,
        name="person_detail",
    ),

    path(
        "robots.txt",
        views.robots_txt,
        name="robots_txt",
    ),

    path(
        "upload/",
        views.upload_photo,
        name="upload_photo",
    ),

    path(
        "upload/success/",
        views.upload_success,
        name="upload_success",
    ),

    path(
        "photo/<slug:slug>/",
        views.photo_detail,
        name="photo_detail",
    ),

]