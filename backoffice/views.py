from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from stronghold.decorators import public
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturaltime
from django import forms

from .models import Post, Comment, Profile
from .forms import SignupForm, PostForm, CommentForm
from eboutique import settings


# Create your views here.
def dashboard(request):
    userPost = Post.objects.filter(user_id=request.user.id).order_by('-date_post')[:5]
    allPost = Post.objects.all().order_by('-date_post')[:5]
    if request.method == 'POST':
        postForm = PostForm(request.POST, request.FILES)
        validate_post(request, postForm)
    else:
        postForm = PostForm()
    return render(
        request,
        'backoffice/index.html',
        {
            'postForm': postForm,
            'userPost': userPost,
            'allPost': allPost
        }
    )


def view_user_post(request):
    # Getting Current User's Post
    getPost = Post.objects.filter(user_id=request.user.id).order_by('-date_post')
    page = request.GET.get('page', 1)
    paginator = Paginator(getPost, 5)

    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        postForm = PostForm(request.POST, request.FILES)
        validate_post(request, postForm)
    else:
        postForm = PostForm()
    return render(
        request,
        'backoffice/my_post.html',
        {
            'post': post,
            'postForm': postForm,
        }
    )


def view_all_post(request):
    # Getting Current User's Post
    getPost = Post.objects.all().order_by('-date_post')
    page = request.GET.get('page', 1)
    paginator = Paginator(getPost, 5)

    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        postForm = PostForm(request.POST, request.FILES)
        validate_post(request, postForm)
    else:
        postForm = PostForm()
    return render(
        request,
        'backoffice/all_post.html',
        {
            'post': post,
            'postForm': postForm,
        }
    )


def displaypost(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        commentForm = CommentForm(request.POST)
    else:
        commentForm = CommentForm()
    if (Comment.objects.filter(post_id=post_id).exists()):
        comments = Comment.objects.filter(post_id=post_id)
        return render(
            request,
            'backoffice/post.html',
            {
                'post': post,
                'comments': comments,
                'commentForm': commentForm
            }
        )
    else:
        return render(
            request,
            'backoffice/post.html',
            {
                'post': post,
                'commentForm': commentForm
            }
        )


def validate_post(request, form):
    if form.is_valid():
        post = form.save(commit=False)
        post.user_id = request.user.id
        post.file = form.cleaned_data.get('file')
        post.save()
        return redirect('backoffice/my_post.html')


@csrf_exempt
def commentpost(request, post_id):
    if request.method == 'POST':
        postForm = Post.objects.get(pk=post_id)
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.user_id = request.user.id
            comment.post_id = postForm.id
            postForm.comment_count = postForm.comment_count + 1
            postForm.save()
            comment.save()
            userData = serialize('json', [request.user, ])
            avatarData = serialize('json', [request.user.profile, ]),
            data = {
                'id_comment': comment.id,
                'id_post': postForm.id,
                'user': userData,
                'avatar': avatarData,
                'date_comment': naturaltime(datetime.now()),
                'comment': commentForm.cleaned_data.get('comment')
            }

            return JsonResponse(data)
    else:
        commentForm = CommentForm()
        postForm = Post.objects.get(pk=post_id)
        comment = Comment.objects.filter(post=post_id).reverse()
    return render(
        request,
        'backoffice/post.html',
        {
            'commentForm': commentForm,
            'postForm': postForm,
            'comment': comment
        }
    )


def likepost(request, post_id):
    postForm = Post.objects.get(pk=post_id)
    postForm.votes = postForm.votes + 1
    postForm.save()
    data = {
        'id_post': postForm.id
    }
    return JsonResponse(data)


def deletecomment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    post = Post.objects.get(pk=comment.post_id)
    post.comment_count = post.comment_count - 1
    comment.delete()
    post.save()
    data = {
        'id_comment': comment.id,
        'id_post': comment.post_id
    }
    return JsonResponse(data)


def deletepost(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()

    return redirect('/backoffice/my_post')


def profile(request, user_id):
    userProfile = Profile.objects.get(user_id=user_id)
    return render(
        request,
        'backoffice/profile.html',
        {
            'userProfile': userProfile,
        }
    )


@public
def signup(request):
    if request.user.is_authenticated:
        return render(request, 'backoffice/index.html')
    if request.method == 'POST':
        userForm = SignupForm(request.POST, request.FILES)
        if userForm.is_valid():
            user = userForm.save()
            user.refresh_from_db()
            user.profile.avatar = userForm.cleaned_data.get('avatar')
            user.save()
            # Log in after successfully created user
            username = user.username
            password = userForm.cleaned_data.get('password1')
            user = authenticate(
                username=username,
                password=password,
            )
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            raise forms.ValidationError(
                'Username with that password already exist !'
            )
    else:
        userForm = SignupForm()
    return render(
        request,
        'registration/signup.html',
        {
            'userForm': userForm
        }
    )
