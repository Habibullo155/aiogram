import asyncio
import os
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import find_dotenv, load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime


load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
url = ['https://allboxing.ru/boxing-news.html',
       'https://allboxing.ru/mma-news.html']


def send_add(_bot, message):
    return _bot.send_message(chat_id=message.chat.id,
                             text='Interested in buying advertising or creating a bot to suit your needs?: admins_link')


@dp.message(CommandStart())
async def say_hi(message: types.Message) ->None:
    if message.from_user.id == <user_id>:
        await bot.send_message(chat_id=message.chat.id, text='bot working')
        while True:
            i = 0
            j = 0
            hash_ = ['#box', '#mma']
            for j in range(2):
                hrefs = []
                list_of_hrefs = []
                get_request = requests.get(url=url[j]).content
                new_soup = BeautifulSoup(get_request, 'lxml')
                for div in new_soup.find_all('div', class_='news_element last'):
                    date_element = div.find('div', class_='news_element_date')
                    if int(date_element.text[:2]) == datetime.now().day:
                        a = div.find('a', class_='news_element_image', href=True)
                        href = ('https://allboxing.ru/' + a.get('href'))
                        list_of_hrefs.append(href)
                [hrefs.append(x) for x in list_of_hrefs if x not in hrefs]
                hrefs = hrefs[::-1]
                for i in range(len(hrefs)):
                    parsed_link = requests.get(hrefs[i]).content
                    soup_element = BeautifulSoup(parsed_link, 'lxml')
                    try:
                        content = soup_element.find('div',
                                                    class_='news_element main')
                        # find elements which need for scraping
                        content1 = soup_element.find('div', class_='news_element_description')
                        title = soup_element.find('h1', class_='news_element_title')
                        today_ = content.find('div', class_='news_element_date')
                        img = content.find('img', src=True)
                        img_result = img.get('src')
                        if int(today_.text[-5:-3]) >= datetime.now().hour - 5:
                            try:
                                content_edited = content1.text[1:900].split('.')[-1]
                                content_replaced = content1.text[1:900].replace(content_edited, '')
                                await bot.send_photo('-1001942224091', '{}'.format(img_result),
                                                     caption=f'<b>{title.text}</b> \n {content_replaced} \n {hash_[j]}',
                                                     parse_mode='html')
                            except:
                                img_ = content.find('a', class_='news_element_image', href=True)
                                img_result_ = img_.get('href')
                                content_edited = content1.text[1:900].split('.')[-1]
                                content_replaced = content1.text[1:900].replace(content_edited, '')
                                await bot.send_photo('chanel_id', '{}'.format(img_result_),
                                                     caption=f'<b>{title.text}</b> \n {content_replaced} \n {hash_[j]}',
                                                     parse_mode='html')
                            else:
                                pass
                        else:
                            pass
                    except:
                        pass
                    i += 1
                hrefs.clear()
                j += 1
            await asyncio.sleep(3600)

    else:
        send_add(_bot=bot, message=message)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
