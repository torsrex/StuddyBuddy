from django.contrib.auth.models import Permission
from django.test import Client, TestCase

from forum.models import Question, Answer
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
            username='Pekka', email='pekka@ntnu.no', password='abraham', )
        permission = Permission.objects.get(codename='delete_question')
        self.teacher.user_permissions.add(permission)
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
        c.post('/forum/up_vote/',
               {'pk_question': self.question_1.id, 'topic': self.question_1.question_topic.id, 'user': self.student})
        assert self.question_1.votes.count() == 1
        c.post('/forum/down_vote/', {'pk_question': self.question_1.id, 'topic': self.question_1.question_topic.id})
        assert self.question_1.votes.count() == 0

    def test_upvote_and_downvote_answer(self):
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
        for a in Answer.objects.all():
            if a.answer_text == 'have':
                answerpk = a.id
        c.post('/forum/up_vote_answer/',
               {'pk_answer': answerpk, 'topic': self.question_1.question_topic.id, 'user': self.student, 'pk_question': self.question_1.id})
        assert Answer.objects.get(pk=answerpk).votes.count() == 1
        c.post('/forum/down_vote_answer/',
               {'pk_answer': answerpk, 'topic': self.question_1.question_topic.id, 'user': self.student, 'pk_question': self.question_1.id})
        assert Answer.objects.get(pk=answerpk).votes.count() == 0

    """
    def test_delete_question(self):
        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )
        questions = Question.objects.all()
        assert len(questions) == 1
        print('\nquestions:',questions)
        c = Client()
        c.force_login(self.student)
        resp=c.post('/forum/'+str(self.question_1.id))
        print('\nresp:',resp)
        questions = Question.objects.all()
        print('\nurl:','/forum/'+str(self.question_1.id)+'/')
        assert len(questions) == 0
    """

    def test_add_answer(self):
        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )
        c = Client()
        c.force_login(self.student)

        answers = Answer.objects.all()
        resp = c.post('/forum/new_answer/', {'answer_text': 'have', 'question': self.question_1.id,
                                             'topic': self.question_1.question_topic.id, 'user': self.student})
        answers = Answer.objects.all()
        answerFound = False
        for a in answers:
            if a.answer_text == 'have':
                answerFound = True
        assert answerFound

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

    def test_teachers_can_delete_all_questions(self):
        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )
        c = Client()
        c.force_login(self.teacher)
        resp = c.post('/forum/delete_question_in_index/',
                      {'pk_question': self.question_1.id, 'topic': self.question_1.question_topic.id})
        questions = Question.objects.all()
        assert len(questions) == 0

    def test_search(self):
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
        resp=c.post('/forum/search/?q=transistors')

        transistorFound=False
        jacobianFound=False
        for q in resp.context['result']:
            if q['question_name'] == 'jacobian':
                jacobianFound=True
            if q['question_name']=='transistor':
                transistorFound=True

        assert not jacobianFound
        assert transistorFound

    def test_mark_as_solved(self):
        self.question_1 = Question.objects.create(
            question_name="testquest",
            question_text="testdesc",
            question_topic=self.topic_1,
            user=self.student2,
        )
        c = Client()
        c.force_login(self.student)

        q = Question.objects.get(pk=self.question_1.id)
        assert not q.question_solved
        resp = c.post('/forum/mark_as_solved/',
                      {'pk_question': self.question_1.id, 'topic': self.question_1.question_topic.id})
        q=Question.objects.get(pk=self.question_1.id)
        assert q.question_solved
        resp = c.post('/forum/mark_as_solved/',
                      {'pk_question': self.question_1.id, 'topic': self.question_1.question_topic.id})
        q = Question.objects.get(pk=self.question_1.id)
        assert not q.question_solved




