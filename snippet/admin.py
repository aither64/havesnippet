from django.contrib import admin
from models import Snippet, Language, Bookmark


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'language_code', 'admin_get_use_count')

admin.site.register(Language, LanguageAdmin)


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'pub_date', 'accessibility', 'expiration', 'rating',
                    'featured')
    list_editable = ('featured',)
    list_filter = ('featured', 'accessibility', 'language')
    date_hierarchy = 'pub_date'
    search_fields = ('title',)

admin.site.register(Snippet, SnippetAdmin)


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('owner', 'snippet', 'user', 'follow')

admin.site.register(Bookmark, BookmarkAdmin)
