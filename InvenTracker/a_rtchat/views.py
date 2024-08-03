from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import ChatRoom, Message
from django.contrib.auth.models import User
from django.db.models import Q 

@login_required
def create_chat_room(request):
    if request.method == 'POST':
        # Get sender and receiver IDs from the form data
        sender_id = request.POST.get('sender_id')
        receiver_id = request.POST.get('receiver_id')
        
        # Fetch the sender and receiver objects from the database
        sender = User.objects.get(pk=sender_id)
        receiver = User.objects.get(pk=receiver_id)
        
        # Check if a chat room already exists between these users
        existing_room = ChatRoom.objects.filter(
            (Q(user1=sender) & Q(user2=receiver)) | (Q(user1=receiver) & Q(user2=sender))
        ).first()

        if existing_room:
            return redirect(reverse('room', kwargs={'room_id': existing_room.id}))
        else:
            # Create a new chat room if one doesn't exist
            new_room = ChatRoom.objects.create(user1=sender, user2=receiver)
            return redirect(reverse('room', kwargs={'room_id': new_room.id}))
    else:
        return redirect('history')  # Redirect to home page if not a POST request
    

@login_required
def hacknite_chat_view(request, room_id):
    # Get the ChatRoom object or return a 404 error if not found
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Filter all message objects related to the given room and order by timestamp
    messages = Message.objects.filter(room=room).order_by('timestamp')
    
    # Pass the room and messages to the template context
    context = {
        'room': room,
        'messages': messages,
    }
    
    # Render the template with the provided context
    return render(request, 'dashboard/chat.html', context)

@login_required
def hacknite_chat_send(request, room_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        print(content)
        room = get_object_or_404(ChatRoom, id=room_id)

        if request.user == room.user1:
            sender = room.user1
            receiver = room.user2
        else:
            sender = room.user2
            receiver = room.user1

        message = Message.objects.create(content=content, sender=sender, receiver=receiver, room=room)
        return redirect('room', room_id=room_id)
    else:
        return redirect('room', room_id=room_id)
