from django.http import HttpResponseNotAllowed
from django.http.response import Http404, HttpResponseForbidden
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.utils import dateparse
from django.views.decorators.csrf import csrf_exempt
from math import ceil
from paytmchecksum import PaytmChecksum
from paytmpg import LibraryConstants,MerchantProperty,UserInfo,Money,EChannelId,EnumCurrency,PaymentDetailsBuilder,Payment
from random import random
from .models import PaymentDetail, Pricing, TransctionDetail,UserModel
from .utils import InternalServerError
from blog.secret import site_name
import logging

mid = "WorldP64425807474247" # "YOUR_MID_HERE"
key = "kbzk1DSbJiV_O3p5" # "YOUR_KEY_HERE"
website = "WEBSTAGING" # "YOUR_WEBSITE_NAME"
client_id = "YOUR_CLIENT_ID_HERE" # 1


def start() : 
    # For Staging 
    environment = LibraryConstants.STAGING_ENVIRONMENT
    # For Production 
    # environment = LibraryConstants.PRODUCTION_ENVIRONMENT

    # Find your mid, key, website in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    # To be edited during production
    callbackUrl = "http://"+ site_name +"/payment/" # "MERCANT_CALLBACK_URL" 
    MerchantProperty.set_callback_url(callbackUrl)

    MerchantProperty.initialize(environment, mid, key, client_id, website)
    # If you want to add log file to your project, use below code
    file_path = './file.log'
    mode = "w"
    handler = logging.FileHandler(file_path, mode)
    formatter = logging.Formatter("%(name)s: %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    MerchantProperty.set_log_handler(handler)
    MerchantProperty.set_logging_disable(False)
    MerchantProperty.set_logging_level(logging.DEBUG)

start()

def startPayment(req: HttpRequest) :
    """ User payment credentials """
    if req.method == 'POST' and req.user.is_authenticated :
        try:  
            user: User = User.objects.get(username=req.user.username)
            userModel : UserModel = UserModel.objects.get(user=user)
            phone = req.POST.get('uPhone','9012345678')
            price = req.POST.get('price', 10)
            address = req.POST.get('address1','') + ' ' + req.POST.get('address2','')
            district = req.POST.get('district', '')
            state = req.POST.get('state', '')
            pin_code = req.POST.get('pin_code', '123456')
            if not price == 0 and not phone == '' and not pin_code == '':
                id = ceil(random()*1000000000000000)
                channel_id = EChannelId.WEB
                order_id = str(id)
                txn_amount = Money(EnumCurrency.INR, str(price)+".00")
                user_info = UserInfo()
                user_info.set_cust_id(user.email)
                user_info.set_address(address)
                user_info.set_email(user.email)
                user_info.set_first_name(user.first_name)
                user_info.set_last_name(user.last_name)
                user_info.set_mobile(phone)
                user_info.set_pincode(pin_code)
                # initialize an Hash/Array
                paytmParams = {}

                paytmParams["MID"] = "WorldP64425807474247"
                paytmParams["ORDERID"] = str(id)

                # Generate checksum by parameters we have
                # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
                paytmChecksum = PaytmChecksum.generateSignature(paytmParams, key)
                # print("generateSignature Returns:" + str(paytmChecksum))

                payment_details = PaymentDetailsBuilder(channel_id, order_id, txn_amount, user_info).build()
                response = Payment.createTxnToken(payment_details)
                details: TransctionDetail = TransctionDetail.objects.create(user=req.user,order_id=order_id, amount=price)
                details.save()
                return render(req, 'payment/payment.html', {'order_id': id, 'price': price, 'res': response }) # replace id by order.id
        except User.DoesNotExist as e:
            return HttpResponseForbidden(e)
        except UserModel.DoesNotExist as e:
            return HttpResponseForbidden("Not Valid")
        except Exception as e:
            return InternalServerError(e)
    elif req.method == 'GET':
        try:
            prices = Pricing.objects.all().order_by('plan_price')
            most_popular = prices.order_by('-plan_users')[0].plan_users
            for price in prices :
                if price.plan_users == most_popular: 
                    price.most_popular = True
                else: 
                    price.most_popular = False
            return render(req, 'pricing.html', {'success': False, 'prices' : prices[:3] })
        except Exception as e: 
            return InternalServerError(e)
    elif req.method == "POST" and not req.user.is_authenticated:
        return redirect('/login')
    return HttpResponseNotAllowed("Not Allowed")

@csrf_exempt
def validate(req: HttpRequest):
    if req.method == 'GET': raise Http404('Not Found')
    # import checksum generation utility
    paytmChecksum = ""
    received_data = req.POST

    # Create a Dictionary from the parameters received in POST
    # received_data should contains all data received in POST
    paytmParams = {}
    for key2, value in received_data.items(): 
        if key2 == 'CHECKSUMHASH':
            paytmChecksum = value
        else:
            paytmParams[key2] = value

    # Verify checksum
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    isValidChecksum = PaytmChecksum.verifySignature(paytmParams, key, paytmChecksum)
    if isValidChecksum:
        # Handle logic for successful or unsuccessful transactions later
        id = paytmParams["ORDERID"]
        code = paytmParams["RESPCODE"]
        deatils = PaymentDetail(BANKNAME=paytmParams["BANKNAME"],BANKTXNID= paytmParams["BANKTXNID"],CURRENCY=paytmParams["CURRENCY"],GATEWAYNAME=paytmParams["GATEWAYNAME"],ORDERID=paytmParams["ORDERID"],PAYMENTMODE=paytmParams["PAYMENTMODE"],RESPCODE=paytmParams["RESPCODE"],RESPMSG=paytmParams["RESPMSG"],STATUS=paytmParams["STATUS"],TXNAMOUNT=paytmParams["TXNAMOUNT"],TXNID=paytmParams["TXNID"],TXNDATE=dateparse.parse_datetime(paytmParams["TXNDATE"])) 
        deatils.save()
        try : 
            tDetail: TransctionDetail = TransctionDetail.objects.get(order_id=id)
            if code == "01":
                ## Handle for success
                tDetail.status = 's'
                tDetail.save(update_fields=['status'])
                return render(req, 'pricing.html', {'success': True, 'details': deatils})
            else:
                ## Handle for failure
                tDetail.status = 'f'
                tDetail.save(update_fields=['status'])
                return render(req, 'pricing.html', {'success': False})
        except TransctionDetail.DoesNotExist as e:
            return render(req, 'pricing.html', {'success': False})
        except Exception as e:
            print(e)
            return InternalServerError(e)
    else:
        return render(req, 'pricing.html', {'success': False})