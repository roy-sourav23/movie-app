from django.forms import ModelForm


class MovieForm(ModelForm):
    name = ModelForm.CharField(max_length=30)
