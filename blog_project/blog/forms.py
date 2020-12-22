from django import forms
class EmailSendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)  #since comments is not compulsory,we required more space so text area
    
from blog.models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')   #this is comment form whatever i m taking !!
        #now i want to add this in views file also
        
