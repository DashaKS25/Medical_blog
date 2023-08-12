from django.http import HttpRequest
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from medapp.forms import ArticleForm
from medapp.models import Article, Comment, Topic, UserModel
from medapp.services import get_sorted_articles


def about_view(request):
    return render(request, 'about.html')


def home_view(request):
    all_articles = Article.objects.all()  # Отримати всі статті з бази даних
    context = {'all_articles': all_articles}
    return render(request, 'home.html', context)


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


def create_article(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return HttpResponseRedirect(reverse('home'))
    else:
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
    return render(request, 'create_article.html', ctx)


def update_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
        return redirect('article_list')

    return render(request, 'article_update.html', {'article': article})


def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')

    return render(request, 'article_delete.html', {'article': article})


def topics_list_view(request):
    topics = Topic.objects.all()

    return render(request, 'topics_list.html', {'topics': topics})


def topics_view(request: HttpRequest, topic_title: str):
    try:
        ctx = {
            'topic': Topic.objects.get(title=topic_title),
            'articles': Article.objects.filter(topics__title=topic_title)
        }
        return render(request, 'topics.html', ctx)
    except Topic.DoesNotExist:
        raise Http404('Topic with this title does not exist.')


def topic_subscribe(request, topic_title):
    topic = Topic.objects.get(title=topic_title)
    return render(request, 'subscribe.html', {'topic': topic})


def topic_unsubscribe(request, topic_title):
    topic = Topic.objects.get(title=topic_title)
    return render(request, 'unsubscribe.html', {'topic': topic})


def set_password(request):
    return HttpResponse("Enter password")


def set_userdata(request):
    return HttpResponse("Enter userdata")


def deactivate_profile(request):
    return HttpResponse("Deactivate profile")


def register_profile(request):
    return render(request, 'register.html')


def login_profile(request):
    return render(request, 'login.html')


def logout_profile(request):
    return HttpResponse("Logout")


def regex(request):
    return HttpResponse("its regex")


def article_list(request):
    try:
        articles = Article.objects.all()
        for article in articles:
            article.comments = Comment.objects.filter(article=article)
        return render(request, 'article_list.html', {'articles': articles})
    except Article.DoesNotExist:
        raise Http404('There is no such article.')


def user_profile(request, username):
    user = get_object_or_404(UserModel, username=username)
    articles = Article.objects.filter(author=user)
    return render(request, 'user_profile.html', {'user': user, 'articles': articles})


def user_profiles_list(request):
    users = UserModel.objects.all()
    return render(request, 'user_profiles_list.html', {'users': users})


def preferred_articles(request, user_id):
    sorted_articles_list = get_sorted_articles(user_id)

    article_data = "Preferred Articles:\n\n"
    for article in sorted_articles_list:
        article_data += f"Title: {article.title}\nContent: {article.content}\nCommon Topics: {article.prefer_topics}\n"

    return HttpResponse(article_data, content_type='text/plain')
