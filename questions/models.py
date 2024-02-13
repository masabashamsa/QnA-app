from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# models.py
class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, related_name='question_upvotes')
    downvotes = models.ManyToManyField(User, related_name='question_downvotes')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, related_name='answer_upvotes')
    downvotes = models.ManyToManyField(User, related_name='answer_downvotes')
    upvotes_count = models.PositiveIntegerField(default=0)
    downvotes_count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Answer to {self.question.title}"

class QuestionUpvotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Add other fields as needed