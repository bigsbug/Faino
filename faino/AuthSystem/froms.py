from django import forms
from faino.AuthSystem.models import PermissionGroup, Endpoints
from django.contrib.admin.widgets import FilteredSelectMultiple


class Permissions_Grup_FORM(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Endpoints.objects.all(),
        widget=FilteredSelectMultiple("Permission Name", False),
    )

    class Meta:
        model = PermissionGroup
        fields = ("name",)
