# Pull data from applied jobs, where both title and company are represented. SAve to excel file
# Pull up this data up as a source, then compare current company title and company to every representation
# Skip over jobs which I do not want to apply to
"""
Created on Sat Jan 13 12:25:38 2018

@author: arthu
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# open browser
browser = webdriver.Firefox()
browser.get('https://linkedin.com')

Function = "Data"
Location = "Toronto"
# log in to account
emailElem = browser.find_element_by_id('login-email')
emailElem.send_keys('my-email')

passwordElem = browser.find_element_by_id('login-password')
passwordElem.send_keys('my-password')
passwordElem.submit()
time.sleep(30)

# Note, these will all be commented out until further notice, as the desirable URL can simply be selected

## Select "Jobs" Tab
#browser.find_element_by_id('jobs-tab-icon').click()
#time.sleep(10)
#
## Fill in "Function" Form
#FunctionElem = browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[3]/div/div[1]/div/div/div[1]/artdeco-typeahead/artdeco-typeahead-input/input[2]')
#FunctionElem.send_keys(Function)
#
## Fill in "Location" Form 
#browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[3]/div/div[1]/div/div/div[2]/artdeco-typeahead/artdeco-typeahead-input/input[2]').send_keys(Location)
#
## Submit form "press search"
#browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[3]/div/div[1]/div/div/button').click()


# Select URL you want to navigate to
browser.get('https://www.linkedin.com/jobs/search/?f_E=2%2C3&f_LF=f_AL&keywords=it&location=Toronto%2C%20Canada%20Area&locationId=ca%3A4876')
#Allow for selection of EZApply and desired credentials
time.sleep(30)
# Pull currentURL

#Pulls Current URL
Current_URL = browser.current_url 
        
def Scroller() :
    """
        arg: None
        description: takes the opened URL and scrolls to the bottom of the page
        returns: None
    """
    htmlElem = browser.find_element_by_tag_name('html')
    for i in range(100) :
        htmlElem.send_keys(Keys.DOWN)
    
def EZApply() :        
    """
        arg: None
        description: applies for the current job opening
        returns: None
    """
    # Open up application
    browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[3]/div/div/button').click()
    time.sleep(5)
     # Send Phone Number Keys to form
    Phoneelem = browser.find_element_by_id('apply-form-phone-input')
    Phoneelem.click()
    # Needs to click on form time.sleep(3)
    for i in '6134831772' :
        Phoneelem.send_keys(i)
    time.sleep(3)
    # Press Resume Button 4
    browser.find_element_by_xpath('/html/body/div[5]/div[6]/div/div[1]/div/div/div/form/div/form/div[1]/div/span').click()
    time.sleep(3)  
    
    # Select Resume from Dropdown
    browser.find_element_by_xpath('/html/body/div[5]/div[6]/div/div[1]/div/div/div/form/div/form/div[2]/ol[1]/li/button').click()
    time.sleep(5)
    
    #Unselect "follow X" company
    browser.find_element_by_xpath('/html/body/div[5]/div[6]/div/div[1]/div/div/div/form/div/div/label').click()
    time.sleep(5)
    
    # Submit Application
    browser.find_element_by_xpath("/html/body/div[5]/div[6]/div/div[1]/div/div/div/form/footer/div/button[2]").click()
    time.sleep(5)
    
def WebScraper() :
    """
        arg: None
        description: applies for the current job opening
        Returns: List of URLS
    """
## Pull all URL's on current page. Commented out until further notice
#    URLlist = []
#    elems = browser.find_elements_by_xpath("//a[@href]")
#    for elem in elems:
#        URLlist.append(elem.get_attribute("href"))
#    print(URLlist)
## Iterate through list, deleted all non-jobs
#    while len(URLlist) > 50 : 
#        try : 
#            for i in range(len(URLlist)) :
#                if "jobs/view" not in URLlist[i] :
#                    del URLlist[i]
#        except Exception as e :
#            print(e)
#            print(len(URLlist))
## eliminate duplicates
#    URLlist = list(set(URLlist))
    
# Testing some code for clicking instead of keeping URL's
    elems = browser.find_elements_by_class_name("truncate-multiline--truncation-target")
    print(elems)
    print("the number of jobs I found:", len(elems))
    return elems

def badRole(elems) :
    print(elems)
    elems = elems.lower()
# Check for special roles I don't want
    if elems == "analytics consultant (entry level)" :
        return 0
    elems = elems.replace("/","").split(" ")
    print(elems)
    badroles = 'sales sale account accounting bilingual mortgage \
            receptionist underwriter customer service lawyer '
    for i in elems :
        if i in badroles :
            return 0
        else : 
            return 1
    
        
# Iterate through each webpage, calling scroller and EZapply to
def WebHANDLER(Counter=0, Current_URL = Current_URL, Job_Index = 0) :
# add counter to the end of the URL, to navigate to the next page
     print(Current_URL)
     print(Counter)
     if Counter != 0:
         Current_URL = Current_URL + "&start=" + str(Counter) 
     else :
         pass
# Navigate to the next page
     
     browser.get(Current_URL)
     time.sleep(15)
#Call Scroller, Call Scraper and store scraper value

     j = 0
# For every URL value returned, do easy application
     for i in range(Job_Index,25) :
         try :
# Click through each element iteratvly. # To continue where you left off, change Job_Index to which job you were at (only for first page)
            Scroller()
            time.sleep(30)
            elems = browser.find_elements_by_class_name("job-card-search__title-line")
#Test to see if elems.text is a title that I don't want           
            roletest = badRole(elems[i].text)
            if roletest == 0:
                print('job skipped because it has a role that is not desirable')
                continue
            elems[i].click()
            time.sleep(30)
            try :
                EZApply()
                browser.back()
                time.sleep(45)
                
                j =j + 1
                print("Number of applications", j)
            except Exception as e :
               print(e)
               print("Webhandler not completed (probably already applied)")  
               browser.back()
               time.sleep(60)
         except Exception as e :
            print("Error with scrolling or with clicking: ",e)
            browser.get(Current_URL)
            time.sleep(30)

def main(main_counter=0,Main_Job_Index=0) :
   """ 
   Arguments = None
   Executes Webhandler, and all other relevant applications. #######Maybe add some error handling#####
   Returns: None
   """
   for i in range(20) :
       if i == 0 :
           WebHANDLER(Counter=main_counter,Job_Index=Main_Job_Index) # calls the job index to start applying for the jobs starting at the specified index
           main_counter = main_counter + 25
       else :
           WebHANDLER(Counter=main_counter)
           main_counter = main_counter + 25

       
main(main_counter=0,Main_Job_Index=0)

