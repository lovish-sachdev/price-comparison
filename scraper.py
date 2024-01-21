## OM NAMAH SHIVAY
import requests
from bs4 import BeautifulSoup as soup
import random,time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import streamlit as st

# flipkart="https://www.flipkart.com/search?q="
# reliance_link="https://www.reliancedigital.in/search?q="
# product_list=["boat airdopes","samsung galaxy s23","oneplus pad","fire boltt phoenix"]
# product_list=["boat airdopes"]

# links=["https://www.amazon.in/s?k=samsung+s23+ultra+5g&crid=19V6DSPG3VG95&sprefix=sams%2Caps%2C231&ref=nb_sb_ss_ts-doa-p_1_4"]

# product_text=random.sample(product_list,1)


class flipkart_scraper:

    def get_description(self,product_text):
        useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        HEADERS=({"user-agent":useragent,"Accept-Language":"en-US , en;q=0.5"})

        flipkart="https://www.flipkart.com/search?q="
        url=flipkart+product_text
        print(url)
        response=requests.get(url,headers=HEADERS)
       
        if response.status_code==200:
            time.sleep(5)
            content=response.content
            soup_obj=soup(content,"html.parser")
            div_1=soup_obj.find_all("div",class_="_1AtVbE col-12-12")
            new_div_1=[]
            for element in div_1:
                ele=element.find("div",class_="_13oc-S")
                if ele!=None:
                    new_div_1.append(ele)
            products=[]
            pattern=None
            for ele in new_div_1:
                products.extend(ele.find_all("div",recursive=False))
                if  pattern==None:
                    if len(ele.find_all("div",recursive=False))==1:
                       pattern="100%"
                    else:
                        pattern="25%"
            if pattern=="100%":
                return self.hundred_percent(products)
            else:
                return self.twenty_percent(products)
        else:
            print(f"error {response.reason}")
        
    def hundred_percent(self,products):
        description_dict={}
        for index,product in enumerate(products):
            product_dict={}
            img_src=product.find("div",class_="CXW8mj").img["src"]
            st.write(img_src)
            title=product.find("div",class_="_4rR01T").text
            price_data=product.find("div",class_="_25b18c")
            if price_data!=None:
               price_data=price_data.find_all("div",recursive=False)
            curr_price=price_data[0].text
            try:
                mrp=price_data[1].text
                discount=price_data[2].find("span").text
                product_dict["mrp"]=mrp
                product_dict["discount"]=discount
            except:
                pass
            product_url="https://www.flipkart.com"+product.find("a",class_="_1fQZEK").attrs["href"]
            features=product.find_all("li")
            for i in range(len(features)):
                features[i]=features[i].text.strip()

            product_dict["curr_price"]=curr_price
            product_dict["title"]=title
            product_dict["features"]=features
            product_dict["product_url"]=product_url
            description_dict["product_"+str(index+1)]=product_dict
        return description_dict

    def twenty_percent(self,products):
        description_dict={}
        for index,product in enumerate(products):
            product_dict={}
            img_src=product.find("div",class_="CXW8mj").img["src"]
            st.write(img_src)
            price_data=product.find("div",class_="_25b18c").find_all("div",recursive=False)
            
            curr_price=price_data[0].text
            try:
                mrp=price_data[1].text
                discount=price_data[2].find("span").text
                product_dict["mrp"]=mrp
                product_dict["discount"]=discount
            except:
                pass
            
            title_url=product.find("a",class_="s1Q9rs")
            
            title=title_url.attrs["title"]
            features=None
            
            product_url="https://www.flipkart.com"+title_url.attrs["href"]
            product_dict["curr_price"]=curr_price
            product_dict["title"]=title
            product_dict["features"]=features
            product_dict["product_url"]=product_url
            description_dict["product_"+str(index+1)]=product_dict
        return description_dict

class croma_scrapper:
    def get_description(self,product_text):
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        product_text=product_text.split(" ")
        product_text="%20".join(product_text)
        product_text=product_text+"%3Arelevance&text="+product_text
        croma="https://www.croma.com/searchB?q="    
        url=croma+product_text
        driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)    
        driver.get(url)
       

        time.sleep(5)
        content=driver.page_source

        soup_obj=soup(content,"html.parser")
        
        products=soup_obj.find_all("li",class_="product-item")
        description_dict={}
      
        for index,product in enumerate(products):
            product_dict={}
            img_src=product.find("div",class_="product-img").find("img").attrs["src"]
            
            info_div=product.find("div",class_="product-info")
            title_url=info_div.find("h3",class_="product-title plp-prod-title").a
            title=title_url.text
            product_url="https://www.croma.com"+title_url.attrs["href"]
            curr_price=info_div.find("span",class_="amount plp-srp-new-amount").text
            try:
                mrp_discount=info_div.find("div",class_="cp-price discount-container").find_all("span",recursive=False)
                mrp=mrp_discount[0].text.strip()
                discount=mrp_discount[2].text.strip()            
                product_dict["mrp"]=mrp
                product_dict["discount"]=discount
            except:
                pass
            product_dict["curr_price"]=curr_price

            product_dict["title"]=title
            product_dict["features"]=None
            product_dict["product_url"]=product_url
            description_dict["product_"+str(index+1)]=product_dict
        driver.quit()
        return description_dict   
            # discount=mrp_parent.find_all("span",recursive=False)[2].text
            # print(title,url,discount)
            
           
class reliance_digital:
    def get_description(self,url,headers):
        driver=webdriver.Chrome(options=headers)
        driver.get(url)
        print("accessed")
        print(url)
        time.sleep(15)
        content=driver.page_source
        soup_obj=soup(content,"html.parser")
        products=soup_obj.find_all("li",class_="grid pl__container__sp blk__lg__3 blk__md__4 blk__sm__6 blk__xs__6")
        for product in products:
            product=product.find("div",class_="sp__product").find_all()
            img_src=product[0].find("img").attrs["src"]
            title=product[1].find("p",class_="sp__name")
            print(title)
            break

def perform(product_text):
    flipkart=flipkart_scraper()
    dicty1=flipkart.get_description(product_text)
    st.write(dicty1)


    # croma=croma_scrapper()
    # dicty=croma.get_description(product_text)
    # # print(dicty)
    # st.write(dicty["product_1"])

product_text=st.text_input(label="product")
st.button(label="run",on_click=lambda:perform(product_text))
# perform("iphone 14")
