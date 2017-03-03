from django import template

register = template.Library()


@register.filter
def votes(value, question):
    return question.votes.count()


@register.filter
def upvote(request, question):
    question.votes.up(request.user.id)


@register.filter
def downvote(request, question):
    question.votes.down(request.user.id)
