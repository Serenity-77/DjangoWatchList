from django import forms


class MoviesForm(forms.Form):

    start = forms.IntegerField(required=True)
    length = forms.IntegerField(required=True)


class WatchListForm(forms.Form):

    movie_id = forms.IntegerField(required=False)
    note = forms.CharField(required=False)
