from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=50, label="Username",
        widget=forms.TextInput(attrs={'fa': 'fas fa-user'})
    )

    password = forms.CharField(
        max_length=50, label="Password",
        widget=forms.TextInput(attrs={'fa': 'fas fa-lock'})
    )
