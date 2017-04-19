from django.contrib.auth.models import Permission
from django.test import Client, TestCase

from forum.models import Question, Answer
from forum.models import Topic, User


class SiteTestCase(TestCase):
    def setUp(self):
        self.topic_1 = Topic.objects.create(  # Creating a topic in the test database
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
                                'topics_list']) == 1)
        """Asserting on the length of the querySet, which contains the names of the topics. 
        We know there should appear only one topic, as the database is empty in the beginning"""

    def test_topic_page(self):
        c = Client()
        resp = c.get('/forum/topics/1/')  # expecting 200, as a topic with id=1 is created.
        self.assertEquals(resp.status_code, 200)


class PermissionTestCase(TestCase):
    def setUp(self):  # Makes users and a topic, so it doesn't have to be done in every test.
        self.teacher = User.objects.create_user(
            username='Pekka', email='pekka@ntnu.no', password='abraham', )
        permission = Permission.objects.get(codename='delete_question')
        self.teacher.user_permissions.add(
            permission)  # Permissions must be added manually, as we bypass the form when creating users this way
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

    def test_post_question(self):  # Are we able to post questions and have them appear in the database?
        c = Client()
        c.force_login(self.student)
        c.post('/forum/topics/1/new_question/',
               {'question_name': "test", 'question_text': "yoyoyo", 'question_topic': self.topic_1.id})
        """Post makes a POST-request to the link in the first argument, 
        sending in the dictionary in the second argument in the request."""
        questions = Question.objects.all()  # Fetches all the Question objects in the database
        question_found = False
        for q in questions:
            if q.__str__() == "test":  # Does the question exist in the database?
                question_found = True
        assert question_found

    def test_teachers_add_topic(self):  # Are we able to create topics and have them appear in the database?
        c = Client()
        c.force_login(self.teacher)
        c.post('/forum/new_topic/', {'topic_name': 'ekstremt smud topic', 'topic_desc': 'uhyre smud desc'})
        topics = Topic.objects.all()  # Fetches all the Topic objects in the database
        topic_found = False
        for t in topics:
            if t.topic_name == "ekstremt smud topic":
                topic_found = True
        assert topic_found

    def test_create_user(self):  # Are we able to create users and have them appear in the database?
        c = Client()
        c.post('/forum/register/',
               {'username': 'testteacher', 'password': 'smud passord', 'email': 'smud@ntnu.no'})
        c.post('/forum/register/',
               {'username': 'teststudent', 'password': 'smud passord', 'email': 'smud@stud.ntnu.no'})
        users = User.objects.all()  # Fetches all the User objects in the database
        user_found = False
        for u in users:
            if u.username == "testteacher":
                user_found = True
        assert user_found

    def test_upvote_and_downvote(self):  # Are we able to register and store upvotes and downvotes in the database?
        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )
        c = Client()
        c.force_login(self.student)
        c.post('/forum/up_vote/',
               {'pk_question': self.question_1.id, 'topic': self.question_1.question_topic.id, 'user': self.student})
        assert self.question_1.votes.count() == 1  # After the upvote, number of votes on question_1 should be 1.
        c.post('/forum/down_vote/', {'pk_question': self.question_1.id, 'topic': self.question_1.question_topic.id})
        assert self.question_1.votes.count() == 0  # After downvote, number of votes on question_1 should be 0 again.

    def test_upvote_and_downvote_answer(self):  # Does upvoting and downvoting answers work?
        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )

        c = Client()
        c.force_login(self.student)
        c.post('/forum/new_answer/',
               {'answer_text': 'have', 'question': self.question_1.id, 'pk_question': self.question_1.id,
                'topic': self.question_1.question_topic.id, 'user': self.student})
        answerpk = -1
        for a in Answer.objects.all():  # Iterates through all the answers in the database
            if a.answer_text == 'have':
                answerpk = a.id  # Finds the pk of the answer we just created by a post-request.
        c.post('/forum/up_vote_answer/',
               {'pk_answer': answerpk, 'topic': self.question_1.question_topic.id, 'user': self.student,
                'pk_question': self.question_1.id})
        assert Answer.objects.get(pk=answerpk).votes.count() == 1
        c.post('/forum/down_vote_answer/',
               {'pk_answer': answerpk, 'topic': self.question_1.question_topic.id, 'user': self.student,
                'pk_question': self.question_1.id})
        assert Answer.objects.get(pk=answerpk).votes.count() == 0

    def test_add_answer(self):  # Are we able to create answers to questions and have them appear in the database?
        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )
        c = Client()
        c.force_login(self.student)

        c.post('/forum/new_answer/', {'answer_text': 'have', 'question': self.question_1.id,
                                      'topic': self.question_1.question_topic.id, 'user': self.student})
        answers = Answer.objects.all()
        answer_found = False
        for a in answers:
            if a.__str__() == 'have':
                answer_found = True
        assert answer_found

    def test_my_question_list(self):
        c = Client()
        c.force_login(self.student)
        resp = c.get('/forum/my_question')
        self.assertTrue(
            len(resp.context['my_question_list']) == 0)  # Before a question is created, the list should be empty
        Question.objects.create(question_name="test", question_topic=self.topic_1, user_id=self.student.id)
        resp = c.get('/forum/my_question')

        # After a question creation the list should have exactly one element for the student.
        self.assertTrue(len(resp.context[
                                'my_question_list']) == 1)
        c.force_login(self.student2)
        resp = c.get('/forum/my_question')
        self.assertTrue(len(resp.context['my_question_list']) == 0)  # For another user, the list should still be empty.

    def test_teachers_can_delete_all_questions(
            self):  # Teachers should be able to delete questions they didn't make themselves.
        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )
        c = Client()
        c.force_login(self.teacher)
        c.post('/forum/delete_question_in_index/',
               {'pk_question': self.question_1.id, 'topic': self.question_1.question_topic.id})
        questions = Question.objects.all()
        assert len(questions) == 0  # If the deletion was successful, we should have no questions left.

    def test_search(
            self):  # Are we able to search for questions and only get questions similar to what we ask for in return?
        self.question_1 = Question.objects.create(
            question_name="transistor",
            question_text="transistors mayne, how do they work?",
            question_topic=self.topic_1,
            user=self.student2,
        )
        self.question_2 = Question.objects.create(
            question_name="jacobian",
            question_text="jacobians mayne, how do they work?",
            question_topic=self.topic_1,
            user=self.student2,
        )

        c = Client()
        c.force_login(self.student)
        # Makes a search for "transistors" and searches through the question_texts of all questions for a similar word.
        resp = c.post('/forum/search/?q=transistors')
        transistor_found = False
        jacobian_found = False
        for q in resp.context['result']:  # Iterates through the questions in the list returned by the search function.
            if q['question_name'] == 'jacobian':  # The jacobian question should not be returned
                jacobian_found = True
            if q['question_name'] == 'transistor':  # The transistor question should not be returned
                transistor_found = True

        assert not jacobian_found
        assert transistor_found

    def test_mark_as_solved(self):  # Are we able to mark questions as solved, and then mark them as unsolved again?
        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )
        c = Client()
        c.force_login(self.student)

        q = Question.objects.get(pk=self.question_1.id)
        assert not q.question_solved  # The question should initially not be solved.
        # After this, the question should be marked as solved.
        c.post('/forum/mark_as_solved/',
               {'pk_question': self.question_1.id,
                'topic': self.question_1.question_topic.id})
        q = Question.objects.get(pk=self.question_1.id)
        assert q.question_solved
        # After this, the question should be marked as unsolved.
        c.post('/forum/mark_as_solved/',
               {'pk_question': self.question_1.id,
                'topic': self.question_1.question_topic.id})
        q = Question.objects.get(pk=self.question_1.id)
        assert not q.question_solved
