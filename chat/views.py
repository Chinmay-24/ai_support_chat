# chat/views.py
import uuid
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .services.mongo import save_message, get_conversation_messages
from .services.gemini import generate_ai_reply

# chat/views.py
from django.shortcuts import render
import uuid

# simple page views used by urls.py
def home_page(request):
    return render(request, "chat/home.html")

def dashboard_page(request):
    context = {"total_conversations": 0, "total_messages": 0}
    return render(request, "chat/dashboard.html", context)

def conversations_page(request):
    return render(request, "chat/conversations.html")

def chat_page(request):
    conversation_id = request.GET.get("conversation_id") or str(uuid.uuid4())
    return render(request, "chat/chat.html", {"conversation_id": conversation_id})

def profile_page(request):
    user = {"name": "Chinmay Naik", "role": "Developer", "email": "you@example.com"}
    return render(request, "chat/profile.html", {"user": user})

def settings_page(request):
    return render(request, "chat/settings.html")

def help_page(request):
    return render(request, "chat/help.html")

def chat_page(request):
    """
    Renders the HTML chat page.
    Generates a new conversation_id if one is not provided.
    """
    conversation_id = request.GET.get("conversation_id") or str(uuid.uuid4())
    return render(request, "chat/chat.html", {"conversation_id": conversation_id})

@csrf_exempt  # for quick dev; later handle CSRF properly
def api_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user_message = data.get("message")
    conversation_id = data.get("conversation_id")

    if not user_message or not conversation_id:
        return JsonResponse({"error": "message and conversation_id are required"}, status=400)

    # 1. Save user message
    save_message(role="user", content=user_message, conversation_id=conversation_id)

    # 2. Get conversation history for context
    history_docs = get_conversation_messages(conversation_id, limit=20)
    history = [
        {"role": doc["role"], "content": doc["content"]}
        for doc in history_docs
    ]

    # 3. Call Gemini
    system_prompt = "You are an AI support assistant. Be concise and helpful."
    ai_reply = generate_ai_reply(history, system_prompt=system_prompt)

    # 4. Save AI message
    save_message(role="assistant", content=ai_reply, conversation_id=conversation_id)

    return JsonResponse({
        "reply": ai_reply,
        "conversation_id": conversation_id,
    })

def api_messages(request):
    conversation_id = request.GET.get("conversation_id")
    if not conversation_id:
        return JsonResponse({"error": "conversation_id is required"}, status=400)

    docs = get_conversation_messages(conversation_id, limit=50)
    messages = []
    for d in docs:
        messages.append({
            "id": str(d["_id"]),
            "role": d["role"],
            "content": d["content"],
            "created_at": d["created_at"].isoformat()
        })
    return JsonResponse({"messages": messages})
