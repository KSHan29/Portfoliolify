# distill_config.py

from django_distill import distill_path
from projects.views import index

def get_index():
    yield None

urlpatterns = [
    distill_path('', index, name='index', distill_func=get_index),
]
