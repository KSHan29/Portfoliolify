from githubDisplay.models import ResumeSummary
from django.core.serializers import serialize

def get_resume_summary(reqest, user):
    resume_exists = ResumeSummary.objects.filter(user=user).exists()
    resume_instance = None
    if resume_exists:
        resume_instance = ResumeSummary.objects.get(user=user)
        return serialize('json', [resume_instance])
    return resume_instance
