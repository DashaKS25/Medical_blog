from django.http import HttpRequest, HttpResponse


def about_view(request):
    return HttpResponse("This is a medical blog that will contain up-to-date information about new discoveries in medicine, effective medicines and treatment methods")

def home_view(request):
    return HttpResponse("Here will be blog structure ")

def article_detail_view(request: HttpRequest, article: str) -> HttpResponse:
    return HttpResponse(f" Default article - {article}")

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

def profile_username(request: HttpRequest, username: str) -> HttpResponse:
    return HttpResponse(f"Enter username - {username}")

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

