from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse

from django.contrib.auth import login,authenticate,logout
from testApp.models import Post,comment,Profile
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.core.mail import send_mail
from testApp.forms import SendEmailForm,CommentForm,SignUpForm,EditProfileForm,EditSignUpForm,UserLoginForm
from verify_email.email_handler import send_verification_email
# Create your views here.

def search_venue(request):
    if request.method == 'GET':
        searched = request.GET['searched']
        searched_Posts=Post.objects.filter(title__icontains = searched) | Post.objects.filter(body__icontains = searched)
        context={'searched':searched,'searched_Posts':searched_Posts}
        return render(request,'testApp/search_venue.html',context)



def edit_profile(request):
    user_form = EditSignUpForm(instance=request.user)
    try:
        profile_form = EditProfileForm(instance=request.user.profile)
    except:
        profile_form = EditProfileForm()
    if  request.method == "POST":
        user_form = EditSignUpForm(request.POST,instance=request.user)
        try:
            profile_form = EditProfileForm(request.POST,request.FILES, instance=request.user.profile)
        except:
            profile_form = EditProfileForm(request.POST,request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            new_profile = profile_form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            user_form = EditSignUpForm()
            profile_form = EditProfileForm()
            messege = 'your profile has been updated!'
    context = {'user_form':user_form,'profile_form':profile_form}
    return render(request, 'testApp/Edit_profile.html',context)

def post_list_view(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list,2)
    page_number = request.GET.get('page')
    post_list = paginator.get_page(page_number)
    return render(request, 'testApp/blog_list.html',{'post_list':post_list})

def DeleteComment(request,id):
    com = get_object_or_404(comment,id=id)
    com.delete()
    data = {
        'id':id,
        'messege': 'comment deleted'
        }
    return JsonResponse(data,safe=False)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # it return to preveous page

def UpdateComment(request,id):
    com = get_object_or_404(comment,id=id)
    if  request.method == "POST":
        form = CommentForm(request.POST,instance=com)    # if we don't pass instance ,then it will add new records instead of update
        if form.is_valid():
            form.save()
            messege = 'Comment Updated'
    # body_com = request.POST.get("body")
    body_com = com.body
    data = {
    'messege': messege,
    'body_com': body_com
    }
    return JsonResponse(data,safe=False)


# for SEO-friendly URLs
def post_detail_view(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,status='published',
                                            publish__year=year,
                                            publish__month=month,
                                            publish__day=day)
    csubmit = False
    rsubmit = False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            #new_comment = request.POST.get("body")
            #post_id = request.POST.get("post_id")
            comment_id = request.POST.get("comment_id")
            if comment_id == "":
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.Name = request.user
                new_comment.save()
                csubmit = True
                form = CommentForm()
            else:
                comment = post.comments.get(id = comment_id )
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.reply = comment
                new_comment.Name = request.user
                new_comment.save()
                rsubmit = True
                form = CommentForm()    # used for clear the form after submit
    else:
        form = CommentForm()

    comments = post.comments.filter(active=True,reply=None)
    replies = post.comments.filter(active=True).exclude(reply=None)
    replyDict={}
    for rply in replies:
        # print(rply.id)
        # print(rply.reply.id)
        if rply.reply.id not in replyDict.keys():
            replyDict[rply.reply.id]=[rply]
        else:
            replyDict[rply.reply.id].append(rply)
    # print(replyDict,comments)

    context = {'post':post,'form':form,'csubmit':csubmit,'rsubmit': rsubmit,'comments':comments,'replyDict': replyDict}
    return render(request, 'testApp/detail_blog.html', context)

def sinUp_view(request):
    form = SignUpForm()
    messages = ''
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            mail = request.POST['email']
            #user = form.save()
            inactive_user = send_verification_email(request, form)
            form = SignUpForm()
            messages = 'User {} created sucessfully </br> your need to activate your account before login. An account activation link has been sent to your mailbox {}'.format(username,mail)
            #login(request,user)     # here after signUp, user account Logged in direct
    return render(request,'testApp/signup.html',{'form':form,'messages':messages})
    
from django.contrib import messages
def login_view(request):
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username, password=password)
            login(request, user)
            return redirect('/home')
        return render(request, 'testApp/LogIn_form.html',{'form':form})

def logout_view(request):
    logout(request)
    return render(request, 'testApp/logout.html')

def userProfile(request,id):
    return render(request,'testApp/userProfile.html' )


# Like and Dislike

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def AddLike(request, pk):
    print(request.body)     # b'csrfmiddlewaretoken=ucAH7RJPTTl0wj2ff6NNVCcsh5lvo2ePkpevjbpEKhQj07LUhaoH4jzK0TCsMIVq&pk=2'
    print(type(request.body))   # <class 'bytes'>
    print()
    print(request.POST)         # <QueryDict: {'csrfmiddlewaretoken': ['iJUwOnGUTFBtq53J3NtOV16JApEOVsEm8Wyk0HmJK36MUTMo5R4I4It1jdVLj8lX'], 'pk': ['2']}>
    print(type(request.POST))   # <class 'django.http.request.QueryDict'>
    
    if request.user.is_authenticated:
        post = Post.objects.get(pk=pk)

        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        data = {
            'authenticated':True,
            'like': is_like,
            'dislike': is_dislike,
            'total_like': post.likes.all().count()
            }
    else:
        data = {
            'authenticated': False
            }
    return JsonResponse(data,safe=False)


def AddDislike(request,pk):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=pk)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if not is_dislike:
            post.dislikes.add(request.user)
        if is_dislike:
            post.dislikes.remove(request.user)

        data = {
                'authenticated':True,
                'like': is_like,
                'dislike': is_dislike,
                'total_dislike': post.dislikes.all().count()
                }
    else:
        data = {
            'authenticated': False
            }
    return JsonResponse(data,safe=False)

def AddLike_comment(request, pk):
    if request.user.is_authenticated:
        cmnt = comment.objects.get(pk=pk)

        is_likeComment = False
        for like in cmnt.likes_comment.all():
            if like == request.user:
                is_likeComment = True
                break
        if not is_likeComment:
            cmnt.likes_comment.add(request.user)

        if is_likeComment:
            cmnt.likes_comment.remove(request.user)

        data = {
            'authenticated':True,
            'like': is_likeComment,
            'total_like': cmnt.likes_comment.all().count()
            }
    else:
        data = {
            'authenticated': False
            }
    return JsonResponse(data,safe=False)
