import sys
sys.path.append('..')
from modules.httprequest import httpRequest
import re
import json

def saveCaptchaImage():
    requestObj = httpRequest()
    url = "https://ecfme.famiport.com.tw/fmedcfpwebv2/CodeHandler.ashx"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    }
    result = requestObj.doRequest(url=url, method="GET", headers=headers)

    #NOTE 存檔
    img_data = result.content
    with open('captcha.png', 'wb') as handler:
        handler.write(img_data)

    return result


def uploadOCR():
    requestObj = httpRequest()
    url = "https://www.prepostseo.com/frontend/uploadReverseImageFiles"
    headers = {
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'accept' : 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with' : 'XMLHttpRequest',    }
    files = {'file': open('captcha.png', 'rb')}

    result = requestObj.doRequest(url=url, method="POST", headers=headers, files=files)
    return result


def doImageToText(img_url = ""):

    requestObj = httpRequest()
    url = "https://www.prepostseo.com/frontend/extractImgText"
    headers = {
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    }
    data = {'submit': 'true', 'imgUrl':img_url}
    result = requestObj.doRequest(url=url, method="POST", headers=headers, data=data)
    return result

def doInquiryOrders(cookies = {}, ec_order = '', text = ''):
    requestObj = httpRequest()
    url = "https://ecfme.famiport.com.tw/fmedcfpwebv2/index.aspx/InquiryOrders"
    headers = {
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'content-type': 'application/json; charset=UTF-8',
            'cookie': cookies,
    }
    data = {'ListEC_ORDER_NO': [ec_order], 'CODE':text}
    result = requestObj.doRequest(url=url, method="POST", headers=headers, json=data)
    return result

def getOrderDetail(ec_order_no = '', order_no = ''):
    requestObj = httpRequest()
    url = "https://ecfme.famiport.com.tw/fmedcfpwebv2/index.aspx/GetOrderDetail"
    headers = {
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'content-type': 'application/json; charset=UTF-8',
    }
    data = {'EC_ORDER_NO': ec_order_no, 'ORDER_NO':order_no, 'RCV_USER_NAME':None}
    result = requestObj.doRequest(url=url, method="POST", headers=headers, json=data)
    return result


if __name__ == "__main__":
   
   #TODO 店商訂單編號
    ec_order = ""


     #TODO 下載驗證圖
    save_captcha_image_info = saveCaptchaImage()    
    #NOTE 取出cookie 驗證時使用
    cookies = save_captcha_image_info.cookies
    cookies_str = 'ASP.NET_SessionId='+cookies['ASP.NET_SessionId']+';fmeweb='+cookies['fmeweb']+';'
    # sys.exit()

     
    #TODO 上傳OCR網頁
    result = uploadOCR()
    res_dic = result.json()
    image_path = res_dic.get('data').get('image_path')

    #TODO 取得解析OCR結果
    result = doImageToText(image_path)
    res_dic = result.json()
    text_ori = res_dic.get('text')
    #NOTE 解析回傳結果 
    text = re.sub(r'[^\d]', '', text_ori)

    #TODO 取得透過EC訂單編號 取得 全家物流訂單編號 (不知道全家物流訂單編號前提)
    result = doInquiryOrders(cookies = cookies_str, ec_order = ec_order, text = text)
    print(result.json())

    res = result.json()
    res_dic = json.loads(res['d'])
    ec_order_no = res_dic.get('List')[0].get('EC_ORDER_NO')
    order_no = res_dic.get('List')[0].get('ORDER_NO')

    #TODO 取得透過EC訂單編號&全家物流訂單編號 取得 訂單資訊
    result = getOrderDetail(ec_order_no = ec_order_no, order_no = order_no)
    res = result.json()
    res_dic = json.loads(res['d'])

    print(result.json())
    print(res_dic)


    # sys.exit()


