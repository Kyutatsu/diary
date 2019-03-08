from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from diary.models import Article
from author.models import Author
from drawing.models import DrawingModel


# models

class ArticleModelTests(TestCase):
    """Articleモデルのテスト"""
    @classmethod
    def setUpTestData(cls):
        for x in range(1, 11):
            Article.objects.create(
                    a_title=f'title{x}',
                    text=f'text_text_text_text_text_text{x}',
                    picture = '/test/path/',
        )
        
    def test_article_str_method(self):
        for x in range(1,11):
            article = Article.objects.get(pk=x)
            self.assertEqual(str(article), f'title{x}')

    def test_article_picture(self):
        article = Article.objects.get(pk=1)
        self.assertEqual(article.picture, '/test/path/')

    def test_article_text20(self):
        article = Article.objects.get(pk=1)
        text='text_text_text_text_text_text'
        self.assertEqual(article.text20, text[:20] + '...')

# views

class IndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
                username='testuser',
                password='testpass',
        )
        user2 = User.objects.create_user(
                username='testuser2',
                password='testpass2',
        )
        author = Author.objects.create(
                name='testauthor',
                user=user,
        )
        author2 = Author.objects.create(
                name='testauthor2',
                user=user2,
        )
        
        # 10個article作っておく
        for i in range(10):
            article = Article.objects.create(
                    a_title=f'test{i}',
                    text=f'{i}abcdefghijklmlnopqrstuvwxyz',
                    author=author,
            )
        # 別user: 5つ
        for i in range(5):
            article2 = Article.objects.create(
                    a_title=f'test2{i}',
                    text=f'{i}2abcdefghijklmlnopqrstuvwxyz2',
                    author=author2,
            )
    
    def setUp(self):
        login = self.client.login(
                username='testuser',
                password='testpass',
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/diary/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('diary:index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('diary:index'))
        self.assertTemplateUsed(response, 'diary/index.html')

    def test_pagination(self):
        response = self.client.get(reverse('diary:index'))
        response_last = self.client.get(
                reverse('diary:index') + '?page=4'
        )
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue('diaries' in response.context)
        self.assertTrue(len(response.context['diaries']) == 3)
        self.assertTrue(len(response_last.context['diaries']) == 1)
        # 新しい順なので、9が先に来る。
        self.assertEqual(
                response.context['diaries'][0].a_title,
                'test9',
        )
        self.assertEqual(
                response_last.context['diaries'][0].a_title,
                'test0',
        )


class IndividualViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
                username='testuser',
                password='testpass',
        )
        user2 = User.objects.create_user(
                username='testuser2',
                password='testpass2',
        )
        author = Author.objects.create(
                name='testauthor',
                user=user,
        )
        author2 = Author.objects.create(
                name='testauthor2',
                user=user2,
        )

        article = Article.objects.create(
                a_title='test',
                text='abcdefghijklmlnopqrstuvwxyz',
                author=author,
        )
        article2 = Article.objects.create(
                a_title='test2',
                text='abcdefghijklmlnopqrstuvwxyz2',
                author=author2,
        )
    
    def setUp(self):
        login = self.client.login(
                username='testuser',
                password='testpass',
        )
        self.art = Article.objects.get(a_title='test')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/diary/{self.art.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
                reverse('diary:individual', args=[self.art.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(
                reverse('diary:individual', args=[self.art.pk])
        )
        self.assertTemplateUsed(response, 'diary/individual.html')

    def test_view_uses_correct_context(self):
        response = self.client.get(
                reverse('diary:individual', args=[self.art.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['article'], self.art)


class MakeDiaryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
                username='testuser',
                password='testpass',
        )
        author = Author.objects.create(
                name='testauthor',
                user=user,
        )
        article = Article.objects.create(
                a_title='test',
                text='abcdefghijklmlnopqrstuvwxyz',
        )

    def setUp(self):
        login = self.client.login(
                username='testuser',
                password='testpass',
        )

    def test_view_url_exists_at_desired_location(self):
        # GET
        response_g = self.client.get('/diary/make_diary/')
        self.assertEqual(response_g.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        # POSTはindexへredirectする
        response_p = self.client.post(
                '/diary/make_diary/',
                data={
                    'a_title': 'post_test',
                    'text': 'texttexttext',
                }
        )
        self.assertEqual(response_p.status_code, 302)
        self.assertEqual(response_p.url, '/diary/')

    def test_post_correct_author(self):
        response = self.client.post(
                '/diary/make_diary/',
                data={
                    'a_title': 'post',
                    'text': 'text',
                }
        )
        art = Article.objects.get(a_title='post')
        self.assertEqual(art.author.name, 'testauthor')


    def test_view_url_accessible_by_name(self):
        response = self.client.get(
                reverse('diary:make_diary')
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(
                reverse('diary:make_diary')
        )
        self.assertTemplateUsed(response, 'diary/make_diary.html')


class DeleteDiaryTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
                username='testuser',
                password='testpass',
        )
        for i in range(1,4):
            Article.objects.create(
                    a_title=f'test{i}',
                    text=f'text_content{i}',
            )
    def test_before_delete(self):
        articles = Article.objects.all()
        self.assertTrue(len(articles) == 3)

    def test_after_delete(self):
        login = self.client.login(
                username='testuser',
                password='testpass',
        )
        response = self.client.get(
                reverse('diary:delete_diary', args=[2])
        )
        articles = Article.objects.all()
        self.assertTrue(response.status_code, 302)
        self.assertEqual(response.url, '/diary/')
        self.assertTrue(len(articles) == 2)
        self.assertTrue(articles[0].a_title == 'test1')
        self.assertTrue(articles[1].a_title == 'test3')
        
