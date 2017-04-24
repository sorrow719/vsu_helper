from django.contrib import admin
from django.db.models import Q

from live_support.models import Chat, ChatMessage, SupportGroup


class SupportGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    filter_horizontal = ('agents', 'supervisors',)


class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'started',)
    list_display_links = ('id', 'name',)
    list_filter = ('started',)

    class Media:
        js = (
            "js/jquery/jquery.js",
            "js/bootstrap/bootstrap.js",
            "live_support/js/live_support_admin.js"
        )
        css = {
            'all': ('css/livechat.css','css/bootstrap/bootstrap.css'),
        }

    def changelist_view(self, request, extra_context=None):
        user = request.user
        pending_chats = Chat.objects.filter(ended=None) \
            .exclude(agents=user) \
            .order_by('-started')
        groups = SupportGroup.objects.filter(
            Q(supervisors=user) |
            Q(agents=user)
        )
        if groups:
            pending_chats = pending_chats.filter(support_group__in=groups)
        active_chats = Chat.objects.filter(ended=None) \
            .filter(agents=request.user)
        c = {
            'pending_chats': pending_chats,
            'active_chats': active_chats,
        }
        return super(ChatAdmin, self).changelist_view(request, extra_context=c)


admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatMessage)
admin.site.register(SupportGroup, SupportGroupAdmin)
