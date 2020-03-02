from urllib.request import urlopen
from bs4 import BeautifulSoup
from github import Github, Issue
import datetime
from pytz import timezone
import os
from dateutil.parser import parse

sites = [ 'https://smartstore.naver.com/kumaelectron/products/4813999869'
         ,'https://smartstore.naver.com/kumaelectron/products/4754238400'
         ,'https://smartstore.naver.com/kumaelectron/products/4754246120'
         ,'https://smartstore.naver.com/kumaelectron/products/4754248104'
         ,'https://smartstore.naver.com/aer-shop/products/4722827602'
         ,'https://smartstore.naver.com/korea-mask/products/4825762296'
         ,'https://smartstore.naver.com/mfbshop/products/4072573492'
         ,'https://smartstore.naver.com/mfbshop/products/4735164530'
         ,'https://smartstore.naver.com/mfbshop/products/4735160554'
         ,'https://smartstore.naver.com/mfbshop/products/4680268551'
         ,'https://smartstore.naver.com/mfbshop/products/4072435942'
         ,'https://smartstore.naver.com/mfbshop/products/4114661363'
         ,'https://smartstore.naver.com/etiqa/products/4817982860'
         ,'https://smartstore.naver.com/gonggami/products/4705579501'
        ]

availe_list = ''
oos_list = ''

for site in sites:
    res = urlopen(site)
    soup = BeautifulSoup(res, 'html.parser')
    buy_span = soup.select('#wrap > div > div.prd_detail_basic > div.info > form > fieldset > div > div.prd_type3 > div.btn_order.v2 > span.buy')
    
    product_title = soup.select('#wrap > div > div.prd_detail_basic > div.info > form > fieldset > div._copyable > dl > dt > strong')
    if product_title:
        product_title = str(product_title[0]).replace('<strong>','').replace('</strong>','')

        image = soup.select('#wrap > div > div.prd_detail_basic > div._image.view > div.bimg > div.img_va > img')
        image = image[0].attrs['src']
        image = '<img src="%s" style="width:100px;"/><br/>'%(image)

        if '<span class="mask2">' in str(buy_span):
            oos_status = '[품절]'
            oos_list += '<a href="%s" target="_blank">%s %s</a><br/>'%(site, oos_status, product_title)
            print(oos_status, product_title)
        else :
            oos_status = '[판매중]'
            availe_list += '<a href="%s" target="_blank">%s %s</a><br/>'%(site, oos_status, product_title)
            print(oos_status, product_title)


KST = timezone('Asia/Seoul')
date = datetime.datetime.now(KST)
today = date.strftime("%Y-%m-%d")

issue_title = "마스크 판매! (%s)" % (date.strftime("%Y년 %m월 %d일 %H시 %M분"))
issue_body = availe_list + '---------------------------------<br/>' + oos_list

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
REPO_NAME = "crawler-check-mask-stocks"
repo = Github(GITHUB_TOKEN).get_user().get_repo(REPO_NAME)
if issue_body != '' and '판매중' in issue_body and REPO_NAME == repo.name:
    res = repo.create_issue(title=issue_title, body=issue_body)
    print(res)
else:
    print(date.strftime("%Y년 %m월 %d일 %H시 %M분"), '대상건이 없음')
