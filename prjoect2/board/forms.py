from django import forms

class LoginForm(forms.Form):
    login_id= forms.CharField(label="아이디", max_length=100, required=True)
    login_pw = forms.CharField(label="패스워드", max_length=100, required=True, widget=forms.PasswordInput)