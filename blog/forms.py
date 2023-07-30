from django.utils.text import slugify
from blog.models import BlogPost
from django import forms
class BlogPostForm(forms.ModelForm):
    """Форма создания блога"""
    class Meta:
        model = BlogPost
        exclude = ['created_at', 'views_count', 'slug', 'user']

    def clean_title(self):
        """метод валидации по запрерщенным словам"""
        cleaned_data = self.cleaned_data.get('title')
        if cleaned_data in ("казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"):
            raise forms.ValidationError('Запрещенное слово')
        return cleaned_data
    def clean_content(self):
        """метод валидации по запрерщенным словам"""
        cleaned_data = self.cleaned_data.get('content')
        if cleaned_data in ("казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"):
            raise forms.ValidationError('Запрещенное слово')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance
