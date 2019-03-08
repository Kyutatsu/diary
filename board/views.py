from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils import timezone

from .models import Board, Topic, Post
from .forms import PostForm
from drawing.models import DrawingModel
from author.models import Author


class BoardListView(LoginRequiredMixin, generic.ListView):
    """Board一覧"""
    template_name = 'board/board_list.html'
    context_object_name = 'boards'
    paginate_by = 3
    model = Board
    ordering = 'name'


class TopicListView(LoginRequiredMixin, generic.View):
    """Topic一覧"""
    template_name = 'board/topic_list.html'

    def get(self, request, pk):
        board = Board.objects.get(pk=pk)
        topics = Topic.objects.filter(board=board)
        topics = topics.order_by('-updated_date')
        paginator = Paginator(topics, 3)
        page = request.GET.get('page')  # 初回は未定義なので1
        page_obj = paginator.get_page(page)
        return render(
                request,
                self.template_name,
                {
                    'board': board,
                    'page_obj': page_obj
                }
        )


class TopicIndividualView(LoginRequiredMixin, generic.DetailView):
    model = Topic

    def get_context_data(self, **kwargs):
        """Topicに属するPostのリストをテンプレで使える様にする

        postの並び(昇順/降順)はsessionに値があれば使う。
        GETでorderを更新した場合、sessionのorderも上書きする。
        """
        context = super().get_context_data(**kwargs)
        saved = self.request.session.get('order', None)
        order = self.request.GET.get('order', saved)
        self.request.session['order'] = order  # sessionに保存しておく。
        if order == 'ascending':
            posts = self.object.post_set.all().order_by('created_date')
        else:
            posts = self.object.post_set.all().order_by('-created_date')

        paginator = Paginator(posts, 50)
        page = self.request.GET.get('page')  # 初回は未定義なので1
        posts = paginator.get_page(page)

        context['posts'] = posts
        context['posts_num'] = len(posts)
        context['order'] = order
        return context


# https://docs.djangoproject.com/en/2.1/topics/class-based-views/generic-editing/
class TopicCreate(LoginRequiredMixin, generic.edit.CreateView):
    """Topicを新規作成するview.

    Boardの表示viewからリンクでここに飛ぶ
    """
    model = Topic
    fields = ['name']

    def form_valid(self, form):
        author = get_object_or_404(Author, user=self.request.user)
        board = get_object_or_404(Board, id=self.kwargs['pk']) # これok?
        now = timezone.now()
        form.instance.updated_date = now
        form.instance.author = author
        form.instance.board = board
        return super().form_valid(form)


@login_required
def make_post(request, pk):
    """topicに対して投稿するためのview.
    
    画像選択周りなど複雑なので、テンプレviewではなくfunction
    viewで実装.
    """
    template_name = 'board/make_post.html'
    topic = get_object_or_404(Topic, id=pk)
    author = get_object_or_404(Author, user=request.user)
    drawings = DrawingModel.objects.filter(author=author).order_by('-created_date')
    drawing_url_list = []
    for drawing in drawings:
        drawing_url_list.append(drawing.drawing.url)
    num_four = list(range(1, len(drawing_url_list) // 4 + 2))
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # topicの更新時間を変更
            topic.updated_date = timezone.now()
            topic.save()
            post = form.save()
            author.post_set.add(post)
            topic.post_set.add(post)
            post.picture = request.POST.get('select_img', None)
            post.save()
            return HttpResponseRedirect(reverse('board:topic', args=[pk]))
    else:
        form = PostForm()
    return render(
            request,
            template_name,
            {
                'form': form,
                'drawing_url_list': drawing_url_list,
                'num_four': num_four,
                'pk': pk,
            }
    )
