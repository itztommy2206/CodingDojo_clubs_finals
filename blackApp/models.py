from django.db import models

# Create your models here.

import re
# Create your models here.
class UserManager (models.Manager):
    def register_validator(self, reqData):
        errors = {}
        if len(reqData['first_name']) < 3:
            errors['first_name'] = "Name must be atleast 3 characters"
        if len(reqData['last_name']) < 2:
            errors['last_name'] = "last name must be atlease 2 characters"
        if len(reqData['password']) < 8:
            errors['password'] = "Password needs to be atleast 8 characters long"
        if reqData['password'] != reqData['password_cf']:
            errors['match'] = 'password does not match'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqData['email']):
            errors['email'] = "invalid email address!"
        email_check = User.objects.filter(email = reqData['email'])
        if len(email_check) >= 1:
            errors['dups'] = "This Email is already taken"
        return errors
class OrgManager(models.Manager):   
    def org_validator(self, reqData):
        errors ={}
        if len(reqData['org_name']) < 1:
            errors['no_empty'] = "Can't sumbit blank"
        if len(reqData['org_name']) < 5:
            errors['org_name'] = "Org name should be atleast 5 characters"
        if len(reqData['description']) < 1:
            errors['nochar'] ="Must have 10 characters"
        if len(reqData['description']) < 10:
            errors['description'] = "description is too short, must be atleast 10 Characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.TextField()
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
 
class Group(models.Model):
    org_name = models.TextField()
    description = models.TextField()
    created_user = models.ForeignKey(User, related_name = "user_created_group", on_delete = models.CASCADE)
    members = models.ManyToManyField(User, related_name = "groups")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = OrgManager()