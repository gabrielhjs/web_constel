from django import forms
from django.core.validators import FileExtensionValidator

from constel.forms import DateInput


class FormUploadCSV(forms.Form):
  data = forms.DateField(label="Data de referência", widget=DateInput(), required=True)
  file_csv = forms.FileField(
    label="arquivo",
    required=True,
    validators=[FileExtensionValidator(allowed_extensions=["csv"], message="Formato inválido")]
  )

  def __init__(self, *args, **kwargs):
    super(FormUploadCSV, self).__init__(*args, **kwargs)

    for key in self.fields.keys():
      self.fields[key].widget.attrs.update({'class': 'form-control'})

  def clean(self):
    form_data = super(FormUploadCSV, self).clean()

    print(self.errors)
