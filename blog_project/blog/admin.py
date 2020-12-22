from django.contrib import admin
from blog.models import Post,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','body','publish','created','updated','status']
    list_filter=('status','author','created','publish')  #to add fiter based on status..i.e:all/draft/published.....here comma we compulsorily need to take as uts a single valued tuple
    search_fields=('title','body')
    raw_id_fields=('author',)   # based on id , select the author
    date_hierarchy='publish'
    ordering=['status','publish']
    prepopulated_fields={'slug':('title',)}  #can you please create the slug based on our title automatically for user friendly url and seo

class CommentAdmin(admin.ModelAdmin):
    list_display=('name','email','post','created','updated','active')
    list_filter=('active','created','updated')
    search_fields=('name','email','body')
    
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)

