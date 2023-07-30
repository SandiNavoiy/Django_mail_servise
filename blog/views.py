from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from blog.forms import BlogPostForm
from blog.models import BlogPost
from blog.services import cached_for_blog


# Create your views here.
class BlogListView(ListView):
    """Вывод списка статей блога"""
    model = BlogPost
    template_name = 'blog/blog_post_list.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        return queryset

    # def get_context_data(self, **kwargs):
    #     """фунция вывода + сервисная прослойка для вывода"""
    #     context_data = super().get_context_data()
    #     context_data['blog_post_list'] = cached_for_blog
    #     return context_data
    #


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Создание статьи блога"""
    model = BlogPost
    form_class = BlogPostForm
    login_url = 'users:login'
    redirect_field_name = 'redirect_to'
    template_name = 'blog/blog_post_create.html'
    success_url = reverse_lazy('blog:blog_post_list')  # редирект


class BlogDetailView(DetailView):
    """Вывод конкретной информации по отлельной статье"""
    model = BlogPost
    template_name = 'blog/blog_post_detail.html'

    def get_object(self, queryset=None):
        """Число просмотров"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Обновление статьи блога"""
    model = BlogPost
    form_class = BlogPostForm
    permission_required = "blog.change_blogpost"
    template_name = 'blog/blog_post_form.html'
    login_url = 'users:login'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        """проверка что редактирование доступно владельцу или модератору или root"""
        self.object = self.get_object()
        if self.object.user != self.request.user and not self.request.user.is_staff and not self.request.user.is_superuser:
            raise Http404("Вы не являетесь владельцем этого продукта.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse('blog:detail', args=[self.object.slug])


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление статьи блога"""
    model = BlogPost
    template_name = 'blog/blog_post_delete.html'
    permission_required = "blog.delete_blogpost"
    login_url = 'users:login'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('blog:blog_post_list')

    def dispatch(self, request, *args, **kwargs):
        """проверка что редактирование доступно владельцу или модератору или root"""
        self.object = self.get_object()
        if self.object.user != self.request.user and not self.request.user.is_staff and not self.request.user.is_superuser:
            raise Http404("Вы не являетесь владельцем этого продукта.")

        return super().dispatch(request, *args, **kwargs)
