from django import forms
from blogs.models import Blog, Post


class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blogs title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter blogs description'}),
        }


class CreatePostForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter posts title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type something...'}),
        }


