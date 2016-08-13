from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.simple_tag(takes_context=True)
def absolute_url(context, url, *args, **kwargs):
    return context['request'].build_absolute_uri(reverse(url, *args, **kwargs))

@register.simple_tag(takes_context=True)
def build_absolute_url(context, url):
    return context['request'].build_absolute_uri(url)
