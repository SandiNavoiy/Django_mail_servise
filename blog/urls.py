from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogDeleteView, BlogCreateView, BlogUpdateView

app_name = BlogConfig.name
urlpatterns = [
    path('list/', BlogListView.as_view(), name='blog_post_list'),
    path('detail/<slug:slug>/', BlogDetailView.as_view(), name='detail'),
    path('delete/<slug:slug>/', BlogDeleteView.as_view(), name='delete'),
    path('create', BlogCreateView.as_view(), name='create'),
    path('update/<slug:slug>/', BlogUpdateView.as_view(), name='update'),

]
