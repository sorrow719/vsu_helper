import re
from selenium import webdriver
from urllib import request, error

site = "http://109.195.55.25"

driver = webdriver.PhantomJS(executable_path="C:/Users/Sorrow/node_modules/phantomjs/lib/phantom/bin/phantomjs.exe")
driver.get(site)
links = re.findall('/links/link[a-zA-Z0-9]+',driver.page_source)
js_src = driver.find_elements_by_xpath('//script')[1].get_attribute('src')
driver.get(js_src)
links += re.findall('/links/link[a-zA-Z0-9]+', driver.page_source)

for link in links:
    code=None
    try:
        conn = request.urlopen(site+link)
        code = conn.code
    except error.HTTPError as e:
        code = e.code
    print(site+link+' code:'+str(code))

driver.quit()