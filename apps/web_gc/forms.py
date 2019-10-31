from django.forms import ModelForm
from apps.web_gc.models import Talao, EntregaTalao


class FormTalao(ModelForm):
    class Meta:
        model = Talao
        fields = ['talao', ]


class FormEntregaTalao(ModelForm):
    class Meta:
        model = EntregaTalao
        fields = ['talao', ]
