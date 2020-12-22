from django.shortcuts import render,get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag

# Create your views here.
def post_list_view(request,tag_slug=None):    #if tag_slug is not passing then its value is None only
    post_list=Post.objects.all()  #when this method is called then internally get_queryset method will be called......this post.objects.all method will display all published and draft blogs on page ,so to overcome this we need custom
    tag=None
    if tag_slug:  #if you are passing tag_slug
        tag=get_object_or_404(Tag,slug=tag_slug)  #create object for tag_slug
        post_list=post_list.filter(tags__in=[tag])   #filter related post from all post accoding to tag
        
    
    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list,'tag':tag})

# from django.views.generic import ListView   #we are doing paginate in a very easy way by using class based views..CBV
# class PostListView(ListView):   #this is stanby for paginate
#     model=Post                  #......//.......
#     paginate_by=1              #.....//......Now i want to add something in url.py
#

from blog.forms import CommentForm

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    
    comments=post.comments.filter(active=True)  #show active comments related to that post
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)  #get new comment but dont save in the database
            new_comment.post=post
            new_comment.save()
            csubmit=True
        
    else:
        form=CommentForm()

    return render(request,'blog/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})

#for mail sending purpose:
from django.core.mail import send_mail   #import statement not necessarily/compulsorily at top
from blog.forms import EmailSendForm     #importing form from forms.py file

def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published') #based on id ,can you plz prob=vided published post to me
    sent=False   #let by default sent is FALSE
    if request.method=='POST':     #it will post data after clicking submit button
        form=EmailSendForm(request.POST)
        if form.is_valid():    #simple validation
            cd=form.cleaned_data   #end user provided data is present in this dictionary
            subject='{}({}) recomends you to read"{}"'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())   #its used to get complete url ...bracket part taken from models.py to take part of url after http.127.0.0.1:800/
            message='Read Post At:\n {} \n\n{}\'s Comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'durga@blog.com',[cd['to']])     #here cd['to'] means receiver for mail
            sent=True
        else:
            form=EmailSendForm()   #else can you plz create form
    form=EmailSendForm()
    return render(request,'blog/sharebymail.html',{'form':form,'post':post,'sent':sent})
