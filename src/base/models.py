#
# Created on Sun Oct 09 2022
#
# The MIT License (MIT)
# Copyright (c) 2022 Rohit Geddam, Arun Kumar, Teja Varma, Kiron Jayesh, Shandler Mason
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

from email.policy import default
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from django_countries.fields import CountryField


from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from .utils import check_ncsu_email


class CustomUser(AbstractUser):
    """Custom User Model"""

    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        email = self.email

        if not check_ncsu_email(email):
            raise ValueError("Please use NCSU Email Id!")
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Model for User Profile"""

    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    GENDER_OTHER = "Other"

    DEGREE_BS = "Bachelors"
    DEGREE_MS = "Masters"
    DEGREE_PHD = "Phd"

    DIET_VEG = "Vegetarian"
    DIET_NON_VEG = "Non Vegetarian"

    COURSE_CS = "Computer Science"
    COURSE_CE = "Computer Engineering"
    COURSE_EE = "Electrical Engineering"
    COURSE_MEC = "Mechanical Engineering"

    BLANK = "--"
    NO_PREF = "No Preference"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    DEGREE_CHOICES = (
        (DEGREE_BS, "Bachelors Program (BS)"),
        (DEGREE_MS, "Masters Program (MS)"),
        (DEGREE_PHD, "Post Docterate (PHD)"),
    )

    COURSE_CHOICES = (
        (COURSE_CS, "Computer Science"),
        (COURSE_CE, "Computer Engg."),
        (COURSE_EE, "Electrical Engg."),
        (COURSE_MEC, "Mechanical Engg."),
    )

    DIET_CHOICES = ((DIET_VEG, "Veg"), (DIET_NON_VEG, "Non Veg"))

    PREF_GENDER_CHOICES = (
        (NO_PREF, "No Preference"),
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    PREF_DEGREE_CHOICES = (
        (NO_PREF, "No Preference"),
        (DEGREE_BS, "Bachelors Program (BS)"),
        (DEGREE_MS, "Masters Program (MS)"),
        (DEGREE_PHD, "Post Docterate (PHD)"),
    )

    PREF_DIET_CHOICES = (
        (NO_PREF, "No Preference"),
        (DIET_VEG, "Veg"),
        (DIET_NON_VEG, "Non Veg"),
    )

    PREF_COURSE_CHOICES = (
        (NO_PREF, "No Preference"),
        (COURSE_CS, "Computer Science"),
        (COURSE_CE, "Computer Engg."),
        (COURSE_EE, "Electrical Engg."),
        (COURSE_MEC, "Mechanical Engg."),
    )

    """User Profile Model"""
    name = models.CharField(max_length=100, default="")
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    hometown = models.CharField(max_length=100, default="", blank=True)

    gender = models.CharField(
        max_length=128, choices=GENDER_CHOICES, blank=True
    )
    degree = models.CharField(
        max_length=128, choices=DEGREE_CHOICES, blank=True
    )
    diet = models.CharField(max_length=128, choices=DIET_CHOICES, blank=True)
    country = CountryField(blank_label="Select Country", blank=True)
    course = models.CharField(
        max_length=128, choices=COURSE_CHOICES, blank=True
    )

    visibility = models.BooleanField(default=True)
    is_profile_complete = models.BooleanField(default=False)
    profile_photo = models.ImageField(
        default="default.png", upload_to="profile_pics"
    )

    # preferences

    preference_gender = models.CharField(
        max_length=128, choices=PREF_GENDER_CHOICES, default=NO_PREF
    )
    preference_degree = models.CharField(
        max_length=128, choices=PREF_DEGREE_CHOICES, default=NO_PREF
    )
    preference_diet = models.CharField(
        max_length=128, choices=PREF_DIET_CHOICES, default=NO_PREF
    )
    preference_country = CountryField(
        blank_label="No Preference", blank=True, default="No Preference"
    )
    preference_course = models.CharField(
        max_length=128, choices=PREF_COURSE_CHOICES, default=NO_PREF
    )

    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}-profile"


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    """Create User Profile"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    """Save User Profile"""
    instance.profile.save()

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender.username}: {self.content[:50]}'