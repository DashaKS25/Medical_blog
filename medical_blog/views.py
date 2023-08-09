from django.http import HttpRequest, HttpResponse
from django.urls import path, include, re_path
from medapp.models import Article, Comment, Topic, UserModel, UserTopicRelationship
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from medapp.services import get_sorted_articles
from django.shortcuts import render



def about_view(request):
    return HttpResponse("This is a medical blog that will contain up-to-date information about new discoveries in medicine, effective medicines and treatment methods")

def home_view(request):
    return HttpResponse("Here will be blog structure ")

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

def article_comment(request, article):
    try:
        Article.objects.get(title=article)  # Check if the article exists
        return HttpResponse(f"Comment to article - {article}")
    except Article.DoesNotExist:
        raise Http404('There is no such article.')

def create_form_article(request):
    return HttpResponse(f"Block_1,Block_2")

def update_article(request, article):
    try:
        Article.objects.get(title=article)  # Check if the article exists
        return HttpResponse(f"Update to article - {article}")
    except Article.DoesNotExist:
        raise Http404('There is no such article.')

def delete_article(request, article):
    try:
        Article.objects.get(title=article)  # Check if the article exists
        return HttpResponse(f"Delete to article - {article}")
    except Article.DoesNotExist:
        raise Http404('There is no such article.')

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
    try:
        articles = Article.objects.all()
        article_data = ""
        for article in articles:
            article_data += f"Title: {article.title}\nContent: {article.content}\n\nComments:\n"
            comments = Comment.objects.filter(article=article)
            for comment in comments:
                article_data += f"- {comment.message}\n"

            article_data += "\n"

        return HttpResponse(article_data, content_type='text/plain')
        
    except Article.DoesNotExist:
        raise Http404('There is no such article.')


def user_profile(request, username):
    try:
        cur_user = UserModel.objects.get(username=username)
        user_data = f"Username: {cur_user.username}\nEmail: {cur_user.email}\n\nArticles:\n"
        articles = Article.objects.filter(author=cur_user)
        user_data += '\n'.join(f"- {article.title}" for article in articles)
        return HttpResponse(user_data, content_type='text/plain')
    except UserModel.DoesNotExist:
        raise Http404('There is no such user.')

def preferred_articles(request, user_id):
    try:
        user = UserModel.objects.get(id=user_id)
        sorted_articles_list = get_sorted_articles(user_id)

        article_data = "Preferred Articles:\n\n"
        for article in sorted_articles_list:
            article_data += f"Title: {article.title}\nContent: {article.content}\nCommon Topics: {article.prefer_topics}\n\n"

        return HttpResponse(article_data, content_type='text/plain')

    except UserModel.DoesNotExist:
        raise Http404('User does not exist')