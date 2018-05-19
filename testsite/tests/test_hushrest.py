from django.test import TestCase
from django.forms.models import model_to_dict


from polls.models import Question, Choice

class TestResources(TestCase):
    def test_empty_list(self):
        response = self.client.get('/api/questions/')
        assert response.status_code == 200
        assert response.json() == []

    def test_non_empty_list(self):
        Question.objects.create(question_text='foo')
        Question.objects.create(question_text='bar')

        response = self.client.get('/api/questions/')
        assert response.status_code == 200
        json = response.json()
        assert len(json) == 2
        assert json[0]['question_text'] == 'foo'
        assert json[1]['question_text'] == 'bar'

    def test_non_existing_list(self):
        response = self.client.get('/api/questions/1/choices/2/vote/')
        assert response.status_code == 404

    def test_store(self):
        response = self.client.post(
            '/api/questions/',
            '{"question_text": "foo"}',
            'application/json',
        )
        assert response.status_code == 200
        assert response.json()['id'] is not None
        assert response.json()['question_text'] == 'foo'
        assert Question.objects.get(id=response.json()['id']) is not None

    def test_show(self):
        question = Question.objects.create(question_text='foo')
        response = self.client.get('/api/questions/%s' % question.id)
        assert response.status_code == 200
        assert response.json()['id'] == question.id
        assert response.json()['question_text'] == question.question_text

    def test_update(self):
        question = Question.objects.create(question_text='foo')
        response = self.client.patch(
            '/api/questions/%s' % question.id,
            '{"question_text": "bar"}'
        )
        assert response.status_code == 200
        assert response.json()['id'] == question.id
        assert response.json()['question_text'] == 'bar'
        question.refresh_from_db()
        assert question.question_text == 'bar'

    def test_destroy(self):
        question = Question.objects.create(question_text='foo')
        response = self.client.delete(
            '/api/questions/%s' % question.id
        )
        assert response.status_code == 204
        try:
            Question.objects.get(id=question.id)
            assert False
        except Question.DoesNotExist:
            assert True

    def test_nested_resource_list(self):
        question = Question.objects.create(question_text='foo')
        Choice.objects.create(
            choice_text='bar',
            question_id=question.id,
        )
        Choice.objects.create(
            choice_text='baz',
            question_id=question.id,
        )
        response = self.client.get(
            '/api/questions/%s/choices/' % question.id
        )
        assert response.status_code == 200
        json = response.json()
        assert len(json) == 2
        assert json[0]['choice_text'] == 'bar'
        assert json[1]['choice_text'] == 'baz'

    def test_nested_resource_store(self):
        question = Question.objects.create(question_text='foo')
        response = self.client.post(
            '/api/questions/%s/choices/' % question.id,
            '{"choice_text": "bar"}',
            'application/json',
        )
        assert response.status_code == 200
        assert response.json()['id'] is not None
        assert response.json()['choice_text'] == 'bar'
        assert Choice.objects.get(id=response.json()['id']) is not None

    def test_nested_resource_show(self):
        question = Question.objects.create(question_text='foo')
        choice = Choice.objects.create(
            choice_text='bar',
            question_id=question.id,
        )
        response = self.client.get(
            '/api/questions/%s/choices/%s' % (question.id, choice.id),
        )
        assert response.status_code == 200
        assert response.json()['id'] is not None
        assert response.json()['choice_text'] == 'bar'

    def test_post_to_index(self):
        question = Question.objects.create(question_text='foo')
        choice = Choice.objects.create(
            choice_text='bar',
            question_id=question.id,
        )
        response = self.client.post(
            '/api/questions/%s/choices/%s/vote/' % (question.id, choice.id),
            '',
            'application/json'
        )
        assert response.status_code == 200
        assert response.json()['id'] is not None
        assert response.json()['choice_text'] == 'bar'
        assert response.json()['votes'] == 1

    def test_blacklist_for_list(self):
        question = Question.objects.create(question_text='foo')
        response = self.client.get('/api/test/blacklist/')
        assert response.status_code == 200
        json = response.json()
        assert len(json) == 1
        assert json[0]['id'] is not None
        assert json[0]['question_text'] == 'foo'
        assert 'pub_date' not in json[0]

    def test_blacklist_for_show(self):
        question = Question.objects.create(question_text='foo')
        response = self.client.get('/api/test/blacklist/%s' % question.id)
        assert response.status_code == 200
        json = response.json()
        assert json['id'] is not None
        assert json['question_text'] == 'foo'
        assert 'pub_date' not in json

    def test_whitelist_for_list(self):
        question = Question.objects.create(question_text='foo')
        response = self.client.get('/api/test/whitelist/')
        assert response.status_code == 200
        assert response.json() == [{ 'id': question.id }]

    def test_whitelist_for_show(self):
        question = Question.objects.create(question_text='foo')
        response = self.client.get('/api/test/whitelist/%s' % question.id)
        assert response.status_code == 200
        assert response.json() == { 'id': question.id }
