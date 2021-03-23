from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages
from django.db.models import Count
# Create your views here.
def firstPage(request):
    return render(request, "firstPage.html")

def register(request):
    if request.method =="POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email= request.POST['email'], password = pw_hash)
            request.session['user_id'] = user.id
            return redirect('/groups')
    return redirect("/")

def login(request):
    if request.method =="POST":
        user_email = User.objects.filter(email = request.POST['email'])
        if user_email:
            user = user_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect("/groups")
        messages.error(request, "Email or Password are incorrect")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def dashboard(request):
    context = {
        "current_user": User.objects.get(id = request.session['user_id']),
        "all_groups":Group.objects.annotate(member=Count("members")).order_by("-member"),
    }
    return render(request, "dashboard.html", context)

def create_org(request):
    if request.method =="POST":
        errors = Group.objects.org_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/groups")
        else:
            org_create = Group.objects.create(org_name = request.POST['org_name'], description = request.POST['description'], created_user = User.objects.get(id=request.session['user_id']))
            current_user = User.objects.get(id = request.session['user_id'])
            org_create.members.add(current_user)
            return redirect("/groups")
    return redirect("/groups")

def deleteGroup(request, group_id):
    if request.method =="POST":
        group_need_delete = Group.objects.get(id=group_id)
        group_need_delete.delete()
        return redirect("/groups")
    
    
def displayGroup(request, group_id):
    context= {
        "current_group":Group.objects.get(id=group_id),
        "current_user":User.objects.get(id=request.session['user_id'])
    }
    return render(request, "groupInfo.html", context)
def joinGroup(request, group_id):
    if request.method =="POST":
        current_group = Group.objects.get(id=group_id)
        current_user = User.objects.get(id = request.session['user_id'])
        current_group.members.add(current_user)
        return redirect(f"/groups/{current_group.id}")

def leaveGroup(request, group_id):
    if request.method =="POST":
        current_group = Group.objects.get(id=group_id)
        current_user = User.objects.get(id = request.session['user_id'])
        current_group.members.remove(current_user)
        return redirect(f"/groups/{current_group.id}")


