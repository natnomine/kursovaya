from django import forms

from messenger.models import Chat, UserProfile


class ChatForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        friends = kwargs.pop("friends")
        super().__init__(*args, **kwargs)
        members = self.fields['members']
        members.help_text = "Удерживайте “Control“ (или “Command“ на Mac), чтобы выбрать несколько значений"
        members.queryset = UserProfile.objects.filter(id__in=friends)

    class Meta:
        model = Chat
        fields = ('name', 'members')


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
