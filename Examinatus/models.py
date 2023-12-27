from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Test(models.Model):
	name = models.CharField("Название", max_length=20)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_creator')


class Question(models.Model):
	text = models.TextField()
	answer = models.TextField()
	test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='question_test')


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_question')
	answer = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_user')
	is_right = models.BooleanField()


class TestUsers(models.Model):
	test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_user')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testUser_user')