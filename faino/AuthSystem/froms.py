from django import forms
from faino.AuthSystem.models import Permission, Endpoint
from django.contrib.admin.widgets import FilteredSelectMultiple


class Permissions_Grup_FORM(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Endpoint.objects.all(),
        widget=FilteredSelectMultiple("Permission Name", False),
    )

    class Meta:
        model = Permission
        fields = ("name",)
