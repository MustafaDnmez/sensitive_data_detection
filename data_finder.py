import requests
from bs4 import BeautifulSoup
import re 
import sys



keys=[
    {
"Twitter Access Token":"[1-9][ 0-9]+-[0-9a-zA-Z]{40}", 
"Facebook Access Token":"EAACEdEose0cBA[0-9A-Za-z]+",
"Facebook OAuth 2.0":"[A-Za-z0-9]{125} (counting letters [2])",
"Instagram OAuth 2.0":"[0-9a-fA-F]{7}\.[0-9a-fA-F]{32}",
"Google API Key":"AIza[0-9A-Za-z-_]{35}",
"Google OAuth 2.0 Auth Code":"4/[0-9A-Za-z\-_]+",
"Google OAuth 2.0 Refresh Token":"1/[0-9A-Za-z\-_]{43}|1/[0-9A-Za-z\-_]{64}",
"Google OAuth 2.0 Access Token":"ya29\.[0-9A-Za-z\-_]+",
"GitHub Personal Access Token (Classic)":"^ghp_[a-zA-Z0-9]{36}$",
"GitHub Personal Access Token (Fine-Grained)":"^github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}$",
"GitHub OAuth 2.0 Access Token":" ^gho_[a-zA-Z0-9]{36}$",
"GitHub User-to-Server Access Token":" ^ghu_[a-zA-Z0-9]{36}$",
"GitHub Server-to-Server Token":" ^ghs_[a-zA-Z0-9]{36}$",
"GitHub Refresh Token":" ^ghr_[a-zA-Z0-9]{36}$",
"Mapbox Public Key":"([s,p]k.eyJ1Ijoi[\w\.-]+)",
"Mapbox Secret Key":"([s,p]k.eyJ1Ijoi[\w\.-]+)",
"Foursquare Secret Key":"R_[0-9a-f]{32}",
"Picatic API Key":"sk_live_[0-9a-z]{32}",
"Paypal / Braintree Access Token":"access_token\,production\$[0-9a-z]{161[0-9a,]{32}",    
"Amazon Marketing Services Auth Token":"amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-10-9a-f1{4}-[0-9a,]{4}-[0-9a-f]{12}",         	
"Twilio API key":"55[0-9a-fA-F]{32}",
"MailGun API Key":"key-[0-9a-zA-Z]{32}",
"MailChimp API Key":"[0-9a-f]{32}-us[0-9]{1,2}",
"Slack OAuth v2 Bot Access Token":"xoxb-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}",
"Slack OAuth v2 User Access Token":"xoxp-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}",
"Slack OAuth v2 Configuration Token":"xoxe.xoxp-1-[0-9a-zA-Z]{166}",
"Slack OAuth v2 Refresh Token":"xoxe-1-[0-9a-zA-Z]{147}",
"Slack Webhook":"T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
"Amazon Web Services Access Key ID":"AKIA[0-9A-Z]{16}",
"Amazon Web Services Secret Key":"[0-9a-zA-Z/+]{40}",
"Google Cloud Platform OAuth 2.0":"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
"Google Cloud Platform API Key":"[A-Za-z0-9_]{21}--[A-Za-z0-9_]{8}",
"Heroku API Key":"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
"Heroku OAuth 2.0":"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}" ,
"stripe_standard_api" : "sk_live_[0-9a-zA-Z]{24}",
"stripe_restricted_api" : "rk_live_[0-9a-zA-Z]{24}",
"json_web_token" : "ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$"
}
]


def crawl(domain):
    web_site=domain
    site=requests.get(web_site,verify=False)
    content=site.text
    texts=content.splitlines()
    soup=BeautifulSoup(site.content,"html.parser")

   
    #check api with regex query in list keys
    def check_api(text):
        values_list=list(keys[0].values())
        keys_list=list(keys[0].keys())

        for api in values_list:
            
            checked=re.findall(api,text,re.IGNORECASE)
            if checked:
                for api_key in checked:
                    position=values_list.index(api)
                    print(f"Platform:{keys_list[position]}  key:{api_key}")
            
            
    # find email in all source code          
    def find_email():
        emails = re.findall(r"[a-z0-9\.\-+]+@[a-z0-9\.\-+]+\.[a-z]+", content)
        unique_mail=set(emails)
        print(unique_mail)
    # find username password and token in input element and get value
    def userpass_atrr():
        keywords=["email","Password","password","username","user","_token","token","csrf-token","api","apikey","api-key"]
        for key in keywords: 
    
            token=soup.find_all(attrs={"name":key},)
            if token!=[]:
                if key=="csrf-token":
                    print(token[0]["content"])
                for x in token:
                    try:
                        print(f'{key}={x["value"]}')
                    except:
                        pass   
#check username and password in text but get much false positive   
# def userpass_text(data):
#      if re.search(r"\b(username|password)\b", data, re.IGNORECASE):
#         print(data)
    find_email()                   
    userpass_atrr()

    for text in texts:
        # filtere  the text include api ,key and  token than send the text to cehck_api function
        if re.search(r'\b(api|key|token|endpoint)\b',text,re.IGNORECASE):
            check_api(text)

try:
    domain = sys.argv[1] 
    #if input is a file open and read it by line
    if ".txt" in domain:
        text_file=[]
        with open(domain,"r") as file:
            text_file=file.readlines()
        for domains in text_file:
     
            crawl(domains)
    else:
        crawl(domain)
except IndexError:
    print('Syntax Error - python3 data_finder.py <domain or domains file with txt>')