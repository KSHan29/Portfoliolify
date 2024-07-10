import json
from githubDisplay.models import Project
from django.core import serializers

def gpt_generate_context_json():
    projects = Project.objects.filter(show=True)
    projects_json = serializers.serialize('json', projects)
    return json.loads(projects_json)