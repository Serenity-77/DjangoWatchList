from django import forms


class RegisterForm(forms.Form):

    firstname = forms.CharField(
        max_length=50, label="First Name",
        widget=forms.TextInput(attrs={'fa': 'fas fa-user'})
    )

    lastname = forms.CharField(
        max_length=50, label="Last Name",
        widget=forms.TextInput(attrs={'fa': 'fas fa-user'}))

    username = forms.CharField(
        max_length=50, label="Username",
        widget=forms.TextInput(attrs={'fa': 'fas fa-user'})
    )

    password = forms.CharField(
        max_length=50, label="Password",
        widget=forms.TextInput(attrs={'fa': 'fas fa-lock'})
    )

    repassword = forms.CharField(
        max_length=50, label="Retype Password",
        widget=forms.TextInput(attrs={'fa': 'fas fa-lock'})
    )

    def clean(self):
        cleaned_data = self.cleaned_data

        password = cleaned_data.get("password")

        if not password:
            return

        repassword = cleaned_data.get("repassword")

        if password != repassword:
            self.add_error("repassword", "Password not match.")
