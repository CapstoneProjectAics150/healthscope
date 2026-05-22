from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Conversation, Message
from .ai_utils import health_chatbot


# 🔹 Chat Page
def chatbot_page(request):
    return render(request, 'chat/chatbot.html')


# 🔹 API (Main Brain)
def chatbot_api(request):
    if request.method == "POST":
        msg = request.POST.get("message")
        convo_id = request.POST.get("conversation_id")
        user = request.user if request.user.is_authenticated else None

        if not msg:
            return JsonResponse({"reply": "Please enter a message"})

        reply = health_chatbot(msg)

        convo = None

        if user:
            if convo_id:
                convo = Conversation.objects.get(id=convo_id, user=user)
            else:
                # ✅ Create new chat with auto title
                title = msg[:30]
                convo = Conversation.objects.create(user=user, title=title)

            Message.objects.create(conversation=convo, sender="user", content=msg)
            Message.objects.create(conversation=convo, sender="bot", content=reply)

        return JsonResponse({
            "reply": reply,
            "conversation_id": convo.id if convo else None
        })


# 🔹 History Page
@login_required
def history_page(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'chat/history.html', {
        "conversations": conversations
    })


# 🔹 Load Messages
def get_messages(request, conv_id):
    messages = Message.objects.filter(conversation_id=conv_id)

    data = []
    for m in messages:
        data.append({
            "sender": m.sender,
            "content": m.content,
            "time": m.timestamp.strftime("%H:%M")
        })

    return JsonResponse({"messages": data})


# 🔹 Delete Chat
@login_required
def delete_conversation(request, conv_id):
    convo = get_object_or_404(Conversation, id=conv_id, user=request.user)
    convo.delete()
    return JsonResponse({"status": "deleted"})


# 🔹 Rename Chat
@login_required
def rename_conversation(request):
    if request.method == "POST":
        conv_id = request.POST.get("conv_id")
        title = request.POST.get("title")

        convo = Conversation.objects.get(id=conv_id, user=request.user)
        convo.title = title
        convo.save()

        return JsonResponse({"status": "renamed"})