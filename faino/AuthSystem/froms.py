from django import forms
from faino.AuthSystem.models import Permission, Endpoint
from django.contrib.admin.widgets import FilteredSelectMultiple


class PermissionForm(forms.ModelForm):
    endpoints = forms.ModelMultipleChoiceField(
        queryset=Endpoint.objects.all(),
        widget=FilteredSelectMultiple("Endpoints name", False),
    )

    class Meta:
        model = Permission
        fields = ("name",)
