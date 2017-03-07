from django import template

register = template.Library()


@register.filter
def votes(value, question):
    return question.vote_score
