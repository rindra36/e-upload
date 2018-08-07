from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Comment


class LogForm(AuthenticationForm):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Username',
            }
        )
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Password'
            }
        )
    )

    class meta:
        model = User
        fields = (
            'username',
            'password'
        )


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        label='First Name',
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'placeholder': 'First Name'
            }
        )
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Last Name'
            }
        )
    )
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Username'
            }
        )
    )
    email = forms.EmailField(
        max_length=254,
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Email'
            }
        )
    )
    password1 = forms.CharField(
        label="Password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Password'
            }
        )
    )
    password2 = forms.CharField(
        label='Confirmation Password',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Confirmation Password'
            }
        )
    )
    avatar = forms.ImageField(
        required=False
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            'avatar'
        )


class PostForm(forms.ModelForm):
    choice = (('False', 'Friends only'), ('True', 'Public'))
    content = forms.CharField(
        label='Message',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Your message',
                'style': 'width: auto'
            }
        )
    )
    file = forms.ImageField(
        label='Attached File',
        required=True,
        widget=forms.FileInput(
            attrs={
                'style': 'width: auto'
            }
        )
    )
    privacy = forms.ChoiceField(
        label='Privacy',
        choices=choice,
        widget=forms.Select(
            attrs={
                'class': 'ui dropdown privacyChoice',
                'style': 'width: auto'
            }
        )
    )

    class Meta:
        model = Post
        fields = (
            'content',
            'file',
            'privacy'
        )


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Add comment...'
            }
        )
    )

    class Meta:
        model = Comment
        fields = (
            'comment',
        )
