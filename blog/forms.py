from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            'user_name':'your name',
            'email' : 'your email',
            'text' : 'your comment'
        }
