from django.http import HttpRequest, HttpResponse
from django.urls import path, include, re_path
from medapp.models import Article, Comment, Topic, UserModel, UserTopicRelationship
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from medapp.services import sorted_articles_view



def about_view(request):
    return HttpResponse("This is a medical blog that will contain up-to-date information about new discoveries in medicine, effective medicines and treatment methods")

def home_view(request):
    return HttpResponse("Here will be blog structure ")

def article_detail_view(request, article):
    article = get_object_or_404(Article, title=article)
    comments = article.comment_set.all()
    article_data = f"Title: {article.title}\nContent: {article.content}\n\nComments:\n"
    for comment in comments:
        article_data += f"- {comment.message}\n"
    return HttpResponse(article_data, content_type='text/plain')

def article_comment(request: HttpRequest, article: str) -> HttpResponse:
    return HttpResponse(f"Comment to article - {article}")

def create_form_article(request):
    return HttpResponse(f"Block_1,Block_2")

def update_article(request: HttpRequest, article: str) -> HttpResponse:
    return HttpResponse(f"Update to article - {article}")

def delete_article(request: HttpRequest, article: str) -> HttpResponse:
    return HttpResponse(f"Delete to article - {article}")

def topics_view(request):
    return HttpResponse("My topics")

def topic_subscribe(request: HttpRequest, topic: str) -> HttpResponse:
    return HttpResponse(f"Subscribe topic - {topic}")

def topic_unsubscribe(request: HttpRequest, topic: str) -> HttpResponse:
    return HttpResponse(f"Unsubscribe topic - {topic}")

def set_password(request) :
    return HttpResponse("Enter password")

def set_userdata(request):
    return HttpResponse("Enter userdata")

def deactivate_profile(request):
    return HttpResponse("Deactivate profile")

def register_profile(request):
    return HttpResponse("Register your profile")

def login_profile(request):
    return HttpResponse("Login in")

def logout_profile(request):
    return HttpResponse("Logout")

def regex(request):
    return HttpResponse("its regex")

def article_list(request):
    articles = Article.objects.all()
    article_data = ""
    for article in articles:
        article_data += f"Title: {article.title}\nContent: {article.content}\n\nComments:\n"
        comments = Comment.objects.filter(article=article)
    for comment in comments:
            article_data += f"- {comment.message}\n"

    article_data += "\n"

    return HttpResponse(article_data, content_type='text/plain')

def user_profile(request, username):
    try:
        cur_user = UserModel.objects.get(username=username)
        user_data = f"Username: {cur_user.username}\nEmail: {cur_user.email}\n\nArticles:\n"
        articles = Article.objects.filter(author=cur_user)
        user_data += '\n'.join(f"- {article.title}" for article in articles)
        return HttpResponse(user_data, content_type='text/plain')
    except UserModel.DoesNotExist:
        raise Http404('There is no such user.')

