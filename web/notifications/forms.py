from django.forms import ModelForm
from django.forms.widgets import SelectMultiple
from users.models import User
from .models import Notification


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'place', 'description', 'participants', 'onset_at']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.fields["participants"].widget = SelectMultiple()
        self.fields["participants"].queryset = User.objects.exclude(id=user.id)
