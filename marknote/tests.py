from django.contrib.auth.models import Group, Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

import json

from marknote.models import Note


class TestNotePost(APITestCase):
    """
    Test cases for POSTs on '/marknote/note'.
    """
    def setUp(self):
        # determine endpoint uri
        self.uri = reverse('marknote:note-list-create')
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # permissions
        self.user.user_permissions.add(Permission.objects.get(codename='add_note'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_note'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_note'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_note'))
        # log in test client
        self.client.login(username=self.username, password=self.password)

    def test_create_db_entry(self):
        """
        Tests that a note was properly added to the database.
        """
        # create note
        body = {
            'title': 'title',
            'content': 'content',
        }
        self.client.post(self.uri, body, format='json')
        note = Note.objects.get(title=body['title'], content=body['content'])
        # test database
        self.assertEqual(body['title'], note.title)
        self.assertEqual(body['content'], note.content)

    def test_post_response(self):
        """
        Tests that a note is returned properly in the response.
        """
        # create note
        body = {
            'title': 'title',
            'content': 'content',
        }
        response = self.client.post(self.uri, body, format='json')
        response_body = json.loads(response.content)
        note = Note.objects.get(title=body['title'], content=body['content'])
        # assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['pk'], note.id)
        self.assertEqual(response_body['title'], body['title'])
        self.assertEqual(response_body['containerId'], None)
        self.assertEqual(response_body['created'], note.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(response_body['updated'], note.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

    # TODO: test creating a note in a folder
    # TODO: test creating a note with only a title
    # TODO: test creating a note without a title
    # TODO: test a non-authenticated user
    # TODO: test a user without permissions
    # TODO: test a user with permissions
