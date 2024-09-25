from django import template
from django.core.cache import cache
from waffle import flag_is_active

from apps.teams.models import Flag

register = template.Library()


@register.simple_tag(takes_context=True)
def is_flag_active(context, flag_name, slug):
    request = context['request']
    cache_key = f'is_flag_active_{flag_name}_{slug}'
    flag_active = cache.get(cache_key)  # Try to get the result from cache

    if flag_active is None:
        flag_active = False  # Initialize the flag_active variable

        if flag_is_active(request, flag_name):
            try:
                flag = Flag.objects.get(name=flag_name)
                if flag.everyone and flag.teams.filter(slug=slug).exists():
                    flag_active = True
            except Flag.DoesNotExist:
                pass  # flag_active remains False

        cache.set(cache_key, flag_active, timeout=600)  # Cache the result for 10 minutes

    return flag_active
