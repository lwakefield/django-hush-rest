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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.http import HttpResponse
from django.core.serializers import serialize

from djangohushrest import Resource

from polls.models import Choice, Question


class QuestionsResource(Resource):
    def list(self, request):
        questions = Question.objects.all()
        return questions

    def store(self, request, *args, **kwargs):
        return Question.objects.create(
            question_text=request.json['question_text']
        )

    def show(self, request, object_id):
        return Question.objects.get(id=object_id)

    def update(self, request, object_id):
        question = Question.objects.get(id=object_id)
        question.question_text = request.json['question_text']
        question.save()
        return question

    def destroy(self, request, object_id):
        question = Question.objects.get(id=object_id)
        question.delete()
        return HttpResponse(status=204)


class ChoicesResource(Resource):
    def list(self, request, question_id):
        choices = Choice.objects.filter(question_id=question_id).all()
        return choices

    def store(self, request, question_id):
        return Choice.objects.create(
            question_id=question_id,
            choice_text=request.json['choice_text'],
        )

    def show(self, request, question_id, object_id):
        return Choice.objects.get(id=object_id)


class VoteResource(Resource):
    def post(self, request, question_id, choice_id):
        choice = Choice.objects.get(id=choice_id)
        choice.votes += 1
        choice.save()
        return choice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/questions/', include(QuestionsResource.urls())),
    path('api/questions/<question_id>/choices/', include(ChoicesResource.urls())),
    path('api/questions/<question_id>/choices/<choice_id>/vote/', include(VoteResource.urls())),
]
