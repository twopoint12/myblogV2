from django import template
from django.db.models.aggregates import Count
from ..models import Article, Category, Tag

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Article.objects.all()[:num]
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Article.objects.dates('created_time', 'month', order='DESC')
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)
    return {
        'category_list': category_list
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)
    return {
        'tag_list': tag_list
    }
