from django import forms
from .models import Project

class ProjectSelectionForm(forms.Form):
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['projects'].queryset = Project.objects.filter(owner=user)
            self.fields['projects'].initial = user.userprofile.selected_projects.all()


    def save(self, user):
        selected_projects = self.cleaned_data['projects']
        user.userprofile.selected_projects.set(selected_projects)
        user.userprofile.save()
