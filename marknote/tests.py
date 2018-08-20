from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from marknote.models import Note
import json


class NotePost(APITestCase):
    """
    Test cases for POSTs on '/marknote/note'.
    """
    def setUp(self):
        # TODO: use reverse() to get URI
        self.uri = '/marknote/note'
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = APIClient()

    def test_create_note(self):
        """
        Creates a note with a title and content.
        """
        # create note
        self.client.login(username=self.username, password=self.password)
        body = {
            'title': 'title',
            'content': 'content',
        }
        response = self.client.post(self.uri, body, format='json')
        response_body = json.loads(response.content)

        # check response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check database
        try:
            note = Note.objects.get(title=body['title'], content=body['content'])
        except Note.DoesNotExist:
            self.fail('Did not create note properly.')

        # check response body
        self.assertEqual(response_body['id'], note.id)
        self.assertEqual(response_body['title'], body['title'])
        self.assertEqual(response_body['content'], body['content'])
        self.assertEqual(response_body['timestamp'], note.timestamp)
        self.assertEqual(response_body['containerId'], None)

    # TODO: test_create_in_folder
    # TODO: test_create_only_title
    # TODO: test_create_no_title
    # TODO: test_user_not_authenticated
