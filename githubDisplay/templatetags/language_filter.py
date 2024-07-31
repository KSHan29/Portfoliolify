from django import template
from .. import utils

register = template.Library()

LANGUAGE_COLORS = utils.get_language_colors()

@register.filter
def language_color(language):
    return LANGUAGE_COLORS.get(language, '#000000')  # Default to black if language not found

@register.filter
def get_language_lines(languages_lines, language):
    return languages_lines.get(language)
