from django import template
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from live_support.forms import ChatForm

from live_support import views
from live_support.models import Chat

register = template.Library()


# тег для вставки формы чата на страницу
def chat_iframe(context, support_group_id=None):
    request = context['request']
    chat = None
    uuid = None
    if 'chat_hash_key' in request.session:
        uuid = request.session['chat_hash_key']
        if Chat.objects.filter(hash_key=uuid).count()==0:
            uuid = None
    if uuid is None:
        chat = Chat()
        chat.name = request.user
        chat.support_group_id = support_group_id
        chat.save()
        request.session['chat_hash_key'] = str(chat.hash_key)
        cache.set('chat_hash_key%s' % chat.id, 'active', 20)
    else:
        chat = get_object_or_404(Chat, hash_key=uuid)
    return {
        'STATIC_URL': settings.STATIC_URL,
        'chat': chat,
        'request': request,
    }


register.inclusion_tag('live_support/chat_iframe.html', takes_context=True)(chat_iframe)
