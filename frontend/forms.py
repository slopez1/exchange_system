# forms.py
from django import forms
from django.forms import inlineformset_factory

from core.models import ABSSharedData, Expedient, MedicalHistory, Medication


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


class ExpedientForm(ABSSharedDataForm):
    friendly_name = 'Expedient'

    medical_history_last_visit = forms.DateField(label="last_visit", required=False)
    medical_history_diagnosis = forms.CharField(label="diagnosis", required=False)
    medical_history_allergies = forms.CharField(label="allergies", required=False)

    medication_name = forms.CharField(label="Medication name", required=False)
    medication_dosage = forms.CharField(label="Medication dosage", required=False)
    medication_frequency = forms.CharField(label="Medication frequency", required=False)

    class Meta:
        model = Expedient
        fields = ['identifier',
                  'description',
                  'name',
                  'date_of_birth',
                  'gender',
                  'social_security_number',
                  'address',
                  'phone',
                  'medical_history_last_visit',
                  'medical_history_diagnosis',
                  'medical_history_allergies',
                  'medication_name',
                  'medication_dosage',
                  'medication_frequency'
                  ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(ExpedientForm, self).__init__(*args, **kwargs)
        if instance:
            self.fields['medical_history_last_visit'].initial = instance.medical_history.last_visit
            self.fields['medical_history_diagnosis'].initial = instance.medical_history.diagnosis
            self.fields['medical_history_allergies'].initial = instance.medical_history.allergies
            self.fields['medication_name'].initial = instance.medical_history.medication.name
            self.fields['medication_dosage'].initial = instance.medical_history.medication.dosage
            self.fields['medication_frequency'].initial = instance.medical_history.medication.frequency

    def save(self, commit=True):
        instance = super(ExpedientForm, self).save(commit=False)
        medical_history = instance.medical_history

        if not medical_history:
            medical_history = MedicalHistory()
            instance.medical_history = medical_history

        medical_history.last_visit = self.cleaned_data['medical_history_last_visit']
        medical_history.diagnosis = self.cleaned_data['medical_history_diagnosis']
        medical_history.allergies = self.cleaned_data['medical_history_allergies']

        medication = medical_history.medication
        if not medication:
            medication = Medication()
            medical_history.medication = medication
        medication.name = self.cleaned_data['medication_name']
        medication.dosage = self.cleaned_data['medication_dosage']
        medication.frequency = self.cleaned_data['medication_frequency']
        if commit:
            medication.save()
            medical_history.save()
            instance.save()
        return instance


# ### Example to add diferents models ###
# class MedicalDataForm(ABSSharedDataForm):
#     friendly_name = 'Medical Data'
#
#     class Meta(ABSSharedDataForm.Meta):
#         model = MedicalData
#         fields = ['identifier', 'description', 'name']


CUSTOM_FORMS = [ABSSharedDataForm, ExpedientForm]  # Add your custom forms
# CUSTOM_FORMS = [ABSSharedDataForm, MedicalDataForm ]  # This is and example
