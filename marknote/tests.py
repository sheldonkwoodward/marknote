from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

import json

from marknote.models import Folder, Note


class TestNoteLCPost(APITestCase):
    """
    Test cases for POST requests on NoteListCreateView.
    """
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # permissions
        self.user.user_permissions.add(Permission.objects.get(codename='add_note'))
        self.user.user_permissions.add(Permission.objects.get(codename='add_folder'))
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
        self.assertEqual(self.user, note.owner)
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

    def test_note_create_not_authenticated(self):
        """
        Tests that a note is not created when the user is not authenticated.
        """
        # create unauthenticated client
        client = APIClient()
        # create note
        body = {
            'title': 'title',
            'content': 'content',
        }
        response = client.post(reverse('marknote:note-list-create'), body, format='json')
        notes = Note.objects.all()
        # test database
        self.assertEqual(len(notes), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_note_create_not_authorized(self):
        """
        Tests that a note is not created when when the user is authenticated but not authorized.
        """
        # create unauthorized user
        username = 'unauthorized'
        password = 'unauthorized'
        User.objects.create_user(username=username, password=password)
        client = APIClient()
        client.login(username=username, password=password)
        # create note
        body = {
            'title': 'title',
            'content': 'content',
        }
        response = client.post(reverse('marknote:note-list-create'), body, format='json')
        notes = Note.objects.all()
        # test database
        self.assertEqual(len(notes), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestNoteLCGet(APITestCase):
    """
    Test cases for GET requests on NoteListCreateView.
    """
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # permissions
        self.user.user_permissions.add(Permission.objects.get(codename='view_note'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_folder'))
        # log in test client
        self.client.login(username=self.username, password=self.password)

    def test_note_get_none(self):
        """
        Tests that no notes are retrieved when none exist.
        """
        response = self.client.get(reverse('marknote:note-list-create'))
        response_body = json.loads(response.content)
        empty_body = {
            'notes': [],
        }
        self.assertEqual(response_body, empty_body)

    def test_note_get_multiple(self):
        """
        Tests that multiple notes are retrieved when they exist.
        """
        # create notes
        Note(title='title1', content='content1', owner=self.user).save()
        Note(title='title2', content='content2', owner=self.user).save()
        # request
        response = self.client.get(reverse('marknote:note-list-create'))
        response_body = json.loads(response.content)
        # test response
        self.assertEqual(len(Note.objects.all()), 2)
        for db_note, response_note in zip(Note.objects.all(), response_body['notes']):
            self.assertEqual(response_note['pk'], db_note.id),
            self.assertEqual(response_note['title'], db_note.title),
            self.assertEqual(response_note['container'], db_note.container_id),
            self.assertEqual(response_note['created'], db_note.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
            self.assertEqual(response_note['updated'], db_note.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ')),

    # TODO: test filter by title
    # TODO: test filter by content
    # TODO: test filter by title and content
    # TODO: test show only owned notes
    # TODO: test not authenticated
    # TODO: test not authorized
