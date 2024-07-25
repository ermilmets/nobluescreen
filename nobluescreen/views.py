from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django import forms


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



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # built-in django
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')   # with SignupForm
            # raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)   # logging in with given data
            return redirect('login')   # 'home'
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {'form': form})

def aboutus(request):
    return render(request, 'aboutus.html')


