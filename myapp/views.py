import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

BASE_FLIPKART_URL = 'https://www.flipkart.com/search?q={}'
BASE_AMAZON_URL = 'https://www.amazon.in/s?k={}'
def home(request):
	return render(request, 'base.html')

def new_search(request):
	search = request.POST.get('search')
	models.Search.objects.create(search=search)
	final_url = BASE_FLIPKART_URL.format(quote_plus(search))
	final_urltwo = BASE_AMAZON_URL.format(quote_plus(search))
	response = requests.get(final_url)
	responsetwo = requests.get(final_urltwo, headers=headers)
	data = response.text
	datatwo = responsetwo.text
	soup = BeautifulSoup(data, features='html.parser')
	souptwo =BeautifulSoup(datatwo, features='html.parser')

	post_listings = soup.find_all('',{'class': '_3O0U0u'})

	if souptwo.find_all('',{'class':'a-section a-spacing-medium a-text-center'}):
		post_listingstwo = souptwo.find_all('',{'class':'a-section a-spacing-medium a-text-center'})
	else:
		post_listingstwo = souptwo.find_all('',{'class':'a-section a-spacing-medium'})

	final_postings = []

	for post in post_listings:
		if post.find(class_='_2LFGJH'):
			post_title = post.find(class_='_2LFGJH').text
		elif post.find(class_='_2cLu-l'):
			post_title = post.find(class_='_2cLu-l').text
		else:
			post_title = post.find(class_='_3wU53n').text

		post_url = post.find('a').get('href')
		post_price = post.find(class_='_1vC4OE').text

		if post.find(class_='_1Nyybr'):
			post_image = post.find(class_='_1Nyybr').get('src')
		else:
			post_image = post.find(class_='_3togXc').get('src')
			print(post_image)

		final_postings.append((post_title, post_url, post_price, post_image))



	final_postingstwo = []

	for post in post_listingstwo:
		if post.find(class_='a-size-medium a-color-base a-text-normal'):
			post_title = post.find(class_='a-size-medium a-color-base a-text-normal').text
		else:
			post_title = post.find(class_='a-size-base-plus a-color-base a-text-normal').text

		if post.find('a'):
			post_url = post.find('a').get('href')
		else:
			post_url = 'Link not avaliable'

		if post.find(class_='a-offscreen'):
			post_price = post.find(class_='a-offscreen').text
		else:
			post_price = 'N/A'

		if post.find(class_='s-image'):
			post_image = post.find(class_='s-image').get('src')

		final_postingstwo.append((post_title, post_url, post_price, post_image))

	stuff_for_frontend = {
	'search': search,
	'final_postings': final_postings,
	'final_postingstwo': final_postingstwo
	}
	return render(request, 'myapp/new_search.html', stuff_for_frontend)