from django.forms import ModelForm
from apps.web_gc.models import Talao


class FormTalao(ModelForm):
    class Meta:
        model = Talao
        fields = ['talao', ]
