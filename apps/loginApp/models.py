##### Belt Exam - Login App
##### Mason Brewer
##### November 19th, 2018

from __future__ import unicode_literals
from django.db import models
import re, bcrypt
    
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def doesExist(email):
    allUsers = User.objects.all()
    if len(allUsers) == 0:
        return False
    for user in allUsers:
        if(email == user.email):
            return True
    return False

def passwordMatch(password, thisEmail):
    user = User.objects.get(email = thisEmail)
    return bcrypt.checkpw(password.encode(), user.passHash.encode())

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['firstName']) < 2:
            errors["firstName"] = "First name should be at least 2 characters."
        if len(postData['lastName']) < 2:
            errors["lastName"] = "Last name should be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors["emailRegex"] = "Invalid email address."
        if doesExist(postData['email']):
            errors["emailExists"] = "Email is already assigned to a user."
        if len(postData['password']) < 8 or postData['password'].isalpha() or postData['password'].islower():
            errors["password"] = "Invalid password. Your password must be 8 or more characters, have a nubmer, and an uppercase letter."
        if postData['password'] != postData['passwordAgain']:
            errors['passwordAgain'] = "Passwords must match."
        return errors

    def login_validator(self, postData):
        errors = {}
        if not doesExist(postData['email']) or not passwordMatch(password = postData["password"], thisEmail = postData["email"]):
            errors["invalidLogin"] = "Invalid login credentials."
        return errors

class User(models.Model):
    username = models.CharField(max_length = 50)
    location = models.CharField(max_length = 50)
    email = models.CharField(max_length = 255)
    passHash = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BandManager(models.Manager):
    def miscValidator(self, postData):
        pass

class Band(models.Model):
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 255)
    subcribers = models.ManyToManyField(User, related_name="subscriptions")
    picLink = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    passHash = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BandManager()

class EventManager(models.Manager):
    def miscValidator(self, postData):
        pass

class Event(models.Model):
    data = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    band = models.ForeignKey(User, related_name="events")
    picLink = models.CharField(max_length = 255)
    attendants = models.ManyToManyField(User, related_name="eventsAttending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()