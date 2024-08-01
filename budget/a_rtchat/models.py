from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

# class ChatGroup(models.Model):
#   group_name = models.CharField(max_length=128,unique=True)

#   def __str__(self):
#     return self.group_name
  
# class GroupMessage(models.Model):
#   group = models.ForeignKey(ChatGroup,related_name='chat_messages',on_delete=models.CASCADE)
#   author = models.ForeignKey(User,on_delete=models.CASCADE)
#   body = models.CharField(max_length=300)
#   created  = models.DateTimeField(auto_now_add=True)

#   def __str__(self):
#     return f'{self.author.username} : {self.body}'
  
#   class Meta:
#     ordering = ['-created']
class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat room between {self.user1.username} and {self.user2.username}"
class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', default=1)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content}"