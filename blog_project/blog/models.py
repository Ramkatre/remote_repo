from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class CustomManager(models.Manager):    #as i want to show only published post on page
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

# Create your models here.
from taggit.managers import TaggableManager
class Post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=256)
    slug=models.SlugField(max_length=264,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)  #the time at which post has been created that time automatically considered
    updated=models.DateTimeField(auto_now=True) #the time at which the updated data is being saved
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects=CustomManager()
    tags=TaggableManager()

    class Meta:
        ordering=('-publish',) #single valued tuple must be ends with comma

    def __str__(self):
        return self.title   #based on name in url ,can you please provide the url ..its the mean of this below line
    def get_absolute_url(self):
        return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])

# Model Related to comments section

class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE) #if you want to access all comments related to post in reverse here we required to use related_name=comments
    #for which purpose we are using related_name,
    # for exa::i got Post object and i want know all commentts related to this post then i will just call
    # post.comments      & i will get all comments related to that post i am going to get  
    name=models.CharField(max_length=32)   #these three things onnly captured from end user
    email=models.EmailField() #these three things onnly captured from end use
    body=models.TextField()  #these three things onnly captured from end use
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=('-created',)  #the recent created comment show first
    def __str__(self):
        return 'Commented By {} on {}'.format(self.name,self.post)




