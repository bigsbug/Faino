from django import forms
from faino.AuthSystem.models import Permissions_Group, Permissions
from django.contrib.admin.widgets import FilteredSelectMultiple


class Permissions_Grup_FORM(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permissions.objects.all(),
        widget=FilteredSelectMultiple("Permission Name", False),
    )

    class Meta:
        model = Permissions_Group
        fields = ("name",)
