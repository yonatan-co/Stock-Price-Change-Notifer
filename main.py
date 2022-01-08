from selenium import webdriver
import time
import yagmail
import os 

password = os.environ['PASSWORD']
sender = os.environ['MY_EMAIL']


reciver = os.environ['EMAIL_RECIVER']

yag = yagmail.SMTP(user=sender, password=password)

def get_drvier():
  options = webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")

  driver = webdriver.Chrome(options=options)
  driver.get("https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6")
  return driver


def clean_price_change(text):
  clean_text = float(text[:-1])
  return clean_text


def main():
  driver = get_drvier()
  
  time.sleep(10)
  price_change = clean_price_change(driver.find_element(by='xpath', value='/html/body/div[2]/div/section[1]/div/div/div[2]/span[2]').text)
  time.sleep(2)
  
  if price_change < -0.10:
    content =  f"""hello, we want to update you that the price of the stock you own has changed by {str(price_change)}%"""
    yag.send(to=reciver, contents=content)
    print(f"""email sent to:{reciver} \n email content:{content}""")
  else:
    content = f"""hello, we want to update you that the price of the stock you own is stable."""
    yag.send(to=reciver, contents=content)
    print(f"""email sent to:{reciver} \n email content:{content}""")
      
      

print(main())
