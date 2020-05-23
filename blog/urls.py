from django.urls import path

from . import views
from blog.feeds import AllPostsRssFeed

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('all/rss/', AllPostsRssFeed(), name='rss'),
    path('search/', views.search, name='search'),
    path('about_site/', views.AboutSiteView.as_view(), name='about_site'),
    path('about_me/', views.AboutMeView.as_view(), name='about_me'),
    path('update_likes/', views.update_likes, name='update_likes'),
]