from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if str.isalpha(postData['first_name'])==False:
            errors["first_name_letters"] = "First name should be letters only"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if str.isalpha(postData['last_name'])==False:
            errors["last_name_letters"] = "Last name should be letters only"
        #checking email format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")  
        #checking the uniqueness of the email address
        this_email=User.objects.filter(email=postData['email'])
        if len(this_email)>0:
            errors['unique_email']="This email already exists!"  
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters!"
        #check if passwords are matching
        if postData['confirm_pw']!=postData['password']:
            errors['pw']="Passwords aren't matching!"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=45)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    
