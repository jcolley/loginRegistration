# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, IntegrityError
import bcrypt
import re


# Create your models here.
class UserManager(models.Manager):
    def registerVal(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        if not postData['first_name'] or len(postData['first_name']) < 3:
            results['status'] = False
            results['errors'].append('Please enter a valid first name')
        if not postData['last_name'] or len(postData['last_name']) < 3:
            results['status'] = False
            results['errors'].append('Please enter a valid last name')
        if not postData['email'] or not re.match(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                postData['email']
        ):
            results['status'] = False
            results['errors'].append('Please enter a valid email')
        if not postData['password'] or len(postData['password']) < 8:
            results['status'] = False
            results['errors'].append('Please enter a valid password')
        if postData['password'] != postData['passvalid']:
            results['status'] = False
            results['errors'].append('Passwords do not match')

        user = User.objects.filter(email=postData['email'])

        if results['status']:
            try:
                user = User.objects.create(
                    first_name=postData['first_name'],
                    last_name=postData['last_name'],
                    email=postData['email'],
                    password=(bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())))
                print user.password
                user.save()
                results['user'] = user
            except IntegrityError as e:
                results['status'] = False
                if 'UNIQUE constraint' in e.message:
                    results['errors'].append('That email is already registered.')
                else:
                    results['errors'].append(e.message)
        return results

    def loginVal(self, postData):
        results = {'status': True, 'user': None, 'errors': []}
        try:
            user = User.objects.get(email=postData['email'])
            if user.password == bcrypt.hashpw(postData['password'].encode(), user.password.encode()):
                pass
            else:
                raise Exception()
        except Exception as e:
            results['status'] = False
            results['errors'].append("Incorrect Username or Password")

        if results['status']:
            results['user'] = user
        return results


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=100)

    objects = UserManager()
