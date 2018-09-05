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
        note = Note.objects.first()
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
        folder = Folder.objects.first()
        # create note
        note_body = {
            'title': 'title',
            'content': 'content',
            'container': folder_response_body['pk'],
        }
        note_response = self.client.post(reverse('marknote:note-list-create'), note_body, format='json')
        note_response_body = json.loads(note_response.content)
        note = Note.objects.first()
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
        response_body = json.loads(response.content)
        notes = Note.objects.all()
        # test database
        self.assertEqual(len(notes), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('pk' in response_body)

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
        # log in test client
        self.client.login(username=self.username, password=self.password)

    def test_note_retrieve_none(self):
        """
        Tests that no notes are retrieved when none exist.
        """
        response = self.client.get(reverse('marknote:note-list-create'))
        response_body = json.loads(response.content)
        empty_body = {
            'notes': [],
        }
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body, empty_body)

    def test_note_retrieve_multiple(self):
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['notes']), 2)
        for db_note, response_note in zip(Note.objects.all(), response_body['notes']):
            self.assertEqual(response_note['pk'], db_note.id),
            self.assertEqual(response_note['title'], db_note.title),
            self.assertEqual(response_note['container'], db_note.container_id),
            self.assertEqual(response_note['created'], db_note.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
            self.assertEqual(response_note['updated'], db_note.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ')),

    def test_note_filter_title(self):
        """
        Tests that notes are filtered appropriately by their title.
        """
        # create notes
        Note(title='ab', content='content', owner=self.user).save()
        note_0 = Note(title='bc', content='content', owner=self.user)
        note_1 = Note(title='cd', content='content', owner=self.user)
        note_0.save()
        note_1.save()
        # request
        response = self.client.get(reverse('marknote:note-list-create') + '?title=c')
        response_body = json.loads(response.content)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['notes']), 2)
        self.assertEqual(response_body['notes'][0]['pk'], note_0.id)
        self.assertEqual(response_body['notes'][1]['pk'], note_1.id)

    def test_note_filter_content(self):
        """
        Tests that notes are filtered appropriately by their title.
        """
        # create notes
        Note(title='title', content='ab', owner=self.user).save()
        note_0 = Note(title='title', content='bc', owner=self.user)
        note_1 = Note(title='title', content='cd', owner=self.user)
        note_0.save()
        note_1.save()
        # request
        response = self.client.get(reverse('marknote:note-list-create') + '?content=c')
        response_body = json.loads(response.content)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['notes']), 2)
        self.assertEqual(response_body['notes'][0]['pk'], note_0.id)
        self.assertEqual(response_body['notes'][1]['pk'], note_1.id)

    def test_note_filter_title_and_content(self):
        """
        Tests that notes are filtered appropriately by their title and content.
        """
        # create notes
        Note(title='a', content='1', owner=self.user).save()
        Note(title='c', content='3', owner=self.user).save()
        note_0 = Note(title='ab', content='13', owner=self.user)
        note_1 = Note(title='ac', content='23', owner=self.user)
        note_0.save()
        note_1.save()
        # request
        response = self.client.get(reverse('marknote:note-list-create') + '?title=a&content=3')
        response_body = json.loads(response.content)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['notes']), 2)
        self.assertEqual(response_body['notes'][0]['pk'], note_0.id)
        self.assertEqual(response_body['notes'][1]['pk'], note_1.id)

    def test_note_retrieve_owned(self):
        """
        Tests that only notes that are owned are retrieved.
        """
        # create notes
        note = Note(title='title', content='content', owner=self.user)
        note.save()
        Note(title='title', content='content', owner=User.objects.create_user(username='other_user')).save()
        # request
        response = self.client.get(reverse('marknote:note-list-create'))
        response_body = json.loads(response.content)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['notes']), 1)
        self.assertEqual(response_body['notes'][0]['pk'], note.id)

    def test_note_retrieve_not_authenticated(self):
        """
        Tests that a note is not created when the user is not authenticated.
        """
        # create unauthenticated client
        client = APIClient()
        # request
        response = client.get(reverse('marknote:note-list-create'))
        response_body = json.loads(response.content)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('notes' in response_body)


class TestNoteRUDGet(APITestCase):
    """
    Test cases for GET requests on NoteRetrieveUpdateDestroyView.
    """
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # log in test client
        self.client.login(username=self.username, password=self.password)

    def test_note_retrieve(self):
        """
        Tests that the proper note is retrieved.
        """
        # create notes
        note = Note(title='title1', content='content1', owner=self.user)
        note.save()
        Note(title='title2', content='content2', owner=self.user).save()
        # request
        response = self.client.get(reverse('marknote:note-retrieve-update-destroy', args=[note.id]))
        response_body = json.loads(response.content)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], note.id)
        self.assertEqual(response_body['title'], note.title)
        self.assertEqual(response_body['container'], None)
        self.assertEqual(response_body['created'], note.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(response_body['updated'], note.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

    def test_note_does_not_exist(self):
        """
        Tests that no note is retrieved if the id specified does not exist.
        """
        # create note
        note = Note(title='title1', content='content1', owner=self.user)
        note.save()
        # request
        response = self.client.get(reverse('marknote:note-retrieve-update-destroy', args=['2']))
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_note_retrieve_not_owned(self):
        """
        Tests that notes that are not owned are not retrieved.
        """
        # create notes
        note = Note(title='title', content='content', owner=User.objects.create_user(username='other_user'))
        note.save()
        # request
        response = self.client.get(reverse('marknote:note-retrieve-update-destroy', args=[note.id]))
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_note_retrieve_not_authenticated(self):
        """
        Tests that a note is not retrieved when the user is not authenticated.
        """
        # create unauthenticated client
        client = APIClient()
        # create notes
        note = Note(title='title', content='content', owner=self.user)
        note.save()
        # request
        response = client.get(reverse('marknote:note-retrieve-update-destroy', args=[note.id]))
        response_body = json.loads(response.content)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('pk' in response_body)


class TestNoteRUDPut(APITestCase):
    """
    Test cases for PUT requests on NoteRetrieveUpdateDestroyView.
    """
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # permissions
        self.user.user_permissions.add(Permission.objects.get(codename='change_note'))
        # log in test client
        self.client.login(username=self.username, password=self.password)

    # TODO: test_note_update_full
    def test_note_update_full(self):
        """
        Tests that a full note update executes properly.
        """
        # create note and folder
        note = Note(title='title', content='content', owner=self.user)
        note.save()
        folder = Folder(title='title', owner=self.user)
        folder.save()
        # request
        body = {
            'title': 'title changed',
            'content': 'content changed',
            'container': folder.id,
        }
        response = self.client.put(reverse('marknote:note-retrieve-update-destroy', args=[note.id]), body, format='json')
        response_body = json.loads(response.content)
        # test database
        note = Note.objects.first()
        self.assertEqual(body['title'], note.title)
        self.assertEqual(body['content'], note.content)
        self.assertEqual(folder, note.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['title'], body['title'])
        self.assertEqual(response_body['content'], body['content'])
        self.assertEqual(response_body['container'], folder.id)

    # TODO: test_note_update_partial
    # TODO: test_note_update_container_does_not_exist
    # TODO: test_note_update_read_only_fields
    # TODO: test_note_update_not_owned
    # TODO: test_note_update_not_authenticated
    # TODO: test_note_update_not_authorized
