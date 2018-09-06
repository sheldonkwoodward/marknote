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
        # view name
        self.view_name = 'marknote:note-list-create'

    def test_note_create(self):
        """
        Tests that a note was properly created.
        """
        # create note
        body = {
            'title': 'title',
            'content': 'content',
        }
        response = self.client.post(reverse(self.view_name), body)
        response_body = json.loads(response.content.decode('utf-8'))
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
        folder = Folder(title='top', owner=self.user)
        folder.save()
        # create note
        note_body = {
            'title': 'title',
            'content': 'content',
            'container': folder.id,
        }
        note_response = self.client.post(reverse(self.view_name), note_body)
        note_response_body = json.loads(note_response.content.decode('utf-8'))
        note = Note.objects.first()
        # test database
        self.assertEqual(note.container.id, note_body['container'])
        self.assertEqual(note.container, folder)
        # test note_response
        self.assertEqual(note_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(note_response_body['container'], folder.id)
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
        response = self.client.post(reverse(self.view_name), body)
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
        response = self.client.post(reverse(self.view_name), body)
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
        response = client.post(reverse(self.view_name), body)
        response_body = json.loads(response.content.decode('utf-8'))
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
        response = client.post(reverse(self.view_name), body)
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
        # view name
        self.view_name = 'marknote:note-list-create'

    def test_note_retrieve_none(self):
        """
        Tests that no notes are retrieved when none exist.
        """
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
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
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['notes']), 2)
        for db_note, response_note in zip(Note.objects.all(), response_body['notes']):
            self.assertEqual(response_note['pk'], db_note.id)
            self.assertEqual(response_note['title'], db_note.title)
            self.assertEqual(response_note['container'], db_note.container_id)
            self.assertEqual(response_note['created'], db_note.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
            self.assertEqual(response_note['updated'], db_note.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

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
        response = self.client.get(reverse(self.view_name) + '?title=c')
        response_body = json.loads(response.content.decode('utf-8'))
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
        response = self.client.get(reverse(self.view_name) + '?content=c')
        response_body = json.loads(response.content.decode('utf-8'))
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
        response = self.client.get(reverse(self.view_name) + '?title=a&content=3')
        response_body = json.loads(response.content.decode('utf-8'))
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
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
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
        response = client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
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
        # view name
        self.view_name = 'marknote:note-retrieve-update-destroy'

    def test_note_retrieve(self):
        """
        Tests that the proper note is retrieved.
        """
        # create notes
        note = Note(title='title1', content='content1', owner=self.user)
        note.save()
        Note(title='title2', content='content2', owner=self.user).save()
        # request
        response = self.client.get(reverse(self.view_name, args=[note.id]))
        response_body = json.loads(response.content.decode('utf-8'))
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
        response = self.client.get(reverse(self.view_name, args=['2']))
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
        response = self.client.get(reverse(self.view_name, args=[note.id]))
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
        response = client.get(reverse(self.view_name, args=[note.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('pk' in response_body)


class TestNoteRUDPutPatch(APITestCase):
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
        # view name
        self.view_name = 'marknote:note-retrieve-update-destroy'

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
        response = self.client.put(reverse(self.view_name, args=[note.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
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

    def test_note_update_partial(self):
        """
        Tests that a partial note update executes properly.
        """
        # create note
        original_title = 'title'
        original_content = 'content'
        note = Note(title=original_title, content=original_content, owner=self.user)
        note.save()
        # request
        body = {
            'title': 'title changed',
        }
        response = self.client.patch(reverse(self.view_name, args=[note.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        note = Note.objects.first()
        self.assertEqual(body['title'], note.title)
        self.assertEqual(original_content, note.content)
        self.assertEqual(None, note.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['title'], body['title'])
        self.assertEqual(response_body['content'], original_content)
        self.assertEqual(response_body['container'], None)

    def test_note_update_container_does_not_exist(self):
        """
        Tests that a note cannot be updated with a non-existent container.
        """
        # create note and folder
        original_title = 'title'
        original_content = 'content'
        note = Note(title=original_title, content=original_content, owner=self.user)
        note.save()
        # request
        body = {
            'container': '1',
        }
        response = self.client.patch(reverse(self.view_name, args=[note.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        note = Note.objects.first()
        self.assertEqual(original_title, note.title)
        self.assertEqual(original_content, note.content)
        self.assertEqual(None, note.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse('pk' in response_body)

    def test_note_update_read_only_fields(self):
        """
        Tests that read only fields cannot be updated.
        """
        # create note
        original_note = Note(title='title', content='title', owner=self.user)
        original_note.save()
        # request
        body = {
            'pk': '2',
            'created': '2018-09-04T16:30:28.469865Z',
            'updated': '2018-09-04T16:30:28.469865Z',
        }
        response = self.client.patch(reverse(self.view_name, args=[original_note.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        note = Note.objects.first()
        self.assertEqual(original_note, note)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response_body['pk'], body['pk'])
        self.assertNotEqual(response_body['created'], body['created'])
        self.assertNotEqual(response_body['updated'], body['updated'])

    def test_note_update_not_owned(self):
        """
        Tests that notes that are note owned are not updated.
        """
        # create note
        original_title = 'title'
        original_content = 'content'
        note = Note(title=original_title,
                    content=original_content,
                    owner=User.objects.create_user(username='other_user'))
        note.save()
        # request
        body = {
            'title': 'title changed',
        }
        response = self.client.patch(reverse(self.view_name, args=[note.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        note = Note.objects.first()
        self.assertEqual(original_title, note.title)
        self.assertEqual(original_content, note.content)
        self.assertEqual(None, note.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('pk' in response_body)

    def test_note_update_not_authenticated(self):
        """
        Tests that a note is not retrieved when a user is not authenticated.
        """
        # create unauthenticated client
        client = APIClient()
        # create note
        original_title = 'title'
        original_content = 'content'
        note = Note(title=original_title, content=original_content, owner=self.user)
        note.save()
        # request
        body = {
            'title': 'title changed',
        }
        response = client.patch(reverse(self.view_name, args=[note.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        note = Note.objects.first()
        self.assertEqual(original_title, note.title)
        self.assertEqual(original_content, note.content)
        self.assertEqual(None, note.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('pk' in response_body)

    def test_note_update_not_authorized(self):
        """
        Tests that a note is not retrieved when a user is not authorized.
        """
        # create unauthorized user
        username = 'unauthorized'
        password = 'unauthorized'
        User.objects.create_user(username=username, password=password)
        client = APIClient()
        client.login(username=username, password=password)
        # create note
        original_title = 'title'
        original_content = 'content'
        note = Note(title=original_title, content=original_content, owner=self.user)
        note.save()
        # request
        body = {
            'title': 'title changed',
        }
        response = client.patch(reverse(self.view_name, args=[note.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        note = Note.objects.first()
        self.assertEqual(original_title, note.title)
        self.assertEqual(original_content, note.content)
        self.assertEqual(None, note.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('pk' in response_body)


class TestNoteRUDDelete(APITestCase):
    """
    Test cases for DELETE requests on NoteRetrieveUpdateDestroyView.
    """
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # permissions
        self.user.user_permissions.add(Permission.objects.get(codename='delete_note'))
        # log in test client
        self.client.login(username=self.username, password=self.password)
        # view name
        self.view_name = 'marknote:note-retrieve-update-destroy'

    def test_note_destroy(self):
        """
        Tests that a note is properly destroyed.
        """
        # create note
        note = Note(title='title', content='content', owner=self.user)
        note.save()
        # request
        response = self.client.delete(reverse(self.view_name, args=[note.id]))
        # test database
        notes = Note.objects.all()
        self.assertEqual(len(notes), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_note_does_not_exist(self):
        """
        Tests that destroying a non-existent note does not affect other notes.
        """
        # create note
        note = Note(title='title', content='content', owner=self.user)
        note.save()
        # request
        response = self.client.delete(reverse(self.view_name, args=['2']))
        # test database
        notes = Note.objects.all()
        self.assertEqual(len(notes), 1)
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_note_destroy_not_owned(self):
        """
        Tests that notes that are not owned are not destroyed.
        """
        # create note
        note = Note(title='title', content='content', owner=User.objects.create_user(username='other_user'))
        note.save()
        # request
        response = self.client.delete(reverse(self.view_name, args=[note.id]))
        # test database
        notes = Note.objects.all()
        self.assertEqual(len(notes), 1)
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_note_destroy_not_authenticated(self):
        """
        Tests that a note is not destroyed when a user is not authenticated.
        """
        # create unauthenticated client
        client = APIClient()
        # create note
        note = Note(title='title', content='content', owner=self.user)
        note.save()
        # request
        response = client.delete(reverse(self.view_name, args=[note.id]))
        # test database
        notes = Note.objects.all()
        self.assertEqual(len(notes), 1)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_note_destroy_not_authorized(self):
        """
        Tests that a note is not destroyed when a user is not authorized.
        """
        # create unauthorized user
        username = 'unauthorized'
        password = 'unauthorized'
        User.objects.create_user(username=username, password=password)
        client = APIClient()
        client.login(username=username, password=password)
        # create note
        note = Note(title='title', content='content', owner=self.user)
        note.save()
        # request
        response = client.delete(reverse(self.view_name, args=[note.id]))
        # test database
        notes = Note.objects.all()
        self.assertEqual(len(notes), 1)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
