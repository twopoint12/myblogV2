from blog.models import Article
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm


@require_POST
def comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.save()
        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        return redirect(article)

    context = {
        'article': article,
        'form': form
    }
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
