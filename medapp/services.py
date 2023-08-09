from django.http import HttpResponse, Http404
from .models import Article, Topic, UserModel
from django.db.models import Count

def get_sorted_articles(user_id):
    try:
        user = UserModel.objects.get(id=user_id)
        
        annotated_articles = Article.objects.annotate(prefer_topics=Count('topics', topics__users=user))
        sorted_articles = annotated_articles.order_by('-created_at', '-prefer_topics')

        return sorted_articles

    except UserModel.DoesNotExist:
        raise Http404('User does not exist')