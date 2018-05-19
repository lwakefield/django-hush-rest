import json

from django.urls import path
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.core.serializers import serialize
from django.db.models import Model, QuerySet
from django.forms.models import model_to_dict

class Resource:
    blacklist = {}
    whitelist = {}

    def parent(self, request, *args, **kwargs):
        request.json = json.loads(request.body) if request.body else None

        fn = None
        if hasattr(self, request.method.lower()):
            fn = getattr(self, request.method.lower())
        elif request.method in {'HEAD', 'GET'}:
            fn = self.list
        elif request.method == 'POST':
            fn = self.store
        else:
            return HttpResponseBadRequest()

        result = fn(request, *args, **kwargs)
        return self.prepare_result(result)

    def child(self, request, *args, **kwargs):
        request.json = json.loads(request.body) if request.body else None

        fn = None
        if request.method in {'HEAD', 'GET'}:
            fn = self.show
        elif request.method in {'PUT', 'PATCH'}:
            fn = self.update
        elif request.method == 'DELETE':
            fn = self.destroy
        else:
            return HttpResponseBadRequest()

        result = fn(request, *args, **kwargs)
        return self.prepare_result(result)

    def prepare_result(self, result):
        if isinstance(result, HttpResponse):
            return result

        if isinstance(result, Model):
            return HttpResponse(
                # trim the beginning and ending square brackets
                json.dumps(self.serialize(result), default=str),
                content_type="application/json"
            )

        if isinstance(result, QuerySet):
            return HttpResponse(
                json.dumps(
                    [
                        self.serialize(item)
                        for item in result
                    ],
                    default=str
                ),
                content_type="application/json"
            )

        return HttpResponseBadRequest()

    def serialize(self, obj):
        result = model_to_dict(obj)
        if self.whitelist:
            result = {
                k: v
                for k,v in result.items()
                if k in self.whitelist
            }
        result = {
            k: v
            for k,v in result.items()
            if k not in self.blacklist
        }

        return result

    def list(self, *args, **kwargs):
        return HttpResponseNotFound()

    def store(self, *args, **kwargs):
        return HttpResponseNotFound()

    def show(self, *args, **kwargs):
        return HttpResponseNotFound()

    def update(self, *args, **kwargs):
        return HttpResponseNotFound()

    def destroy(self, *args, **kwargs):
        return HttpResponseNotFound()

    @classmethod
    def urls(cls):
        inst = cls()
        return [
            path('', inst.parent),
            path('<object_id>', inst.child),
        ]
