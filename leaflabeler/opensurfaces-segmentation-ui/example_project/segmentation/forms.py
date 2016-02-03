from django import forms

class LabelerIDForm(forms.Form):
    labeler_id = forms.IntegerField(label='Please enter your LabelerID')
