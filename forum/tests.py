from django.test import Client, tag, LiveServerTestCase,TestCase
from forum.models import Topic, User

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from forum.models import Question


# Create your tests here.
class siteTestCase(TestCase):
    def setUp(self):
        self.topic_1 = Topic.objects.create(
            topic_name="smud test topic",
            topic_desc="veldig smud, veldig test.",
            id=1
        )

    def test_root_page_404(self):
        client = Client()
        response = client.get('/')  # expecting 404
        self.assertEquals(response.status_code, 404)

    def test_forum(self):
        client = Client()
        response = client.get('/forum/')  # expecting 200
        self.assertEquals(response.status_code, 200)

    def test_forum(self):
        client = Client()
        response = client.get('/forum/')  # expecting 200
        self.assertEquals(response.status_code, 200)

    def test_topics_appear_on_index_page(self):
        client = Client()
        response = client.get('/forum/')  # expecting 200
        self.assertEquals(response.status_code, 200) #
        self.assertTrue("topics_list" in response.context)
        self.assertTrue(len(response.context['topics_list'])==1) #Asserting on the length of the querySet, which contains the names of the topics.

    def test_topic_page(self):
        c=Client()
        resp=c.get('/forum/topics/1/') #expecting 200
        self.assertEquals(resp.status_code, 200)


class permissionTestCase(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='Pekka', email='pekka@ntnu.no', password='abraham', id=0)
        self.student = User.objects.create_user(
            username='GenericStudent', email='generic@stud.ntnu.no', password='qwerty', id=1
        )
        self.student2 = User.objects.create_user(
            username='GenericStudent2', email='generic2@stud.ntnu.no', password='qwerty', id=2
        )
        self.topic_1 = Topic.objects.create(
            topic_name="smud test topic",
            topic_desc="veldig smud, veldig test.",
            id=1
        )

    @tag('notworking')
    def test_need_to_be_logged_in_to_post_questions(self):
        c = Client()
        resp = c.get('/forum/topics/1/new_question')
        print('resp1= '+str(resp))
        c.force_login(self.student)
        resp = c.get('/forum/topics/1/new_question')
        print('resp2= '+str(resp))
        self.assertEquals(resp.status_code, 301)

    #@tag('notworking')
    #def teachers_can_delete_questions(self):

    @tag('notworking')
    def test_post_question(self):
        self.assertTrue(True)

    def test_my_question_list(self):
        c = Client()
        c.force_login(self.student)
        resp = c.get('/forum/my_question')
        self.assertTrue(len(resp.context['my_question_list']) == 0) #Before a question is created, the list should be empty
        q = Question.objects.create(question_name="balle", question_topic=self.topic_1, user_id=self.student.id)
        resp = c.get('/forum/my_question')
        self.assertTrue(len(resp.context['my_question_list']) == 1) #After a question is created the list should have exactly one element for the student.
        c.force_login(self.student2)
        resp = c.get('/forum/my_question')
        self.assertTrue(len(resp.context['my_question_list']) == 0) #For another user, the list should still be empty.


@tag('selenium')
class MySeleniumTests(LiveServerTestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='Pekka', email='pekka@ntnu.no', password='abraham', id=0)
        self.selenium = webdriver.Firefox()
        super(MySeleniumTests, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(MySeleniumTests, self).tearDown()

    def test_login(self):
        selenium = self.selenium
        #Opening the link we want to test
        selenium.get('http://127.0.0.1:8000/forum/login')
        #find the form element
        username = selenium.find_element_by_name('username')
        password = selenium.find_element_by_name('password')

        login = selenium.find_element_by_id('login_button')

        #Fill the form with data
        username.send_keys('Pekka')
        password.send_keys('abraham')
        #submitting the form
        login.click()
            #send_keys(Keys.RETURN)

        #check the returned result
        print(selenium.title)
        assert 'Topics' in selenium.title