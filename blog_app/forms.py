from djrichtextfield.widgets import RichTextWidget
from django.forms import ValidationError
from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment
from.models import Category

# if we want to hard code categories into select field we can just do so by passing in python list
# (choice name, choice value)
# choices = [('Programming', 'Programming'),
#            ('Gaming', 'Gaming'), ('Sports', 'Sports')]

# better way is to get categories from the Category model

choices = Category.objects.all().values_list('name', 'name')


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'author']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title of your post'}),

            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'write something here . . .'}),

            'author': forms.TextInput(attrs={'class': 'form-control', 'id': 'authorbox', "type": "hidden", "value": ""}),

            'category': forms.Select(choices=choices, attrs={'class': 'form-control'})
        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter any new category'}),
        }

    def clean_name(self):
        entered_cat = self.cleaned_data.get('name').capitalize()

        category = Category.objects.filter(name=entered_cat)

        if category:
            raise ValidationError("Category already exists!")
        else:
            return entered_cat.capitalize()


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'write your comment here . . .'}),
        }
