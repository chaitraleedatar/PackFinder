#
# Created on Sun Nov 04 2024
#
# The MIT License (MIT)
# Copyright (c) 2024 Chaitralee Datar, Ananya Patankar, Yash Shah
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# accounts/urls.py
from django.urls import path
from .views import SignUpView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from base.views import ActivateAccount
from django.views.generic import TemplateView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("findpeople/", views.findpeople, name="findpeople"),
    path("myroom/", views.myroom, name="myroom"),
    path("logout/", views.user_logout, name="user_logout"),
    path('chats/', views.chat_list, name='chat_list'),
    path('chat/<int:room_id>/', views.chat_room, name='chat_room'),
    path('chat/create/<int:user_id>/', views.create_chat_room, name='create_chat_room'),
    path('chat/<int:room_id>/clear/', views.clear_chat, name='clear_chat'),
    path(
        "about",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "activate/<uidb64>/<token>/",
        ActivateAccount.as_view(),
        name="activate",
    ),
    path("", views.home, name="home"),
    path('add-room/', views.add_room, name='add_room'),
    path('toggle-interest/<int:room_id>/', views.toggle_room_interest, name='toggle_room_interest'),
]

# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
