from django.shortcuts import render
from .biasclassifier.classifier import predictor
from .biasclassifier.pull import get_all_tweets
from django.http import JsonResponse
# Create your views here.
def home(request):
    return render(request, 'predict/home.html')


def check(request, uname):
	print('getting')
	status, tweets = get_all_tweets(uname)
	print(status)
	if not status:
		return JsonResponse({'status' : status, 'bias' : None})

	p = predictor(dir_path = 'predict/biasclassifier/')
	bias = p.classify(tweets)
	return JsonResponse({'status' : status, 'bias' : bias})
