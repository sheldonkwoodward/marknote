from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

import json

from marknote.models import Folder


class TestFolderLCPost(APITestCase):
    """
    Test cases for POST requests on NoteListCreateView.
    """
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # permissions
        self.user.user_permissions.add(Permission.objects.get(codename='add_folder'))
        # log in test client
        self.client.login(username=self.username, password=self.password)
        # view name
        self.view_name = 'marknote:folder-list-create'

    def test_folder_create(self):
        """
        Tests that a folder was properly created.
        """
        # create folder
        body = {
            'title': 'title',
        }
        response = self.client.post(reverse(self.view_name), body)
        response_body = json.loads(response.content.decode('utf-8'))
        folder = Folder.objects.first()
        # test database
        self.assertEqual(body['title'], folder.title)
        self.assertEqual(self.user, folder.owner)
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body['pk'], folder.id)
        self.assertEqual(response_body['title'], body['title'])
        self.assertEqual(response_body['container'], None)
        self.assertEqual(response_body['created'], folder.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(response_body['updated'], folder.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

    def test_folder_create_in_folder(self):
        """
        Tests that a folder in a folder was properly created.
        """
        # create container folder
        top_folder = Folder(title='top', owner=self.user)
        top_folder.save()
        # create another folder
        body = {
            'title': 'title',
            'container': top_folder.id,
        }
        bottom_response = self.client.post(reverse(self.view_name), body)
        bottom_response_body = json.loads(bottom_response.content.decode('utf-8'))
        bottom_folder = Folder.objects.get(title=body['title'])
        # test database
        self.assertEqual(bottom_folder.container.id, body['container'])
        self.assertEqual(bottom_folder.container, top_folder)
        # test folder_response
        self.assertEqual(bottom_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(bottom_response_body['container'], top_folder.id)

    def test_folder_create_no_title(self):
        """
        Tests that a folder is not created without a title.
        """
        # create folder
        body = {}
        response = self.client.post(reverse(self.view_name), body)
        folders = Folder.objects.all()
        # test database
        self.assertEqual(len(folders), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_folder_create_not_authenticated(self):
        """
        Tests that a folder is not created when the user is not authenticated.
        """
        # create unauthenticated client
        client = APIClient()
        # create folder
        body = {
            'title': 'title',
        }
        response = client.post(reverse(self.view_name), body)
        response_body = json.loads(response.content.decode('utf-8'))
        folders = Folder.objects.all()
        # test database
        self.assertEqual(len(folders), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('pk' in response_body)

    def test_folder_create_not_authorized(self):
        """
        Tests that a folder is not created when when the user is authenticated but not authorized.
        """
        # create unauthorized user
        username = 'unauthorized'
        password = 'unauthorized'
        User.objects.create_user(username=username, password=password)
        client = APIClient()
        client.login(username=username, password=password)
        # create folder
        body = {
            'title': 'title',
        }
        response = client.post(reverse(self.view_name), body)
        folders = Folder.objects.all()
        # test database
        self.assertEqual(len(folders), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestFolderLCGet(APITestCase):
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
        self.view_name = 'marknote:folder-list-create'

    def test_folder_retrieve_none(self):
        """
        Tests that no folders are retrieved when none exist.
        """
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        empty_body = {
            'folders': [],
        }
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body, empty_body)

    def test_folder_retrieve_multiple(self):
        """
        Tests that multiple folders are retrieved when they exist.
        """
        # create folders
        Folder(title='title1', owner=self.user).save()
        Folder(title='title2', owner=self.user).save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['folders']), 2)
        for db_folder, response_folder in zip(Folder.objects.all(), response_body['folders']):
            self.assertEqual(response_folder['pk'], db_folder.id)
            self.assertEqual(response_folder['title'], db_folder.title)
            self.assertEqual(response_folder['container'], db_folder.container_id)
            self.assertEqual(response_folder['created'], db_folder.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
            self.assertEqual(response_folder['updated'], db_folder.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

    def test_folder_filter_title(self):
        """
        Tests that folders are filtered appropriately by their title.
        """
        # create folders
        Folder(title='ab', owner=self.user).save()
        folder_0 = Folder(title='bc', owner=self.user)
        folder_1 = Folder(title='cd', owner=self.user)
        folder_0.save()
        folder_1.save()
        # request
        response = self.client.get(reverse(self.view_name) + '?title=c')
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['folders']), 2)
        self.assertEqual(response_body['folders'][0]['pk'], folder_0.id)
        self.assertEqual(response_body['folders'][1]['pk'], folder_1.id)

    def test_folder_retrieve_owned(self):
        """
        Tests that only folders that are owned are retrieved.
        """
        # create folders
        folder = Folder(title='title', owner=self.user)
        folder.save()
        Folder(title='title', owner=User.objects.create_user(username='other_user')).save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['folders']), 1)
        self.assertEqual(response_body['folders'][0]['pk'], folder.id)

    def test_folder_retrieve_not_authenticated(self):
        """
        Tests that a folder is not created when the user is not authenticated.
        """
        # create unauthenticated client
        client = APIClient()
        # request
        response = client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('folders' in response_body)


class TestFolderRUDGet(APITestCase):
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
        self.view_name = 'marknote:folder-retrieve-update-destroy'

    def test_folder_retrieve(self):
        """
        Tests that the proper folder is retrieved.
        """
        # create folders
        folder = Folder(title='title1', owner=self.user)
        folder.save()
        Folder(title='title2', owner=self.user).save()
        # request
        response = self.client.get(reverse(self.view_name, args=[folder.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['pk'], folder.id)
        self.assertEqual(response_body['title'], folder.title)
        self.assertEqual(response_body['container'], None)
        self.assertEqual(response_body['created'], folder.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(response_body['updated'], folder.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

    def test_folder_does_not_exist(self):
        """
        Tests that no folder is retrieved if the id specified does not exist.
        """
        # create folder
        folder = Folder(title='title1', owner=self.user)
        folder.save()
        # request
        response = self.client.get(reverse(self.view_name, args=['2']))
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_folder_retrieve_not_owned(self):
        """
        Tests that folders that are not owned are not retrieved.
        """
        # create folders
        folder = Folder(title='title', owner=User.objects.create_user(username='other_user'))
        folder.save()
        # request
        response = self.client.get(reverse(self.view_name, args=[folder.id]))
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_folder_retrieve_not_authenticated(self):
        """
        Tests that a folder is not retrieved when the user is not authenticated.
        """
        # create unauthenticated client
        client = APIClient()
        # create folders
        folder = Folder(title='title', owner=self.user)
        folder.save()
        # request
        response = client.get(reverse(self.view_name, args=[folder.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('pk' in response_body)


class TestFolderRUDPutPatch(APITestCase):
    """
    Test cases for PUT requests on NoteRetrieveUpdateDestroyView.
    """
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # permissions
        self.user.user_permissions.add(Permission.objects.get(codename='change_folder'))
        # log in test client
        self.client.login(username=self.username, password=self.password)
        # view name
        self.view_name = 'marknote:folder-retrieve-update-destroy'

    def test_folder_update_full(self):
        """
        Tests that a full folder update executes properly.
        """
        # create folder and folder
        top_folder = Folder(title='title', owner=self.user)
        top_folder.save()
        bottom_folder = Folder(title='title', owner=self.user)
        bottom_folder.save()
        # request
        body = {
            'title': 'title changed',
            'container': top_folder.id,
        }
        response = self.client.put(reverse(self.view_name, args=[bottom_folder.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        folder = Folder.objects.get(id=bottom_folder.id)
        self.assertEqual(body['title'], folder.title)
        self.assertEqual(top_folder, folder.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['title'], body['title'])
        self.assertEqual(response_body['container'], top_folder.id)

    def test_folder_update_partial(self):
        """
        Tests that a partial folder update executes properly.
        """
        # create folder
        original_title = 'title'
        folder = Folder(title=original_title, owner=self.user)
        folder.save()
        # request
        body = {
            'title': 'title changed',
        }
        response = self.client.patch(reverse(self.view_name, args=[folder.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        folder = Folder.objects.first()
        self.assertEqual(body['title'], folder.title)
        self.assertEqual(None, folder.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['title'], body['title'])
        self.assertEqual(response_body['container'], None)

    def test_folder_update_container_does_not_exist(self):
        """
        Tests that a folder cannot be updated with a non-existent container.
        """
        # create folder and folder
        original_title = 'title'
        folder = Folder(title=original_title, owner=self.user)
        folder.save()
        # request
        body = {
            'container': '2',
        }
        response = self.client.patch(reverse(self.view_name, args=[folder.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        folder = Folder.objects.first()
        self.assertEqual(original_title, folder.title)
        self.assertEqual(None, folder.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse('pk' in response_body)

    def test_folder_update_read_only_fields(self):
        """
        Tests that read only fields cannot be updated.
        """
        # create folder
        original_folder = Folder(title='title', owner=self.user)
        original_folder.save()
        # request
        body = {
            'pk': '2',
            'created': '2018-09-04T16:30:28.469865Z',
            'updated': '2018-09-04T16:30:28.469865Z',
        }
        response = self.client.patch(reverse(self.view_name, args=[original_folder.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        folder = Folder.objects.first()
        self.assertEqual(original_folder, folder)
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response_body['pk'], body['pk'])
        self.assertNotEqual(response_body['created'], body['created'])
        self.assertNotEqual(response_body['updated'], body['updated'])

    def test_folder_update_not_owned(self):
        """
        Tests that folders that are folder owned are not updated.
        """
        # create folder
        original_title = 'title'
        folder = Folder(title=original_title, owner=User.objects.create_user(username='other_user'))
        folder.save()
        # request
        body = {
            'title': 'title changed',
        }
        response = self.client.patch(reverse(self.view_name, args=[folder.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        folder = Folder.objects.first()
        self.assertEqual(original_title, folder.title)
        self.assertEqual(None, folder.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('pk' in response_body)

    def test_folder_update_not_authenticated(self):
        """
        Tests that a folder is not retrieved when a user is not authenticated.
        """
        # create unauthenticated client
        client = APIClient()
        # create folder
        original_title = 'title'
        folder = Folder(title=original_title, owner=self.user)
        folder.save()
        # request
        body = {
            'title': 'title changed',
        }
        response = client.patch(reverse(self.view_name, args=[folder.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        folder = Folder.objects.first()
        self.assertEqual(original_title, folder.title)
        self.assertEqual(None, folder.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('pk' in response_body)

    def test_folder_update_not_authorized(self):
        """
        Tests that a folder is not retrieved when a user is not authorized.
        """
        # create unauthorized user
        username = 'unauthorized'
        password = 'unauthorized'
        User.objects.create_user(username=username, password=password)
        client = APIClient()
        client.login(username=username, password=password)
        # create folder
        original_title = 'title'
        folder = Folder(title=original_title, owner=self.user)
        folder.save()
        # request
        body = {
            'title': 'title changed',
        }
        response = client.patch(reverse(self.view_name, args=[folder.id]), body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        folder = Folder.objects.first()
        self.assertEqual(original_title, folder.title)
        self.assertEqual(None, folder.container)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('pk' in response_body)


class TestFolderRUDDelete(APITestCase):
    """
    Test cases for DELETE requests on NoteRetrieveUpdateDestroyView.
    """
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # permissions
        self.user.user_permissions.add(Permission.objects.get(codename='delete_folder'))
        # log in test client
        self.client.login(username=self.username, password=self.password)
        # view name
        self.view_name = 'marknote:folder-retrieve-update-destroy'

    def test_folder_destroy(self):
        """
        Tests that a folder is properly destroyed.
        """
        # create folder
        folder = Folder(title='title', owner=self.user)
        folder.save()
        # request
        response = self.client.delete(reverse(self.view_name, args=[folder.id]))
        # test database
        folders = Folder.objects.all()
        self.assertEqual(len(folders), 0)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_folder_does_not_exist(self):
        """
        Tests that destroying a non-existent folder does not affect other folders.
        """
        # create folder
        folder = Folder(title='title', owner=self.user)
        folder.save()
        # request
        response = self.client.delete(reverse(self.view_name, args=['2']))
        # test database
        folders = Folder.objects.all()
        self.assertEqual(len(folders), 1)
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_folder_destroy_not_owned(self):
        """
        Tests that folders that are not owned are not destroyed.
        """
        # create folder
        folder = Folder(title='title', owner=User.objects.create_user(username='other_user'))
        folder.save()
        # request
        response = self.client.delete(reverse(self.view_name, args=[folder.id]))
        # test database
        folders = Folder.objects.all()
        self.assertEqual(len(folders), 1)
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_folder_destroy_not_authenticated(self):
        """
        Tests that a folder is not destroyed when a user is not authenticated.
        """
        # create unauthenticated client
        client = APIClient()
        # create folder
        folder = Folder(title='title', owner=self.user)
        folder.save()
        # request
        response = client.delete(reverse(self.view_name, args=[folder.id]))
        # test database
        folders = Folder.objects.all()
        self.assertEqual(len(folders), 1)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_folder_destroy_not_authorized(self):
        """
        Tests that a folder is not destroyed when a user is not authorized.
        """
        # create unauthorized user
        username = 'unauthorized'
        password = 'unauthorized'
        User.objects.create_user(username=username, password=password)
        client = APIClient()
        client.login(username=username, password=password)
        # create folder
        folder = Folder(title='title', owner=self.user)
        folder.save()
        # request
        response = client.delete(reverse(self.view_name, args=[folder.id]))
        # test database
        folders = Folder.objects.all()
        self.assertEqual(len(folders), 1)
        # test response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
