from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['first_name']) < 3:
            errors['first_name'] = "Name is too short"
        if len(requestPOST['last_name']) < 3:
            errors['last_name'] = "Name is too short"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors['email'] = "Invalid email address"
        if len(requestPOST['password']) < 8:
            errors['password'] = "Password is too short"
        if requestPOST['password'] != requestPOST['password_conf']:
            errors['no_match'] = "Password and Password Confirmation must match"
        return errors
    def quote_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['author']) < 3:
            errors['author'] = "The author's name is too short."
        if len(requestPOST['quote']) < 10:
            errors['quote'] = "Quote must be more than 10 characters."
        return errors
    def update_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['first_name']) < 3:
            errors['first_name'] = "Name is too short."
        if len(requestPOST['last_name']) < 3:
            errors['last_name'] = "Name is too short"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors['email'] = "Invalid email address."
        users_with_email = User.objects.filter(email=requestPOST['email'])
        if len(users_with_email) > 0:
            errors['duplicate'] = "Email already exists."
        return errors

class User(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.TextField()
    quote = models.TextField()
    user = models.ForeignKey(User, related_name="quotes", on_delete=models.CASCADE)
    users_that_liked = models.ManyToManyField(User, related_name="quotes_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
