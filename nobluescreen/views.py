from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.http import HttpResponse, HttpResponseRedirect


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose Password'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

    # class Meta:
    #     model = User
    #     fields = ('username', 'password')
    #     field_classes = {'username': forms.TextInput, 'password': forms.PasswordInput}


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')   # 'home'
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            # user = auth.authenticate(username=username, password=password)
            user = form.get_user()
            # auth.login(request, user)
            next_page = request.GET.get('next')
            # if user is not None:
            auth.login(request, user)
            if next_page:
                return HttpResponseRedirect(next_page)
            return redirect('home')
    else:
        form = LoginForm()
        next_page = request.GET.get('next')
    return render(request, "registration/login.html", {'form': form, 'next': next_page})


def custom_logout(request):
    auth.logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('home')



