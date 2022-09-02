from django.shortcuts import render
from django.views import View
from .models import User, Tweet, Hashtag, Search
from django.shortcuts import render
from .forms import NewTweetForm, SearchForm
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

# Create your views here.
class UserView(View):
    def get (self, request, **kwargs):
        username = kwargs.get('username', '')
        try:
            u = User.objects.get(username=username)
        except:
            return HttpResponseRedirect("/")
        
        user_tweets = Tweet.objects.filter(user_ref=u)
        tags = Hashtag.objects.all()
        context = {
            "user_tweets": user_tweets,
            "new_tweet_form": NewTweetForm(),
            "hashtags": tags,
            "is_self": u == request.user
        }
        return render(request, "homepage/user.html", context)

    @method_decorator(login_required)
    def post (self, request, **kwargs):
        if request.user.username == kwargs.get("username", ""):
            form = NewTweetForm(request.POST)
            try:
                tweet = form.save(False)
                tweet.user_ref = request.user
                tweet.save()
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

            except ValidationError as e:
                print(e)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class IndexView(View):
    def get (self, request, **kwargs):
        return render(request, "homepage/index.html")

class LikePostView(View):
    @method_decorator(login_required)
    def post (self, request, **kwargs):
        try:
            tweet_id = kwargs.get("post_id")
            tweet = Tweet.objects.get(id=tweet_id)
            print(tweet)
            tweet.toggle_like(by=request.user)
            print(tweet.liked_by.all())
            response = JsonResponse({'likes': tweet.likes()})
            return response

        except Exception as e:
            # TODO: proper error handling
            print(e, "RESPONSE")
            return HttpResponse(400)


class SearchView(View):
    @method_decorator(login_required)
    def get (self, request, **kwargs):
        q = request.get("q")
        
        resulting_tweets = Tweet.objects.all()
        resulting_people = User.objects.all()

        if q:
            resulting_tweets = resulting_people.filter(username__icontains=q)
            resulting_tweets = resulting_tweets.filter(content__icontains=q)
        
        context = {
            "tweet": resulting_tweets,
            "people": resulting_people,
        }

        return 

class SearchHistoryView(View):
    @method_decorator(login_required)
    def get (self, request, **kwargs):
        search_id = kwargs
        
        get('search_id')
        if search_id:
            search = get_object_or_404(Search, id=search_id, user_ref=request.user)
            return JsonResponse(search)
        else:
            return JsonResponse(Search.objects.filter(user_ref=request.user))

    @method_decorator(login_required)
    def post (self, request, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.user_ref = request.user
            form.save()
        else:
            # TODO: ACTUAL ERROR HANDLING
            return HttpResponse(status_code=400)