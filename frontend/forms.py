# forms.py
from django import forms

from core.models import ABSSharedData


class ABSSharedDataForm(forms.ModelForm):
    # Override this class to add new forms

    friendly_name = 'Generic_Data'  # This field need to override on each inheritance, no spaces allowed

    class Meta:
        model = ABSSharedData
        fields = ['identifier', 'description']

    def __init__(self, *args, **kwargs):
        super(ABSSharedDataForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        instance = kwargs.get('instance')
        if instance:
            self.fields['identifier'].widget.attrs['disabled'] = 'disabled'


# ### Example to add diferents models ###
# class MedicalDataForm(ABSSharedDataForm):
#     friendly_name = 'Medical Data'
#
#     class Meta(ABSSharedDataForm.Meta):
#         model = MedicalData
#         fields = ['identifier', 'description', 'name']


CUSTOM_FORMS = []  # Add your custom forms
# CUSTOM_FORMS = [ABSSharedDataForm, MedicalDataForm ]  # This is and example
