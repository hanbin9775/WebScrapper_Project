import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

#scrapping 해올 url
BASE_CRAIGSLIST_URL = 'https://comic.naver.com/webtoon/weekdayList.nhn?week={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

#home view. 메인 페이지를 렌더한다.
def home(request):
    return render(request, 'base.html')

def MakeFullDay(day):
    if(day=="mon"):
        return 'monday'
    if(day=="tue"):
        return 'tuesday'
    if(day=="wed"):
        return 'wendesday'
    if(day=="thu"):
        return 'thursday'
    if(day=="fri"):
        return 'friday'
    if(day=="sat"):
        return 'saturday'
    if(day=="sun"):
        return 'sunday'    
        

#서치해서 출력한다.
def new_search(request):
    #search에 form으로 입력한 문자가 들어간다.
    search = request.POST.get('search')
    #모델에 search이란 이름으로 객체 추가
    models.Search.objects.create(search=search)
    #BASE_URL의 {} 부분에 search 삽입
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))

    search = MakeFullDay(search)

    response = requests.get(final_url)
    data = response.text
    #크롤링할 데이터를 soup에 전달
    soup = BeautifulSoup(data, features='html.parser')

    #li 태그의 class = result-row를 다 가져온다.
    post_listings = soup.findAll('div',{'class':'thumb'})
    #프리미엄 배너 (3개) 제외하기
    post_listings = post_listings[3:]
    #print(post_listings)
    final_postings = []


    #크롤링 데이터들 변환
    for post in post_listings:
        post_title = post.find('a').get('title')
        print(post_title)
        post_url = "http://comic.naver.com"
        post_url += post.find('a').get('href')
        print(post_url)
        """
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        """
        if post.find('img').get('src'):
            post_image_url = post.find('img').get('src')
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_image_url))
        
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)