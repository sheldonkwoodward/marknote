from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import json

from marknote.models import Folder, Note


class TestNotePost(APITestCase):
    """
    Test cases for POSTs on '/marknote/note'.
    """
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # permissions
        self.user.user_permissions.add(Permission.objects.get(codename='add_note'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_note'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_note'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_note'))
        self.user.user_permissions.add(Permission.objects.get(codename='add_folder'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_folder'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_folder'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_folder'))
        # log in test client
        self.client.login(username=self.username, password=self.password)

    def test_note_create(self):
        """
        Tests that a note was properly created.
        """
        # create note
        body = {
            'title': 'title',
            'content': 'content',
        }
        response = self.client.post(reverse('marknote:note-list-create'), body, format='json')
        response_body = json.loads(response.content)
        note = Note.objects.get(title=body['title'], content=body['content'])
        # test database
        self.assertEqual(body['title'], note.title)
        self.assertEqual(body['content'], note.content)
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['pk'], note.id)
        self.assertEqual(response_body['title'], body['title'])
        self.assertEqual(response_body['container'], None)
        self.assertEqual(response_body['created'], note.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(response_body['updated'], note.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

    def test_note_create_in_folder(self):
        """
        Tests that a note in a folder was properly created.
        """
        # create folder
        folder_body = {
            'title': 'folder',
        }
        folder_response = self.client.post(reverse('marknote:folder-list-create'), folder_body, format='json')
        folder_response_body = json.loads(folder_response.content)
        folder = Folder.objects.get(title=folder_body['title'])
        # create note
        note_body = {
            'title': 'title',
            'content': 'content',
            'container': folder_response_body['pk'],
        }
        note_response = self.client.post(reverse('marknote:note-list-create'), note_body, format='json')
        note_response_body = json.loads(note_response.content)
        note = Note.objects.get(title=note_body['title'], content=note_body['content'])
        # test database
        self.assertEqual(note.container.id, note_body['container'])
        self.assertEqual(note.container, folder)
        # test note_response
        self.assertEqual(note_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(note_response_body['container'], folder_response_body['pk'])
        # test database against note_response
        self.assertEqual(note.container.id, note_response_body['pk'])

    def test_note_create_no_title(self):
        """
        Tests that a note is not created without a title.
        """
        # create note
        body = {
            'content': 'content',
        }
        response = self.client.post(reverse('marknote:note-list-create'), body, format='json')
        notes = Note.objects.all()
        # test database
        self.assertEqual(len(notes), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_note_create_no_content(self):
        """
        Tests that a note is not created without content.
        """
        # create note
        body = {
            'title': 'title',
        }
        response = self.client.post(reverse('marknote:note-list-create'), body, format='json')
        notes = Note.objects.all()
        # test database
        self.assertEqual(len(notes), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TODO: test a non-authenticated user
    # TODO: test a user without permissions
    # TODO: test a user with permissions
