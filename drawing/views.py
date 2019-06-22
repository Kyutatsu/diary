import codecs
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.files.base import ContentFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponseRedirect

from author.models import Author
from drawing.models import DrawingModel
from drawing.forms import DrawingModelForm


class IndexView(LoginRequiredMixin, generic.ListView):
    '''userの投稿した絵一覧を表示する'''
    template_name = 'drawing/index.html'
    context_object_name = 'drawings'
    paginate_by = 3
    model = DrawingModel

    def get_queryset(self):
        author = get_object_or_404(Author, user=self.request.user)
        drawing = DrawingModel.objects.filter(author=author)
        drawing = drawing.order_by('-created_date')
        return drawing


class IndividualView(LoginRequiredMixin, generic.DetailView):
    '''個々の絵の詳細を表示する'''
    model = DrawingModel


@permission_required('drawing.delete_drawingmodel')
def delete(request, pk):
    '''絵を削除する'''
    drawing = get_object_or_404(DrawingModel, pk=pk)
    drawing.delete()
    return redirect('drawing:index')


class DrawingView(PermissionRequiredMixin, generic.View):
    '''絵を描く, アップロードする'''
    permission_required = 'drawing.add_drawingmodel'
    template_name = 'drawing/drawing.html'

    def get(self, request):
        form = DrawingModelForm()
        return render(
                request,
                self.template_name,
                {'form': form}
        )

    def post(self, request):
        form = DrawingModelForm(request.POST, request.FILES)
        if form.is_valid():
            drawing = form.save()
            author = get_object_or_404(Author, user=request.user)
            author.drawingmodel_set.add(drawing)
            # 変換後,base64のdataが不要となるので冗長。修正予定.
            drawing_by_text = form.cleaned_data['drawing_base64']
            drawing_base64_part = drawing_by_text.split(',')[1].encode()
            while len(drawing_base64_part) % 4 != 0:
                drawing_base64_part = drawing_base64_part + b'='
            drawing_decoded = codecs.decode(drawing_base64_part, 'base64')
            file_obj = ContentFile(drawing_decoded)
            # https://docs.djangoproject.com/en/2.1/ref/models/fields/#filefield-and-fieldfile
            # drawing.drawing.save(form.cleaned_data['title'], file_obj, save=True)
            drawing.drawing.save(str(drawing.id), file_obj, save=True)
        return redirect('drawing:index')
