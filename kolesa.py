import urllib.request
from bs4 import BeautifulSoup

import requests


#url = "https://api.telegram.org/bot500967450:AAEnql1rqEnw7MtpvujpR07bDvxwAVfl4_g/"

BASE_URL = 'https://kolesa.kz/cars/toyota/almaty/?price[from]=7+000+000&price[to]=15+000+000'



def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse(html):
    soup = BeautifulSoup(html,"lxml")
    titles = []
    prices = []
    Desc = []
    urls = []
    table = soup.find('div', class_='result-block col-sm-8')
    k=0
    for row in table.find_all('div',class_='a-info-side col-right-list'):

        imena = row.find_all('span', class_='a-el-info-title')

        prices = row.find_all('span', class_='price')

        Desc = row.find_all('div', class_='desc')

        urls = row.find_all('a', class_='list-link')


        first = prices[0].text.split()[0]
        second = first + " " + prices[0].text.split()[1]
        third = second + " " + prices[0].text.split()[2]

        if prices[0].text.split()[2] != "₸":

        	third = third + " " + prices[0].text.split()[3]

        titles.append({
            'title': imena[0].a.text,
            'цена': third,  
            'Описание': Desc[0].text,
            'Ссылка' :"https://kolesa.kz"+urls[0].get('href')+"/"
        })
        k = k + 1
    
    return titles


def text_to_mess(titles):

    text_of_message = []

    text_of_message.append((titles[0]['title']+"kek", titles[0]['цена']+"kek", titles[0]['Описание']+"kek", titles[0]['Ссылка']))

    text = str(text_of_message)    
    
    return text

def models(text):

	if text.lower().find("audi") == -1 and text.lower().find("bmw") ==-1 and text.lower().find("merc") == -1 and text.lower().find("porsche") == -1  and text.lower().find("lexus") == -1 and text.lower().find("toyota") == -1:

		return False

	else:
		return True


def geturl(titles):

	text = titles[0]['Ссылка']

	textt = text.replace(" ","")

	return textt

def cheaper(html):

	soup = BeautifulSoup(html,"lxml")

	if soup.find('span',class_='kolesa-score-label cheaper') != None:
		return True

	return False


def getpercentage(html):

	soup = BeautifulSoup(html,"lxml")

	percentage = soup.find('span',class_='kolesa-score-label cheaper')

	percent = percentage.text.split("%")[0]

	percent.replace(" ","")

	return percent



def beautify_the_text(string):

	text = string.replace("(","",1)

	text = text.replace(")","")

	text = text.replace("\\xa0г.","г. ")

	text = text.replace("kek","\n")

	text = text.replace("  ","")

	text = text.replace("\\n","")

	text = text.replace("'","")

	text = text.replace(",","")

	text = text.replace("[","")

	text = text.replace("]","")
	
	return text


class BotHandler:
	
	def __init__(self,token):
		self.token = token
		self.api_url = "https://api.telegram.org/bot{}/".format(token)

	def get_updates(self, offset=None, timeout=30):
		method = 'getUpdates'
		params = {'timeout': timeout, 'offset': offset}
		resp = requests.get(self.api_url + method, params)
		result_json = resp.json()['result']
		return result_json

	def send_message(self, chat_id, text):
		params = {'chat_id': chat_id, 'text': text}
		method = 'sendMessage'
		resp = requests.post(self.api_url + method, params)
		return resp

	def get_last_update(self):

		get_result = self.get_updates()

		if len(get_result) > 0:
			last_update = get_result[-1]
		else:
			last_update = None
	
		return last_update


token = '560432515:AAE6D_Hugs5ZN0cuCc_dl_xQnh_ESOV6HRI'
krisha_bot = BotHandler(token)  

command1 = '/start'
command2 = '/help' 
command3 = '/аренда'
command4 = '/продажа'
command5 = '/re'
def main():
	lasttext = ""
	new_offset = None
	while True:
		try:
			krisha_bot.get_updates(new_offset)			
			last_update = krisha_bot.get_last_update()

			if isinstance(last_update, list):
				last_update_id = last_update_id[-1]['update_id']

			elif last_update == None:
				continue

			else:
				last_update_id = last_update['update_id']

			last_chat_text = last_update['message']['text']
			last_chat_id = last_update['message']['chat']['id']
			last_chat_name = last_update['message']['chat']['first_name']
	        


			whole = []	
	                                
			whole = parse(get_html(BASE_URL))

			cheap = False

			if cheaper(get_html(geturl(whole))) == True:

				percentt = getpercentage(get_html(geturl(whole)))

				percentt = percentt.replace("на ","")

				if float(percentt) >= 0 and models(text_to_mess(whole)) == True:
					cheap = True


			if lasttext != beautify_the_text(text_to_mess(whole)) and cheap == True :
				last_chat_id = '400757313'
				krisha_bot.send_message(last_chat_id, beautify_the_text(text_to_mess(whole)))
				krisha_bot.send_message(last_chat_id, percentt+"%")
				lasttext = beautify_the_text(text_to_mess(whole))
				last_chat_id = '497431011'	
				krisha_bot.send_message(last_chat_id, beautify_the_text(text_to_mess(whole)))
				krisha_bot.send_message(last_chat_id, percentt+"%")
				lasttext = beautify_the_text(text_to_mess(whole))
			

		except urllib.error.HTTPError:
			continue


if __name__ == '__main__':  
	try:
		main()
	except KeyboardInterrupt:
		exit()
    
