try:
    import simplejson as json
except ImportError:
    import json
from django.contrib.auth.decorators import permission_required
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.html import escape

from live_support.forms import ChatMessageForm, ChatForm
from live_support.models import Chat, ChatMessage, SupportGroup


# Специалист присоеденился к чату
@permission_required('live_support.chat_admin')
def join_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user.is_authenticated():
        chat.agents.add(request.user)
        message = ChatMessage()
        name = request.user.first_name or request.user.username
        message.message = '%s присоеденился к чату.' % name
        chat.messages.add(message, bulk=False)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Отправление сообщения специалистом
@permission_required('live_support.chat_admin')
def post_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    last_message_id = request.POST.get('last_message_id')
    message_form = ChatMessageForm(request.POST or None)
    if message_form.is_valid():
        message = message_form.save(commit=False)
        message.chat = chat
        message.agent = request.user
        message.name = message.get_name()
        message.save()
    if request.is_ajax():
        if last_message_id:
            new_messages = chat.messages.filter(id__gt=last_message_id)
        else:
            new_messages = chat.messages.all()
        new_message_list = []
        for message in new_messages:
            new_message_list.append({
                'name': escape(message.name),
                'message': escape(message.message),
                'pk': message.pk,
                'chat': chat.id,
            })
        return HttpResponse(json.dumps(new_message_list))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Завершение чата специалистом
@permission_required('live_support.chat_admin')
def end_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    message = ChatMessage()
    name = request.user.first_name or request.user.username
    message.message = '%s покинул чат.' % name
    chat.messages.add(message, bulk=False)
    if request.POST.get('end_chat') == 'true':
        chat.end()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@permission_required('live_support.chat_admin')
def delete_all_chat(request):
    Chat.objects.all().delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Получить сообщения из чата
@permission_required('live_support.chat_admin')
def get_messages(request):
    user = request.user
    chats = {}
    for k, v in request.GET.items():
        alive = True
        messages = ChatMessage.objects.filter(chat__id=k)
        if v:
            messages = ChatMessage.objects.filter(chat__id=k, id__gt=v)
        if not cache.get('chat_%s' % k):
            alive = False

        message_list = []
        for message in messages:
            message_list.append({
                'name': escape(message.name),
                'message': escape(message.message),
                'pk': message.pk,
            })
        chats[k] = {
            'messages': message_list,
            'alive': alive
        }
    pending_chats = Chat.objects.filter(ended=None) \
        .exclude(agents=user) \
        .order_by('-started')
    groups = SupportGroup.objects.filter(
        Q(supervisors=user) |
        Q(agents=user)
    )
    if groups:
        pending_chats = pending_chats.filter(support_group__in=groups)

    pending_chats = list(pending_chats)
    pending_chats_list = [{
        'name': escape(chat.name),
        'url': reverse(join_chat, args=[chat.id]),
        'active': chat.is_active(),
    } for chat in pending_chats]

    output = {
        'chats': chats,
        'pending_chats': pending_chats_list,
    }
    if groups:
        for group in groups:
            cache.set('admin_active_%s' % group.id, True, 20)
    else:
        cache.set('admin_active', True, 20)
    return HttpResponse(json.dumps(output))


# Клиент запрашивает сообщения
def client_get_messages(request, chat_uuid):
    chat = get_object_or_404(Chat, hash_key=chat_uuid)
    cache.set('chat_%s' % chat.id, 'active', 20)
    messages = chat.messages.all()
    return render(request, 'live_support/live_support.html', {"messages": messages, "chat": chat, "user": request.user})


# Клиент покинул чат
def client_end_chat(request, chat_uuid):
    chat = get_object_or_404(Chat, hash_key=chat_uuid)
    if request.POST.get('end_chat') == 'true':
        message = ChatMessage()
        message.message = '%s покинул чат.' % request.user.username
        chat.messages.add(message, bulk=False)
        chat.end()
    return HttpResponse('Спасибо')


# Клиент отправил сообщение
def client_post_message(request, chat_uuid):
    chat = get_object_or_404(Chat, hash_key=chat_uuid)
    last_message_id = request.POST.get('last_message_id')
    message_form = ChatMessageForm(request.POST or None)
    # если чат закрыт, но клиент еще что-то отправил - переоткрываем
    if chat:
        if chat.ended != None:
            chat.ended = None
            chat.save()
    if message_form.is_valid():
        message = message_form.save(commit=False)
        message.chat = chat
        message.name = str(request.user)
        message.save()
    if last_message_id:
        new_messages = chat.messages.filter(id__gt=last_message_id)
    else:
        new_messages = chat.messages.all()
    new_message_list = []
    for message in new_messages:
        new_message_list.append({
            'name': escape(message.name),
            'message': escape(message.message),
            'pk': message.pk,
            'chat': chat.id,
        })
    return HttpResponse(json.dumps(new_message_list))


# форма отправки сообщения
def client_chat(request, chat_uuid):
    chat = get_object_or_404(Chat, hash_key=chat_uuid)
    message_form = ChatMessageForm(request.POST or None)
    if message_form.is_valid():
        message = message_form.save(commit=False)
        message.chat = chat
        message.name = chat.name
        message.save()
        message_form = ChatMessageForm()

    params = {
        'user': request.user,
        'chat': chat,
        'message_form': message_form,
    }
    return render(request, 'live_support/live_support.html', params)


# Начать чат
def start_chat(request, support_group_id=None):
    chat_form = ChatForm(request.POST or None)
    chat = chat_form.save(commit=False)
    chat.name = request.user
    chat.support_group_id = support_group_id
    chat.save()
    request.session['chat_hash_key'] = str(chat.hash_key)
    print(chat)
    return HttpResponseRedirect(reverse(
        client_chat,
        args=[chat.hash_key, ])
    )
