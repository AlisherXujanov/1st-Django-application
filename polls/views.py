from django.shortcuts import render, get_object_or_404
from .models import Question
from django.views.generic import ListView




class QuestionListView(ListView):
    
    context = {
        'questions': Question.objects.all()
    }
    model = Question
    context_object_name = 'questions'
    template_name = 'polls/questions.html'



