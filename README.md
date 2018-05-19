Django - Hush, Rest.
====================

[![CircleCI](https://circleci.com/gh/lwakefield/django-hush-rest/tree/master.svg?style=svg)](https://circleci.com/gh/lwakefield/django-hush-rest/tree/master)

`djangohushrest` provides a base for simple restful django resources.

## Philosopy

Magic is good, great even. However too much magic can make it too difficult to
understand what is going on (we are talking about programming, not _actual_
magic).

`djangohushrest` aims to strike a balance between magic and simple.

`djangohushrest` should be as extendible as possible, but no more. If
`djangohushrest` cannot be extended to work for you, then forking, or even,
copy pasting `djangohushrest/__init__.py` _will_ work for you.

## Install

```
pip install djangohushrest
```

## Usage

### Basic Usage

From the example "Polls" app from the [django tutorial](https://docs.djangoproject.com/en/2.0/intro/)

```python
# urls.py
from django.urls import path
from django.conf.urls import include
from django.http import HttpResponse

from djangohushrest import Resource

from polls.models import Question

class QuestionsResource(Resource):
    def list(self, request):
        return Question.objects.all()

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


urlpatterns = [
    path('api/questions/', include(QuestionsResource.urls())),
]
````

### Nested Usage

```python
# urls.py

class ChoicesResource(Resource):
    def list(self, request, question_id):
        return Choice.objects.filter(question_id=question_id).all()

    def store(self, request, question_id):
        return Choice.objects.create(
            question_id=question_id,
            choice_text=request.json['choice_text'],
        )

    def show(self, request, question_id, object_id):
        return Choice.objects.get(id=object_id)

urlpatterns = [
    path('api/questions/<question_id>/choices/', include(ChoicesResource.urls())),
]
```

### Respond by http verbs

```python
# Note that these will only work on the parent endpoint
# ie. they will respond on /api/thing/ but not /api/thing/<thing_id>
class VerbResource(Resource):
    def get(self, request):
        pass

    def get(self, request):
        pass

    def head(self, request):
        pass

    def put(self, request):
        pass

    def patch(self, request):
        pass
```

### I don't like the verbs chosen

```python
class BaseResource(Resource):
    def store(self, *args, **kwargs):
        if hasattr(self, 'create') is False:
            return HttpResponseNotFound()

        return self.create(*args, **kwargs)

class QuestionResource(BaseResource):
    def create(self, request):
        pass
```
