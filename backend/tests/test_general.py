from asyncio import tasks
from urllib import response
from requests import request
from backend.tests import base
from backend.database import Project, Task
from backend import schema
class TestProject(base.BaseTestCase):
    def test_create_project(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user=user)
        response = self.post('/project/', data={'name': "Test Project"})
        data = response.json

        self.assertTrue(data['success'])
        self.assertIsInstance(data['result'], dict)
        self.assertEqual(data['result']['name'], "Test Project")
        self.assertEqual(data['result']['manager'], schema.UserSchema().dump(user))
        self.logout()
    

    def test_edit_project(self, *args, **kwargs):
        test_user = base.create_random_user()
        self.login(user = test_user)

        response = self.post("/project/<int:project_id>/edit/")
        status_code = response.status_code
        data = response.json

        self.assertEqual(201, status_code) #edited status code for post
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Project edited successfully")
        self.assertIsInstance(data['result'], dict)
        self.assertEqual(data['result']['projects_you_contribute_to'], schema.projects_schema.dump(test_user.projects))

        self.logout()


    def test_get_projects_list(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user = user)

        response = self.get('/project/')
        status_code = response.status_code
        data = response.json

        self.assertEqual(200, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Succesfully fetched projects.")
        self.assertIsInstance(data['result'], dict)
        self.assertEqual(data['result']['projects_you_contribute_to'], schema.projects_schema.dump(user.projects))

        self.logout()


    def test_get_project_details(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user = user)

        response = self.get('/project/<int:project_id>/')
        status_code = response.status_code
        data = response.json

        self.assertEqual(200, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Found")
        
        self.logout()


    def test_search_for_keyword_in_project(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user = user)

        response = self.get('/project/')
        status_code = response.status_code
        data = response.json

        self.assertEqual(200, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Search results")

        self.logout()

    def test_remove_contributors_from_project(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user=user)

        response = self.post("/project/<int:project_id>/remove-contributor/")
        status_code = response.status_code
        data = response.json

        self.assertEqual(201, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Successfully updated project")

        self.logout()


    def test_add_contributors_to_project(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user=user)

        response = self.post("/project/<int:project_id>/add-contributor/")
        status_code = response.status_code
        data = response.json

        self.assertEqual(201, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['result']['contributor_ids'], "23")
        self.assertEqual(data['message'], "Successfully updated project")

        self.logout()


    def test_get_contributors_for_task(self, *args, **kwargs):
        test_user = base.create_random_user()
        self.login(user=test_user)

        response = self.get('/project/<int:project_id>/task/<int:task_id>/contributors/')
        status_code = response.status_code
        data = response.json

        self.assertEqual(201, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Project found")

        self.logout()


    def test_get_invitations(self, *args, **kwargs):
        test_user = base.create_random_user()
        self.login(user=test_user)

        response = self.get('/invitation/')
        status_code = response.status_code
        data = response.json

        self.assertEqual(201, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Successfully retrieved invitations")

        self.logout()
    
   
    def test_decline_invitation(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user=user)

        response = self.get('/invitation/<int:invitation_id>/decline/')
        status_code = response.status_code
        data = response.json

        self.assertEqual(201, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Invitation deleted successfully.")

        self.logout()


    def test_accept_invitation(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user=user)

        response = self.get('/invitation/<int:invitation_id>/accept/')
        status_code = response.status_code
        data = response.json

        self.assertEqual(201, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Successully accepted Invitation")

        self.logout()


    #def test_is_product_manager(self, *args, **kwargs):
    

    def test_delete_project(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user=user)

        response = self.delete('/project/<int:project_id>/delete/')
        status_code = response.status_code
        data = response.json

        self.assertEqual(204, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Project Deleted Successfully.")

        self.logout()

    def test_update_project_status(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user=user)

        response = self.put('/project/<int:project_id>/completion-status/', data={'name': "Test Project"})
        status_code = response.status_code
        data = response.json

        self.assertEqual(201, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], f"Successfully Updated the Completion Status of project{project_id}.")

        self.logout()


    def test_update_project_deadline(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user=user)

        response = self.put('/project/<int:project_id>/<deadline_date>', data={'name': "Test Project"})
        status_code = response.status_code
        data = response.json

        self.assertEqual(201, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], f"Successfully Changed the Deadline of project{project_id}.")

        self.logout()


class TestTask(base.BaseTestCase):

    def test_create_task(self, *args, **kwargs):
        test_user = base.create_random_user()
        self.login(user = test_user)

        response = self.post("/project/<int:project_id>/task/", data={'name': "Sample Task"})
        status_code = response.status_code
        data = response.json

        self.assertEqual(201, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Task Successfully Created.")        
        self.logout()

    def test_get_tasks(self, *args, **kwargs):
        test_user = base.create_random_user()
        self.login(user = test_user)

        response = self.get('/task/')
        status_code = response.status_code
        data = response.json

        self.assertEqual(200, status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['result'], schema.tasks_schema.dump(tasks))
        self.assertEqual(data['message'], "Tasks fetched.")

        self.logout() 

    def test_get_tasks_list(self, *args, **kwargs):
        test_user = base.create_random_user()
        self.login(user = test_user)

        response = self.get('/project/<int:project_id>/task/')
        status_code = response.status_code
        data = response.json

        self.assertEqual(200, status_code)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['result'], dict)
        self.assertEqual(data['result']['created_tasks'], schema.tasks_schema.dump(Task.query.filter_by(created_by_id = test_user.id).all()))
        self.assertEqual(data['message'], "Successfully fetched all tasks.")
        self.logout()

    # later write logic for the following
    # def test_update_task(self, *args, **kwargs): 
    # def test_delete_task(self, *args, **kwargs):
    # def test_update_task_status(self, *args, **kwargs):
    # def test_update_task_deadline(self, *args, **kwargs):
    # def test_get_task_details(self, *args, **kwargs):
    # def test_create_message(self, *args, **kwargs):
