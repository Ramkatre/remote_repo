from blog.models import Post
from django import template
register=template.Library()

@register.simple_tag(name='my_tag')
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('blog/latest_posts123.html')
def show_latest_posts(count=3):   #default value for count is 3 if we dont specify count value in base.html file....Means 3 latest posts will display on sidebar
    latest_posts=Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

from django.db.models import Count
@register.simple_tag
def get_most_commented_posts(count=5):
    #here in below line: get all post and annotate means create the variable name as total_comments where no. of bcomments of all post is stored and then order by make the ordering of that comments from highest o. of comments to lowest no. of commented 
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    