from django.contrib import admin
from models import Snippet, Language


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'language_code', 'admin_get_use_count')

admin.site.register(Language, LanguageAdmin)


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_name', 'user', 'pub_date', 'accessibility', 'expiration')
    list_filter = ('accessibility', 'language')
    date_hierarchy = 'pub_date'
    search_fields = ('title',)

admin.site.register(Snippet, SnippetAdmin)
