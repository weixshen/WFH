from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib import auth
from bs4 import BeautifulSoup
import urllib.request
import datetime
import string

from .forms import UserForm
from .models import Learner, Word, Article


def register(request):
    # 标记是否注册成功
    registered = False
    if request.user.is_authenticated():
        return HttpResponseRedirect("/wfh/")
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            password = user_form.cleaned_data['password']
            confirm = user_form.cleaned_data['confirm_password']
            if password == confirm:
                # 新建User
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                # 新建Learner，并关联User
                learner = Learner()
                learner.user = user
                learner.save()
                registered = True
                return render(request, 'wfh/login.html',
                              {"message": "注册成功，请登录！"})
            else:
                user_form.add_error("confirm_password", "两次输入的密码不匹配")
    else:
        user_form = UserForm()
    return render(request, "wfh/register.html",
                  {'user_form': user_form, 'registered': registered})


def login(request):
    errors = []
    if request.user.is_authenticated():
        return HttpResponseRedirect("/wfh/")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/wfh/")
        else:
            errors.append("账号/密码错误！")
    return render(request, 'wfh/login.html', {"errors": errors})


def logout(request):
    auth.logout(request)
    return render(request, 'wfh/login.html', {"message": "已成功退出!"})


@login_required(login_url='/wfh/login/')
def index(request):
    if not Article.objects.all():
        all_in_one()
    else:
        latest = Article.objects.order_by('-pub_date')[0]
        delta = datetime.datetime.now() - latest.pub_date.replace(tzinfo=None)
        if delta > datetime.timedelta(hours=6):
            all_in_one()
    articles = get_article_list(request)
    return render(request, 'wfh/index.html',
                  {'articles': articles})


@login_required(login_url='/wfh/login/')
def words(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    url = article.url
    title = article.title
    content = article.content
    words = get_headline_words(content)
    known_words = (known.word for known in request.user.learner.words.all())
    unknown_words = (word for word in words if word not in known_words)
    return render(request, 'wfh/words.html',
                  {'aid': article_id, 'url': url,
                   'title': title, 'words': unknown_words})


@login_required(login_url='/wfh/login')
def known(request):
    word = request.POST.get('word')
    word = Word.objects.get(word=word)
    request.user.learner.words.add(word)
    request.user.learner.save()
    return HttpResponseRedirect("")


@login_required(login_url='/wfh/login')
def readed(request):
    aid = request.GET.get('id')
    article = Article.objects.get(pk=aid)
    request.user.learner.articles.add(article)
    request.user.learner.save()
    return HttpResponseRedirect("/wfh/")


def get_article_list(request):
    return Article.objects.exclude(learner__id=request.user.learner.id)


def get_headline_url():
    page = urllib.request.urlopen("http://www.globaltimes.cn/business/insight/")
    soup = BeautifulSoup(page, "html.parser")
    # head = soup.find_all('div', attrs={'class': 'zn__column--idx-0'})[0]
    # link = head.find('a').get('href')
    # head = soup.find_all('time')[2]
    # link = head.find_next('a').get('href')
    head = soup.find_all('div', attrs={'id': 'channel-more'})[0]
    link = head.find('a').get('href')
    return link


def get_headline_content(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    title = soup.title.string
    content = soup.find("div", class_="row-content").get_text()
    return title, content


def get_headline_words(content):
    words = set()
    for s in string.punctuation:
        content = content.replace(s, ' ')
    for w in content.split():
        w = w.lower()
        if len(w) <= 2:
            continue
        if not w.isalpha():
            continue
        words.add(w)
    return words


def all_in_one():
    url = get_headline_url()
    latest_article = Article.objects.filter(url=url)
    if not latest_article:
        title, content = get_headline_content(url)
        article = Article(url=url, title=title, content=content)
        article.save()

        words = get_headline_words(content)
        for w in words:
            word = Word.objects.filter(word=w)
            if not word:
                word = Word(word=w)
                word.save()

if __name__ == '__main__':
    print(get_headline_content(get_headline_url()))
