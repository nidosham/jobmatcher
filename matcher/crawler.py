import urllib
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os


# from indeed.com

def load_jobs_div(job_title, location):
    getVars = {'q': job_title, 'l': location,
               'fromage': 'last', 'sort': 'date'}
    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="resultsCol")
    return job_soup


def extract_job_details(job_soup, search_category):
    job_fields = job_soup.find_all('div', class_='jobsearch-SerpJobCard')

    cols = []
    job_info = []

    if 'titles' in search_category:
        titles = []
        cols.append('titles')
        for job_field in job_fields:
            titles.append(extract_job_title(job_field))
        job_info.append(titles)

    if 'links' in search_category:
        links = []
        cols.append('links')
        for job_field in job_fields:
            links.append(extract_link(job_field))
        job_info.append(links)

    if 'companies' in search_category:
        companies = []
        cols.append('companies')
        for job_field in job_fields:
            companies.append(extract_company(job_field))
        job_info.append(companies)

    if 'date_listed' in search_category:
        dates = []
        cols.append('date_listed')
        for job_field in job_fields:
            dates.append(extract_date(job_field))
        job_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = job_info[j]

    num_listings = len(job_info[0])

    return jobs_list, num_listings


def extract_job_title(job_field):
    title_field = job_field.find('h2', class_='title')
    title = title_field.text.strip()
    return title


def extract_company(job_field):
    company_field = job_field.find('span', class_='company')
    company = company_field.text.strip()
    return company


def extract_link(job_field):
    link = job_field.find('a')['href']
    link = 'www.indeed.com/' + link
    mod_link = link
    link = mod_link.replace("/rc/clk", "viewjob")
    linkList = link.split("=")
    link = linkList[0]+"="+linkList[1]
    return link


def extract_date(job_field):
    date_field = job_field.find('span', class_='date')
    date = date_field.text.strip()
    return date


def find_jobs_from(website, job_title, location, search_category, filename="results.xls"):
    """
    This function extracts all the desired characteristics of all new job postings
    of the title and location specified and returns them in single file.
    The arguments it takes are:
        - Website: to specify which website to search (options: 'Indeed' or 'CWjobs')        
        - search_category: this is a list of the job characteristics of interest,
            from titles, companies, links and date_listed.
        - Job_title
        - Location
        - Filename: to specify the filename and format of the output.
            Default is .xls file called 'results.xls'
    """
    jobs_list = []
    if website == 'Indeed':
        job_soup = load_jobs_div(job_title, location)
        jobs_list, num_listings = extract_job_details(
            job_soup, search_category)
        return jobs_list
