from venv import create
from django.db import models

# Create your models here.
class Question(models.Model):
    subject     = models.CharField(max_length=200)
    content     = models.TextField()
    create_date = models.DateTimeField()

    # id 값 대신 제목 표시
    def __str__(self):
        return self.subject

class Answer(models.Model):
    question    = models.ForeignKey(Question, on_delete=models.CASCADE)     # Question 모델을 속성으로 가져가기 위해 ForeignKey, on_delete=models.CASCADE는 질문 삭제시 답변도 자동 삭제
    content     = models.TextField()
    create_date = models.DateTimeField()



