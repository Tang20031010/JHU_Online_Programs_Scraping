from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime, timedelta


URL = "https://cty.jhu.edu/programs/online/courses?field_qualifying_level_value=All&field_eligibility_course_type_value=All&program_type[]=54279&program_type[]=63553&program_type[]=40249&program_type[]=35&grade[]=8&grade[]=9&grade[]=10&grade[]=11&topic[]=128576&topic[]=128575&topic[]=128572&topic[]=126668&topic[]=128574&topic[]=128573&page=6"
root = requests.get(URL, headers = {'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(root.text, 'html.parser')
holders = soup.find('div', class_='views-infinite-scroll-content-wrapper clearfix')
holders_lin = holders.findAll('div', class_= 'cty-card__grid-meta')
urls = []
JHU_Programs = []
college_name = "Johns Hopkins University"
program_name = "Johns Hopkins Center for Talented Youth"

for element in holders_lin:
    l1 = element.find('a')
    l2 = l1.get('href')
    l3 = "https://cty.jhu.edu/"
    l = l3 + l2
    urls.append(l)

for url in urls[0:]:
    each_program = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
    program_soup = BeautifulSoup(each_program.text, 'html.parser')
    program_holder = program_soup.find('div', class_= 'node__content clearfix')
    course_name = program_holder.find('h2').text
    program_description = program_holder.find('p').text
    program_temp = program_holder.find('div', class_= 'views-element-container')
    program_check = program_temp.find('div')
    program_check2 = program_check.get('class')
    
    if('no-results' in program_check2):
        program_tuition = ''
    else:
        program_tuition_temp = program_temp.find('div', class_= 'views-field views-field-field-fee-amount')
        program_tuition_temp2 = program_tuition_temp.find('div', class_='field-content').text
        program_tuition = program_tuition_temp2.replace('$', '')
    
    program_eli_temp = program_holder.find('div', class_='field field--name-field-eligibility-course-type field--type-list-string field--label-hidden')
    program_eligibility1 = program_eli_temp.find('p').text
    
    program_eli_temp2 = program_eli_temp.find('div', class_= 'clearfix text-formatted field field--name-field-course-prerequisites field--type-text-long field--label-hidden field__item')
    if (program_eli_temp2 is not None):
        program_eligibility2 = program_eli_temp2.find('p').text
    else:
        program_eligibility2 = ''
    program_eligibility = program_eligibility1 + ' ' + program_eligibility2

    application_fee = 15

    if 'NCAA' in course_name:
        credit_offer = 'college'
    else:
        credit_offer = 'no'
    

    category = ''
    app_date = ''
    other_fee = 20
    start_date = ''
    end_date = ''
    JHU_Programs.append([college_name, program_name, course_name, 
                            category, program_description, 'remote', 'remote', 
                            '', "United States", "no", "yes", 'no', "no", "no", "yes", "no", 
                            application_fee, app_date, "0", other_fee, credit_offer, program_tuition, start_date, end_date, program_eligibility, "9-12", url])

df = pd.DataFrame(JHU_Programs, columns=["college", "program_name", "course_title", "program_category",
                                        "course_description", "city", "state", "zip_code", "country", "residential", 
                                        "application", "transcript", "letter_of_recommendation", "counselor_report",
                                        "test_scores", "toefl_or_english_exam", "app_fee", "app_date", 
                                        "enrollment_fee", "fees", "credit_offerred", "tuition", "start_date", "end_date", "eligibility_requirements",
                                        "grades", "link"])
df.to_csv('JHU_programs.csv')