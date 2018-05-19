"""testsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from datetime import datetime

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.http import HttpResponse
from django.core.serializers import serialize
import json

from hushrest import Resource

from polls.models import Choice, Question


class QuestionsResource(Resource):
    def list(self, request, *args, **kwargs):
        questions = Question.objects.all()
        return questions

    def create(self, request, *args, **kwargs):
        return Question.objects.create(
            question_text=request.json['question_text'],
            pub_date=datetime.now()
        )

    def get(self, request, object_id):
        return Question.objects.get(id=object_id)

    def update(self, request, object_id):
        question = Question.objects.get(id=object_id)
        question.question_text = request.json['question_text']
        question.save()
        return question

    def delete(self, request, object_id):
        question = Question.objects.get(id=object_id)
        question.delete()
        return HttpResponse(status=204)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/questions/', include(QuestionsResource.urls())),
]
