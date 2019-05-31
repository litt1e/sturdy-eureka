from django import forms


class CreatingThread(forms.Form):
    title = forms.CharField(max_length=80, label='тема треда:')
    text = forms.CharField(widget=forms.Textarea)


class Reply(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


class Registration(forms.Form):
    nickname = forms.CharField(max_length=20, label='никнейм:')
    email = forms.EmailField(label='почта', required=False)
    password = forms.CharField(widget=forms.PasswordInput)


class LogIn(forms.Form):
    login = forms.CharField(max_length=20, label='логин:')
    password = forms.CharField(widget=forms.PasswordInput)


class AddSection(forms.Form):
    title = forms.CharField(max_length=20, label='название:')


class AddBoard(forms.Form):
    title = forms.CharField(max_length=40, label='полное название:')
    short_title = forms.CharField(max_length=4, label='краткое название:')