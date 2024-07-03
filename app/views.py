from django.shortcuts import get_object_or_404, render , redirect
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile , Post , Follow , Likes , Comments , Share

def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('feed')  # Replace 'feed' with the URL name of your feed page
        return view_func(request, *args, **kwargs)
    return wrapper


def empty(request):
    return redirect('login')

@redirect_authenticated_user
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('pass')

        print(password)

        if User.objects.filter(username=username).exists():

            user = authenticate(request,username=username,password=password)
            if user != None:

                login(request,user)
                return redirect('profile-settings')
            else:
                messages.error(request,'Wrong Password !')
                return redirect('login')
        else:
            messages.error(request,'Wrong username !')
            return redirect('login')
            

    else:
        return render(request , 'login.html')

@redirect_authenticated_user
def signup(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')


        if pass1 == pass2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=pass1)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                return redirect('login')
            else:
                messages.error(request,'user already exist !')
                return redirect('signup')
        else:
            messages.error(request,'Password mismatch !')
            return redirect('signup')
    else:
        return render(request ,'signup.html')



@login_required
def profile_settings(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)

        
        nickname = request.POST.get('nickname')
        bio = request.POST.get('bio')

        if 'profile-image' in request.FILES:
            image = request.FILES['profile-image']
            profile.profile_image = image


        profile.nickname = nickname
        profile.bio = bio

        profile.save()

        return redirect('feed')
    else:
        return render(request , 'profile_settings.html', {'profile':profile})

# Feed function 

@login_required
def feed(request):
    posts = Post.objects.all()
    profile = Profile.objects.all()

    uPost = []

    followers = []
    follower = Follow.objects.filter(follower=request.user)
    for follow in follower:
        followers.append(follow.following.id)  # Extracting user IDs

    for post in posts:
        post.likes = Likes.objects.filter(post=post).count()
        post.shares = Share.objects.filter(post=post).count()
        post.comments = Comments.objects.filter(post=post).count()
        post.comments_data = Comments.objects.filter(post=post)

        if post.user.id in followers:  # Checking user IDs
            uPost.append(post)

    # Get suggested users
    suggested_users = User.objects.exclude(id__in=followers).exclude(id=request.user.id)[:5]

    context = {
        'posts': uPost,
        'profile': profile,
        'suggested_users': suggested_users
    }
    return render(request, 'feed.html', context)
@login_required
def profile(request,username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    #if user = current user 
    current_user = False
    if user == request.user:
        current_user = True

    #follwers section 
    followers = Follow.objects.filter(following=user).count()
    following = Follow.objects.filter(follower=user).count()
    is_following = Follow.objects.filter(follower=request.user , following=user).exists()

    posts = user.post_set.all()
    posts_count = user.post_set.all().count()
    for post in posts:

        post.likes = Likes.objects.filter(post=post)
        post.comments = Comments.objects.filter(post=post)
        post.share = Share.objects.filter(post=post)

        post.likes_count = Likes.objects.filter(post=post).count()
        post.comments_count = Comments.objects.filter(post=post).count()
        post.share_count = Share.objects.filter(post=post).count()

    context = {
        'profile':profile,
        'posts': posts,
        'followers': followers,
        'following': following,
        'current_user':current_user,
        'is_following': is_following,
        'posts_count':posts_count,
    }
    return render(request,'profile.html',context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

@login_required
def follow(request,username):
    profile_user = get_object_or_404(User,username=username)
    follower = request.user
    Follow.objects.create(follower=follower,following=profile_user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def unfollow(request,username):
    profile_user = get_object_or_404(User,username=username)
    follower = request.user
    Follow.objects.filter(follower=follower,following=profile_user).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def upload_post(request):
        
     
        if request.FILES['file']:
            
            file = request.FILES['file']
            post_type = request.POST.get('content_type')

            if request.POST.get('caption'):
                caption = request.POST.get('caption')
                
                if post_type == "image":
                    Post.objects.create(user=request.user,image=file,caption=caption)
                else:
                    Post.objects.create(user=request.user,video=file,caption=caption)
            else:
                  
                if post_type == "image":
                    Post.objects.create(user=request.user,image=file)
                else:
                    Post.objects.create(user=request.user,video=file)
            
        else:
            messages.info(request,'No file Selected !')
     
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# Explore view 
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, Follow

def explore_view(request):
    query = request.GET.get('q')
    users = []
    if query:
        users = User.objects.filter(Q(username__icontains=query) | Q(profile__nickname__icontains=query))
    
    current_user = request.user
    following = set(Follow.objects.filter(follower=current_user).values_list('following_id', flat=True))
    
    context = {
        'users': users,
        'following': following
    }
    return render(request, 'explore.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def like_post(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # This is an AJAX request
            post_id = request.POST.get('post_id')
            post = Post.objects.get(pk=post_id)
            user = request.user

            # Check if the user has already liked the post
            if Likes.objects.filter(post=post, user=user).exists():
                # Unlike the post
                Likes.objects.filter(post=post, user=user).delete()
            else:
                # Like the post
                Likes.objects.create(post=post, user=user)

            # Get updated like count for the post
            like_count = Likes.objects.filter(post=post).count()

            return JsonResponse({'likes': like_count})
        else:
            # Handle non-AJAX request
            return JsonResponse({'error': 'Invalid request'})
    else:
        # Handle non-POST request
        return JsonResponse({'error': 'Invalid request'})


@csrf_exempt
def comment_post(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # This is an AJAX request
            post_id = request.POST.get('post_id')
            comment_content = request.POST.get('comment')
            post = Post.objects.get(pk=post_id)
            user = request.user

            # Create a new comment for the post
            Comments.objects.create(post=post, user=user, content=comment_content)

            # Get updated comment count for the post
            comment_count = Comments.objects.filter(post=post).count()

            return JsonResponse({'comments': comment_count})
        else:
            # Handle non-AJAX request
            return JsonResponse({'error': 'Invalid request'})
    else:
        # Handle non-POST request
        return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def share_post(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # This is an AJAX request
            post_id = request.POST.get('post_id')
            post = Post.objects.get(pk=post_id)
            user = request.user

            # Create a new share for the post
            Share.objects.create(post=post, user=user)

            # Get updated share count for the post
            share_count = Share.objects.filter(post=post).count()

            return JsonResponse({'shares': share_count})
        else:
            # Handle non-AJAX request
            return JsonResponse({'error': 'Invalid request'})
    else:
        # Handle non-POST request
        return JsonResponse({'error': 'Invalid request'})


# views.py
