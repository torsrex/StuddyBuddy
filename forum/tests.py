from django.test import Client, TestCase

from forum.models import Question
from forum.models import Topic, User


# Create your tests here.
class siteTestCase(TestCase):
    def setUp(self):
        self.topic_1 = Topic.objects.create(
            topic_name="smud test topic",
            topic_desc="veldig smud, veldig test.",
            id=1
        )

    def test_forum(self):
        client = Client()
        response = client.get('/forum/')  # expecting 200
        self.assertEquals(response.status_code, 200)

    def test_topics_appear_on_index_page(self):
        client = Client()
        response = client.get('/forum/')  # expecting 200
        self.assertEquals(response.status_code, 200)  #
        self.assertTrue("topics_list" in response.context)
        self.assertTrue(len(response.context[
                                'topics_list']) == 1)  # Asserting on the length of the querySet, which contains the names of the topics.

    def test_topic_page(self):
        c = Client()
        resp = c.get('/forum/topics/1/')  # expecting 200, as a topic with id=1 is created.
        self.assertEquals(resp.status_code, 200)


class permissionTestCase(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='Pekka', email='pekka@ntnu.no', password='abraham')
        self.student = User.objects.create_user(
            username='GenericStudent', email='generic@stud.ntnu.no', password='qwerty'
        )
        self.student2 = User.objects.create_user(
            username='GenericStudent2', email='generic2@stud.ntnu.no', password='qwerty'
        )
        self.topic_1 = Topic.objects.create(
            topic_name="smud test topic",
            topic_desc="veldig smud, veldig test.",
        )

    def test_post_question(self):
        c = Client()
        c.force_login(self.student)
        resp = c.post('/forum/topics/1/new_question/',
                      {'question_name': "balle", 'question_text': "yoyoyo", 'question_topic': self.topic_1.id})
        questions = Question.objects.all()
        questionFound = False
        for q in questions:
            if q.question_name == "balle":  # Does the question exist in the database?
                questionFound = True
        assert questionFound

    def test_teachers_add_topic(self):
        c = Client()
        c.force_login(self.teacher)
        resp = c.post('/forum/new_topic/', {'topic_name': 'ekstremt smud topic', 'topic_desc': 'uhyre smud desc'})
        topics = Topic.objects.all()
        topicFound = False
        for t in topics:
            if t.topic_name == "ekstremt smud topic":
                topicFound = True
        assert topicFound

    def test_create_user(self):
        c = Client()
        resp = c.post('/forum/register/',
                      {'username': 'testbruker', 'password': 'smud passord', 'email': 'smud@ntnu.no'})
        users = User.objects.all()
        userFound = False
        for u in users:
            if u.username == "testbruker":
                userFound = True
        assert userFound

    def test_upvote_and_downvote(self):

        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )
        c = Client()
        c.force_login(self.student)
        c.post('/forum/upvote/',
               {'pk_question': self.question_1.id, 'topic': self.question_1.question_topic, 'user': self.student})
        assert self.question_1.votes.count() == 1
        c.post('/forum/downvote/', {'pk_question': self.question_1.id, 'topic': self.question_1.question_topic})
        assert self.question_1.votes.count() == 0

    """
    @tag('notworking') #Det virker ikke som det funker å bruke post-request.
    def test_add_answer(self):

        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )
        c=Client()
        c.force_login(self.student)
        resp = c.post('/forum/new_answer/', {'answer_text':'have', 'question':self.question_1, 'topic': self.question_1.question_topic, 'user':self.student})
        answers=Answer.objects.all()
        print('svar: ',answers)
        answerFound=False
        for a in answers:
            if a.answer.text=='have':
                answerFound=True
        assert answerFound
        """

    def test_my_question_list(self):
        c = Client()
        c.force_login(self.student)
        resp = c.get('/forum/my_question')
        self.assertTrue(
            len(resp.context['my_question_list']) == 0)  # Before a question is created, the list should be empty
        q = Question.objects.create(question_name="balle", question_topic=self.topic_1, user_id=self.student.id)
        resp = c.get('/forum/my_question')
        self.assertTrue(len(resp.context[
                                'my_question_list']) == 1)  # After a question is created the list should have exactly one element for the student.
        c.force_login(self.student2)
        resp = c.get('/forum/my_question')
        self.assertTrue(len(resp.context['my_question_list']) == 0)  # For another user, the list should still be empty.


"""
    def test_teachers_can_delete_all_questions(self):
        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )
        c=Client()
        c.force_login(self.teacher)
        questions = Question.objects.all()
        print(questions)
        resp=c.post('/forum/delete_question_in_index/', {'pk_question':self.question_1.id,'topic':self.question_1.question_topic})
        questions=Question.objects.all()
        print(questions)
        assert len(questions)==0
"""

"""
@tag('selenium')
class MySeleniumTests(LiveServerTestCase): #HUSK AT DISSE BRUKER LIVE-DATABASEN, Tester krever: bruker Student, bruker admin, minst ett spørsmål i databasen (som slettes).
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
        time.sleep(0.3)
        assert selenium.current_url=='http://127.0.0.1:8000/forum/topics/1/new_question/'

    @tag('slow')
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
"""
