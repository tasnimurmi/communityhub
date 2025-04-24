from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import *
from .forms import *
import os
from django.conf import settings

# Create your views here.
@login_required
def home(request):
    posts = Post.objects.all().order_by('-timestamp') 
    if request.method == "POST":
        if "like_post" in request.POST:
            post_id = request.POST.get("post_id")
            post = get_object_or_404(Post, id=post_id)
            
            if request.user in post.likes.all():
                post.likes.remove(request.user)  
                liked = False
            else:
                post.likes.add(request.user) 
                liked = True
            
            return redirect("home")  
        
        if "contents" in request.POST:  
            post_id = request.POST.get("post_id")
            contents = request.POST.get("contents")
            post = get_object_or_404(Post, id=post_id)

            # Create comment
            Comment.objects.create(
                post=post,
                user=request.user,
                contents=contents,
            )
            return redirect("home")  

    context = {'post': posts}
    return render(request, template_name="Home/home.html", context=context)


@login_required
def forum(request):
    forums = Forum.objects.all().order_by('-time')  

    if request.method == "POST":
        post_id = request.POST.get("post_id")
        forum = get_object_or_404(Forum, id=post_id)
        if "upvote" in request.POST:
            if request.user in forum.upvotes.all():
                forum.upvotes.remove(request.user)  
            else:
                forum.upvotes.add(request.user) 
                forum.downvotes.remove(request.user) 

        elif "downvote" in request.POST:
            if request.user in forum.downvotes.all():
                forum.downvotes.remove(request.user) 
            else:
                forum.downvotes.add(request.user)  
                forum.upvotes.remove(request.user) 

        elif "contents" in request.POST:  
            contents = request.POST.get("contents")
            ForumComment.objects.create(
                forum=forum,
                user=request.user,
                contents=contents,
            )
            return redirect("forum")

        return redirect("forum")

    context = {'forum': forums}
    return render(request, "Home/forum.html", context)




@login_required
def createpost(request):
    post=Post.objects.all()
    context={
        'post':post,
    }
    return render(request,template_name="Home/createpost.html",context=context)






@login_required
def clubdetails(request):
    club=Club.objects.all()
    context={
        'club':club,
    }
    return render(request,template_name="Home/clubdetails.html",context=context)

def login(request):
    if request.method == "POST":
        username = request.POST.get('name')  
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  

    return render(request, template_name="register/login.html")

# Signup Page
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        User_Profile.objects.create(user=user)
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')

    return render(request, template_name="register/signup.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')



#upload post(Create) 
@login_required
def upload_post(request):
    form=PostForm()
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('home')
    context={'form':form}
    return render(request,template_name="allforms\postform.html",context=context)


@login_required
def update_post(request,id):
    post=Post.objects.get(pk=id)
    if request.user != post.user:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('home')
    if request.user != post.user:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('home')
    form=PostForm(instance=post)
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('home')
    context={'form':form}
    return render(request,template_name="allforms\postform.html",context=context)


@login_required
def delete_post(request,id):
    post=Post.objects.get(pk=id)
    if request.user != post.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('home')

    if request.user != post.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('home')

    if request.method=='POST':
        post.delete()
        return redirect('home')
    return render(request,template_name="allforms/delete_post.html")

@login_required
def upload_query(request):
    form=ForumPost_Form()
    if request.method=='POST':
        form=ForumPost_Form(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('forum')
    context={'form':form}
    return render(request,template_name="allforms\postform.html",context=context)


@login_required
def update_query(request,id):
    forum=Forum.objects.get(pk=id)
    if request.user != forum.user:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('home')
    if request.user != forum.user:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('home')
    form=ForumPost_Form(instance=forum)
    if request.method=='POST':
        form=ForumPost_Form(request.POST,request.FILES,instance=forum)
        if form.is_valid():
            forum=form.save(commit=False)
            forum.user=request.user
            forum.save()
            return redirect('forum')
    context={'form':form}
    return render(request,template_name="allforms\postform.html",context=context)


@login_required
def delete_query(request,id):
    forum=Forum.objects.get(pk=id)
    if request.user != forum.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('home')
    if request.user != forum.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('home')
    if request.method=='POST':
        forum.delete()
        return redirect('forum')
    return render(request,template_name="allforms/delete_query.html")


@login_required
def resources(request):
    resource=Resources.objects.all()
    context={
        'resource':resource
    }
    return render(request,template_name="Home/resources.html",context=context)


@login_required
def upload_resource(request):
    form = Resource_Form()
    if request.method == 'POST':
        form = Resource_Form(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('resources')
    context = {'form':form}
    return render(request, template_name='allforms/resourceform.html',context=context)


@login_required
def update_resource(request,id):
    resource = Resources.objects.get(pk=id)
    form = Resource_Form(instance=resource)
    if request.method=='POST':
        form = Resource_Form(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            resource=form.save(commit=False)
            resource.user=request.user
            resource.save()
            return redirect('resources')
    context = {'form':form}
    return render(request,template_name='allforms/resourceform.html', context=context)

@login_required
def delete_resource(request, id):
    # Get the resource object
    resource = get_object_or_404(Resources, pk=id)

    if request.method == 'POST':
        # Delete the file from the file system if it exists
        if resource.resource:
            resource_path = os.path.join(settings.MEDIA_ROOT, resource.resource.name)
            if os.path.exists(resource_path):
                os.remove(resource_path)

        # Delete the resource object from the database
        resource.delete()

        # Redirect to the resources page
        return redirect('resources')

    return render(request, template_name='allforms/deleteresource.html')



@login_required
def profile(request):
    # Get the logged-in user's profile
    user_profile = get_object_or_404(User_Profile, user=request.user)

    user_posts = Post.objects.filter(user=request.user).order_by('-timestamp')

    print(user_posts)
    context = {
        'user_profile': user_profile,
        'user_posts': user_posts,
    }
    return render(request, template_name='Home/profile.html', context=context)


@login_required
def edit_profile(request):
    user_profile = request.user.profile
    form = UserProfileForm(instance=user_profile,user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')

    context = {'form': form}
    return render(request, 'allforms/edit_profile.html', context=context)



    
##alumni

def alumni_section(request):
    alumni_list = Alumni.objects.all()
    context = {
        'alumni_list': alumni_list,
    }
    return render(request, 'Home/alumni_section.html', context)