from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
# csrf_exempt is a decorator in python which changes the functionality of a function
from .paytm import checksum
MERCHANT_KEY = 'kbzk1DAbJiV_03p5'


def index(request):
    # products = Product.objects.all()
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    allcat = []
    catprod = Product.objects.values("category", "id")
    cats = {i["category"] for i in catprod}
    for j in cats:
        prod = Product.objects.filter(category=j)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allcat.append([nSlides, range(1, nSlides), prod])
    # allcat = [[nSlides, range(1, nSlides) ,products], [
    #     nSlides, range(1, nSlides), products]]
    params = {'allcat': allcat}
    return render(request, 'shop/index.html', params)


def searchMatch(query, item):
    if query in item.product_name.lower() or query in item.description.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get("search")
    allcat = []
    catprod = Product.objects.values("category", "id")
    cats = {i["category"] for i in catprod}
    for j in cats:
        prodtemp = Product.objects.filter(category=j)
        prod = [item for item in prodtemp if searchMatch(query, item)]


        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        if len(prod) != 0:
            allcat.append([nSlides, range(1, nSlides), prod])
    # allcat = [[nSlides, range(1, nSlides) ,products], [
    #     nSlides, range(1, nSlides), products]]
    params = {'allcat': allcat}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, "shop/about.html")


def contactus(request):
    thank = False
    if request.method == "POST":
        # print(request)
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phoneno = request.POST.get("phoneno", "")
        desc = request.POST.get("desc", "")
        contact = Contact(name=name, email=email, phoneno=phoneno, desc=desc)
        contact.save()
        thank = True
        # first variable is of db and other is of model
    return render(request, "shop/contactus.html", {"thank": thank})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get("orderId", "")
        email = request.POST.get("email", "")
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if (len(order) > 0):
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append(
                        {"text": item.update_desc, "time": item.timestamp})
                    response = json.dumps(
                        [updates, order[0].item_json], default=str)
                return HttpResponse(response)

            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, "shop/tracker.html")


def products(request, pid):
    product = Product.objects.filter(id=pid)
    # print(product) single product stored in product
    # jo bhi product ki value hogi vo "product" m jaegi jise index lega
    return render(request, "shop/products.html", {"product": product[0]})


def checkout(request):
    if request.method == "POST":
        # print(request)
        item_json = request.POST.get("itemsJson", "")
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        address = request.POST.get("address1", "") + \
            " " + request.POST.get("address2", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zip_code = request.POST.get("zip_code", "")
        phone = request.POST.get("phone", "")
        amount = request.POST.get('amount', '')
        order = Order(item_json=item_json, name=name, email=email, phonenumber=phone,
                      address=address, city=city, state=state, zip_code=zip_code, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        # here the amount will be sent to paytm and it will accept the amount as amount shown in checkout page

        param_dict = {
            'MID': 'Your-Merchant-Id-Here',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/HandleRequest/',
        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, "shop/checkout.html")


@csrf_exempt
def HandleRequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' +
                  response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
