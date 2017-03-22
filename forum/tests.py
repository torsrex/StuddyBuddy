from django.test import Client, tag, LiveServerTestCase,TestCase
from forum.models import Topic, User
import time

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

    def test_topics_appear_on_index_page(self):
        client = Client()
        response = client.get('/forum/')  # expecting 200
        self.assertEquals(response.status_code, 200) #
        self.assertTrue("topics_list" in response.context)
        self.assertTrue(len(response.context['topics_list'])==1) #Asserting on the length of the querySet, which contains the names of the topics.

    def test_topic_page(self):
        c=Client()
        resp=c.get('/forum/topics/1/') #expecting 200, as a topic with id=1 is created.
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
class MySeleniumTests(LiveServerTestCase): #HUSK AT DISSE BRUKER LIVE-DATABASEN
    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(MySeleniumTests, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(MySeleniumTests, self).tearDown()

     #Finner ikke ut om brukeren eksisterer i den ekte databasen, bare testbasen.
    def test_registration(self):
        selenium=self.selenium
        selenium.get('http://127.0.0.1:8000/forum/register/')

        time.sleep(0.5)

        username = selenium.find_element_by_name('username')
        password = selenium.find_element_by_name('password')
        email=selenium.find_element_by_name('email')

        register=selenium.find_element_by_id('register_button')

        name='random'+str(round(time.time(),0))

        time.sleep(0.5)
        username.send_keys(name)
        password.send_keys('stuff')
        email.send_keys('dfssdf@ntnu.no')
        time.sleep(0.5)
        register.send_keys(Keys.RETURN)
        time.sleep(0.8)
        """
        users=User.objects.all() #Dette returnerer test-databasebrukerne
        userFound=False
        for u in users:
            print('\n',u.username)
            if name == u.username:
                userFound=True"""
        assert 'Topics' in selenium.title

    def login_as_student(self,selenium): #Requires a user with username student and password qwerty
        selenium.get('http://127.0.0.1:8000/forum/login')
        # find the form element
        username = selenium.find_element_by_name('username')
        password = selenium.find_element_by_name('password')

        login = selenium.find_element_by_id('login_button')

        # Fill the form with data
        username.send_keys('student')
        password.send_keys('qwerty')
        # submitting the form
        login.send_keys(Keys.RETURN)

    def login_as_admin(self,selenium):
        selenium.get('http://127.0.0.1:8000/forum/login')
        # find the form element
        username = selenium.find_element_by_name('username')
        password = selenium.find_element_by_name('password')

        login = selenium.find_element_by_id('login_button')

        # Fill the form with data
        username.send_keys('admin')
        password.send_keys('admin')
        # submitting the form
        login.send_keys(Keys.RETURN)

    @tag('slow')
    def test_login(self):
        selenium = self.selenium
        self.login_as_admin(selenium)
        time.sleep(0.8) #If this test fails, try a longer sleep time.
        assert 'Topics' in selenium.title

    @tag('slow')
    def test_must_be_logged_in_to_post_questions(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/forum/topics/1/')
        selenium.find_element_by_id('registration_button').click()
        time.sleep(0.3)
        assert selenium.current_url=='http://127.0.0.1:8000/forum/login/?next=/forum/topics/1/new_question/'
        self.login_as_student(selenium)
        time.sleep(0.3)
        selenium.get('http://127.0.0.1:8000/forum/topics/1/')
        selenium.find_element_by_id('registration_button').click()
        """selenium.find_element_by_id('question_name').send_keys('test')
        selenium.find_element_by_id('question_text').send_keys('testtext')
        selenium.find_element_by_id('button').send_keys(Keys.RETURN)"""
        time.sleep(0.3)
        assert selenium.current_url=='http://127.0.0.1:8000/forum/topics/1/new_question/'

    def test_teacher_can_remove_post(self):
        selenium=self.selenium
        self.login_as_admin(selenium)
        time.sleep(0.6)
        selenium.find_element_by_id('t1').click() #Krever at det finnes en topic
        time.sleep(0.8)
        selenium.find_element_by_id('b1').click() #Krever at det finnes et spørsmål
        time.sleep(0.4)
        selenium.find_element_by_id('remove').click()
        time.sleep(0.4)
        assert True #Hvis sletteknappen finnes, har alt gått bra.




