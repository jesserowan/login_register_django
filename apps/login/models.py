from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def register(self, form):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(form['fname']) < 2:
            errors['fname'] = "Your first name must be at least two characters"
        if len(form['lname']) < 2:
            errors['lname'] = "Your last name must be at least two characters"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Please enter a valid email address"
        if len(User.objects.filter(email=form['email'])) != 0:
            errors['email_in_use'] = "This email is already in use"
        if form['pw'] != form['confirm']:
            errors['match'] = "Please enter the same password in both fields"
        if len(form['pw']) < 8:
            errors['pw_length'] = "Your password must be at least eight characters"
        return errors

    def login(self, form):
        errors = {}
        match = User.objects.filter(email=form['login_email'])
        print(match)
        if len(match) == 0:
            errors['login'] = "Your information is incorrect"
        elif not bcrypt.checkpw(form['login_pass'].encode(), match[0].pw_hash.encode()):
            errors['login'] = "Your information is incorrect"
        return errors

        
        


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
