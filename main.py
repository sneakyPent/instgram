import argparse
import getopt
import random
import time
import sys

import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle

# Arguments variables
argv = sys.argv[1:]
opts = ''
postURL = ''

# seconds
browser = webdriver.Chrome()
secondRangeStart = 5
secondRangeEnd = 10
delay = 15000
commentBlock = 120
comments = 301
prevComments = -1
cookieFilepath = "cookies.pkl"
host = 'https://www.instagram.com'
username = ""
password = ""
friends = [
	"@mariazachaa ",
	"@zacharioudakis_ ",
	"@giorgos_aerakis ",
	"@evi_kalbe ",
	"@manosverigos ",
	"@grimm_emmanuel_helmut ",
	"@giwrgos_grammatikakis ",
	# "@giorgos.evangelopoulos ",
	# "@panagioulakis ",
	"@lu_tsag ",
	"@thodorisapost ",
	"@mikaeligi ",
	# "@johnmosxakis "
]


def get_arguments():
	global opts
	# Construct the argument parser
	ap = argparse.ArgumentParser()
	# Add the arguments to the parser
	ap.add_argument("-l", "--login", help="For logging in")
	ap.add_argument("-o", "--open", help='For opening after logging in')
	ap.add_argument("-g", "--post", help="The post")
	ap.add_argument("-p", "--password", help="Login Password")
	ap.add_argument("-u", "--username", help="Login Username")
	opts, args = getopt.getopt(argv, 'lou:p:g:')


def get_random_names():
	rNames = []
	for i in range(3):
		# getting random name from friends
		curName = random.choice(friends)
		# check if name is already in the list
		while curName in rNames:
			curName = random.choice(friends)
		# append new name in the list
		rNames.append(curName)
	listToStr = ' '.join([str(cur) for cur in rNames])
	return listToStr


def logging_in():
	tmp = webdriver.Chrome()
	tmp.get(host)
	tmp.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]').click()
	# wait until find username input and add username
	WebDriverWait(tmp, delay).until(
		EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
	tmp.find_element_by_name("username").send_keys(username)
	# wait until find password input and add password
	WebDriverWait(tmp, delay).until(
		EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
	tmp.find_element_by_name("password").send_keys(password)
	# Click login button
	WebDriverWait(tmp, delay).until(
		EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
	tmp.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()

	# storing the cookies
	time.sleep(5)
	pickle.dump(tmp.get_cookies(), open(cookieFilepath, "wb"))
	tmp.quit()


def open_insta():
	global browser
	browser = webdriver.Chrome()
	browser.get(host)
	# loading the stored cookies
	cookies = pickle.load(open(cookieFilepath, "rb"))
	for cookie in cookies:
		browser.add_cookie(cookie)
	browser.get(host)
	browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()


def find_post(post):
	global browser
	browser.get(host + '/p/' + post)


def exit_post():
	instaLogo = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/div'
	WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, instaLogo)))
	browser.find_element_by_xpath(instaLogo).click()


def add_comment(comment):
	# find comment area click on it
	commentTextAreaXpath = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea'
	commentDivXpath = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div'
	WebDriverWait(browser, delay).until(
		EC.presence_of_element_located((By.XPATH, commentDivXpath)))
	browser.find_element_by_xpath(commentDivXpath).click()
	WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, commentTextAreaXpath)))
	commentText = browser.find_element_by_xpath(commentTextAreaXpath)
	commentText.send_keys(comment)


def submit_comment():
	sButton = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/button'
	WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, sButton)))
	browser.find_element_by_xpath(sButton).click()


def commenting(comment):
	add_comment(comment)
	clear_comment_area()
	add_comment(comment)
	time.sleep(1)
	submit_comment()


def clear_comment_area():
	# find comment area and clear it
	commentTextAreaXpath = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea'
	WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, commentTextAreaXpath)))
	comment_area = browser.find_element_by_xpath(commentTextAreaXpath)
	comment_area.send_keys(Keys.CONTROL + "a")
	comment_area.send_keys(Keys.DELETE)


try:
	# 1 for login 0 for open
	loginOpen = -1
	get_arguments()
	for opt, arg in opts:
		if opt == '-u':
			username = arg
		elif opt == '-p':
			password = arg
		elif opt == '-g':
			postURL = arg
		elif opt == '-o':
			loginOpen = 0
		elif opt == '-l':
			loginOpen = 1
	if loginOpen == 0:
		open_insta()
		find_post(postURL)
		while True:
			print(comments)
			try:
				commentFlag = True
				commenting(get_random_names())
				comments += 1
				pass
			except ElementNotInteractableException:
				comments -= 1
				exit_post()
				time.sleep(commentBlock)
				find_post(postURL)
				pass
			time.sleep(random.randint(secondRangeStart, secondRangeEnd))
	elif loginOpen == 1:
		logging_in()
	else:
		print("Give option")

except TimeoutException:
	print('Loading took too much time!')
