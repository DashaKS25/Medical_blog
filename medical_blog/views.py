from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView, View, FormView, DetailView
from medapp.forms import ArticleForm, UserLoginForm, UserRegistrationForm
from medapp.models import Article, Comment, Topic, UserModel
from medapp.services import get_sorted_articles


class AboutView(TemplateView):
    template_name = 'about.html'


class HomeView(ListView):
    model = Article
    template_name = 'home.html'
    context_object_name = 'all_articles'


def article_detail_view(request, article_id):
    try:
        cur_article = get_object_or_404(Article, id=article_id)
        comments = Comment.objects.filter(article=cur_article)

        article_data = f'TITLE: {cur_article.title}\n\nCONTENT: {cur_article.content}\n\nCOMMENTS:\n'
        for comment in comments:
            article_data += f'- {comment.message}\n'

        return HttpResponse(article_data, content_type='text/plain')

    except Article.DoesNotExist:
        raise Http404('There is no such article.')


def article_comment(request, article_id):
    try:
        article = get_object_or_404(Article, id=article_id)  # Get the article by its id
        return HttpResponse(f"Comment to article - {article.title}")
    except Article.DoesNotExist:
        raise Http404('There is no such article.')


class CreateArticleView(View):
    template_name = 'create_article.html'

    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        topics = Topic.objects.all()
        topics_to_ctx = []
        for index, topic in enumerate(topics):
            cur_topic = {'option_value': index + 1, 'topic': topic}
            topics_to_ctx.append(cur_topic)
        ctx = {
            'form': form,
            'topics_list': topics_to_ctx,
            'topics': Topic.objects.all(),
        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            if request.user.is_authenticated:
                article.author = request.user
                article.save()
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("You need to be logged in to create an article.")
        topics = Topic.objects.all()
        topics_to_ctx = []
        for index, topic in enumerate(topics):
            cur_topic = {'option_value': index + 1, 'topic': topic}
            topics_to_ctx.append(cur_topic)
        ctx = {
            'form': form,
            'topics_list': topics_to_ctx,
            'topics': Topic.objects.all(),
        }
        return render(request, self.template_name, ctx)


class UpdateArticleView(View):
    template_name = 'article_update.html'

    def get(self, request, article_id, *args, **kwargs):
        article = get_object_or_404(Article, pk=article_id)
        return render(request, self.template_name, {'article': article})

    def post(self, request, article_id, *args, **kwargs):
        article = get_object_or_404(Article, pk=article_id)
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
        return redirect('article_list')


def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')

    return render(request, 'article_delete.html', {'article': article})


class TopicsListView(View):
    template_name = 'topics_list.html'

    def get(self, request, *args, **kwargs):
        topics = Topic.objects.all()
        return render(request, self.template_name, {'topics': topics})


class TopicsView(View):
    template_name = 'topics.html'

    def get(self, request, topic_title, *args, **kwargs):
        try:
            topic = Topic.objects.get(title=topic_title)
            articles = Article.objects.filter(topics__title=topic_title)
            ctx = {
                'topic': topic,
                'articles': articles
            }
            return render(request, self.template_name, ctx)
        except Topic.DoesNotExist:
            raise Http404('Topic with this title does not exist.')


def topic_subscribe(request, topic_title):
    try:
        topic = Topic.objects.get(title=topic_title)
        return render(request, 'subscribe.html', {'topic': topic})
    except Topic.DoesNotExist:
        raise Http404("Topic does not exist")


def topic_unsubscribe(request, topic_title):
    try:

        topic = Topic.objects.get(title=topic_title)
        return render(request, 'unsubscribe.html', {'topic': topic})
    except Topic.DoesNotExist:
        raise Http404("Topic does not exist")


class SetPasswordView(LoginRequiredMixin, View):
    template_name = 'set_password.html'

    def post(self, request):
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password successfully changed")
            return redirect(reverse('user_profiles_list'))
        else:
            messages.error(request, 'Passwords don\'t match. Try again')
            return render(request, self.template_name)

    def get(self, request):
        return render(request, self.template_name)


def set_userdata(request):
    return HttpResponse("Enter userdata")


class DeactivateProfileView(View):
    template_name = 'deactivate_profile.html'

    @login_required
    def post(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()

        logout(request)
        messages.success(request, "Your profile has been deactivated. You have been logged out.")
        return redirect('home')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RegisterProfileView(FormView):
    template_name = 'register.html'
    form_class = UserRegistrationForm

    def form_valid(self, form):
        username = form.cleaned_data['username']

        if get_user_model().objects.filter(username=username).exists():
            error_message = "This name is already used."
            return render(self.request, self.template_name, {'form': form, 'error_message': error_message})

        form.create_user()
        return HttpResponseRedirect(reverse('login'))


class LoginProfileView(View):
    template_name = 'login.html'

    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('user_profile', pk=user.pk, username=user.username)

        return render(request, self.template_name, {'form': form})


class LogoutProfileView(LogoutView):
    template_name = 'logout.html'


def regex(request):
    return HttpResponse("its regex")


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    queryset = Article.objects.all().prefetch_related('comment_set')


class UserProfileView(DetailView):
    model = UserModel
    template_name = 'user_profile.html'
    context_object_name = 'user'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.filter(author=self.object)
        context['articles'] = articles
        return context


class UserProfilesListView(ListView):
    model = UserModel
    template_name = 'user_profiles_list.html'
    context_object_name = 'users'


def preferred_articles(request, user_id):
    sorted_articles_list = get_sorted_articles(user_id)

    article_data = "Preferred Articles:\n\n"
    for article in sorted_articles_list:
        article_data += f"Title: {article.title}\nContent: {article.content}\nCommon Topics: {article.prefer_topics}\n"

    return HttpResponse(article_data, content_type='text/plain')


def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        message = request.POST.get('message')
        user = request.user

        if user.is_authenticated:
            Comment.objects.create(article=article, author=user, message=message)
            return redirect('article_list')
        else:
            message = request.POST.get('message')
        if message:

            message = "You need to log in or register to add a comment."
        else:

            message = "Please enter a comment before submitting."

    return render(request, 'article_list.html', {'article': article, 'message': message})
