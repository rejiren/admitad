from django.forms import ModelForm
from django.forms.widgets import SelectMultiple
from users.models import User
from .models import Notification


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'place', 'description', 'participants', 'onset_at']

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.fields["participants"].widget = SelectMultiple()
        if self.initial and self.initial.get('creator'):
            self.instance.creator = self.initial['creator']
            self.fields["participants"].queryset = User.objects.exclude(id=self.instance.creator.id)
