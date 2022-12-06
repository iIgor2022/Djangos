from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInLineFormset(BaseInlineFormSet):
    is_main = False
    def clean(self):
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                if self.is_main:
                    raise ValidationError('Основным может быть только один раздел')
                else:
                    self.is_main = form.cleaned_data.get('is_main')

        if not self.is_main:
            raise ValidationError('Укажите основной раздел')

        self.is_main = False
        return super().clean()


class ScopeInLine(admin.TabularInline):
    model = Scope
    formset = ScopeInLineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'published_at', 'image']
    inlines = [ScopeInLine, ]
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    extra = 1