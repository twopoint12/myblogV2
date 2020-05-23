from django import template
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, article, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'article': article
    }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, article):
    comment_list = article.comment_set.all()
    comment_count = comment_list.count()
    return {
        'comment_list': comment_list,
        'comment_count': comment_count
    }
