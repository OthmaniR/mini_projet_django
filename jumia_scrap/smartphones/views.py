import time
from urllib.parse import urljoin
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import requests
from django.urls import reverse


def special_template(request):
    time.sleep(40)  # Render the special template for 40 seconds
    return redirect(reverse('next_page'))  # Redirect to the next page


def next_page(request):
    return render(request, 'Search_Phone.html')  # Redirect to the next page


def Search_Phone(request):

    Phone_Brands = []
    smartphones = []
    page = []

    for i in range(0, 1):
        url = f"https://www.jumia.com.tn/mlp-telephone-tablette/smartphones/?page={i}#catalog-listing"
        response = requests.get(url)
        response = response.content
        soup = BeautifulSoup(response, 'html.parser')


        div = soup.find('div', class_='-paxs row _no-g _4cl-3cm-shs')

        articles = div.find_all('article', class_='prd _fb col c-prd')

        if request.method == 'POST':
            brand = request.POST.get('brand')
            price = request.POST.get('price')

        for article in articles:
            title = article.find('div', class_='info')
            phone_name = title.find('h3', class_='name').text.strip()
            phone_brand = phone_name.split()[0]
            prix = title.find('div', class_='prc').text
            phone_price = float(prix.replace(',', '').replace('.', '').replace('TND', '')) / 100
            image = article.find('div', class_='img-c')
            phone_img = image.find('img', class_='img')['data-src']
            phone_link = article.find('a', class_='core').get('href')
            link = urljoin('https://www.jumia.com.tn/', phone_link)

            if phone_brand not in Phone_Brands:
               Phone_Brands.append(phone_brand)

            if request.method == 'POST':
                if brand == '' or phone_brand.lower() == brand.lower():
                   if price == '' or float(phone_price) <= float(price):
                       smartphones.append({'brand': phone_brand, 'name': phone_name, 'price': phone_price, 'img': phone_img, 'phone_link': link})
            else :
               smartphones.append({'brand': phone_brand, 'name': phone_name, 'price': phone_price, 'img': phone_img, 'phone_link': link})

    if request.method == 'POST':
        context = {'Phone_Brands': Phone_Brands, 'SmaPhones': smartphones, 'selected_brand': brand,
                   'selected_price': price}
    else:
        context = {'Phone_Brands': Phone_Brands, 'SmaPhones': smartphones}

    return render(request, 'Search_Phone.html', context)




