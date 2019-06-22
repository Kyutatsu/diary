from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic

from .forms import UserForm, AuthorForm
from .models import Author
from drawing.models import DrawingModel
from diarySite.settings import BASE_DIR


class AuthorProfile(generic.View):
    template_name_for_read = 'author/author_profile.html'
    template_name_for_change = 'author/author_profile_change.html'

    def get(self, request):
        author = get_object_or_404(Author, user=request.user)
        return render(
                request,
                self.template_name_for_read,
                {'author': author, 'email': request.user.email},
        )
    @permission_required('author.change_author')
    def post(self, request):
        check = request.POST.get('second', None)
        author = get_object_or_404(Author, user=request.user)
        drawings = DrawingModel.objects.filter(author=author)
        drawings = drawings.order_by('-created_date')
        drawings_url_list = []
        for drawing in drawings:
            drawings_url_list.append(drawing.drawing.url)
        num_four = list(range(1, len(drawings_url_list) // 4 + 2))
        if check:
            # 最初はdbの値を入力した状態で表示,更新押すとhiddenが入って分岐する
            form = AuthorForm(request.POST, instance=author)
            if form.is_valid():
                profile = form.save()
                # jsでonclickした画像からprofileをhidden属性経由で取得
                profile.icon = request.POST.get('select_img', None)
                profile.save()
                return redirect(reverse('author:profile'))
        else:
            form = AuthorForm(instance=author)

        return render(
                request,
                self.template_name_for_change,
                {
                    'form': form,
                    'drawings_url_list': drawings_url_list,
                    'now_picture': author.icon,
                    'num_four': num_four,

                }
        )


def user_form_registration(request):
    '''サインアップ(ユーザの新規登録)'''
    group = Group.objects.get(name='DiaryMembers')
    message = None
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_r = form.cleaned_data['password_r']
            if password == password_r:
                user.set_password(password)
                user.save()
                user.groups.add(group)

                author = Author.objects.create(
                        name=username,
                        user=user,
                )
                # 登録したら即ログインさせる
                user_auth = authenticate(
                            username=username,
                            password=password
                )
                if user_auth is not None:
                    login(request, user_auth)
                    return redirect('author:profile')
            else:
                message = 'パスワードが一致していません'
        # invalidな場合
        return render(
                request,
                'author/registration_form.html', 
                {'form': form, 'pass_message': message}
        )
    else:  # GET
        form = UserForm()
        return render(
                request,
                'author/registration_form.html', 
                {'form': form},
        )
