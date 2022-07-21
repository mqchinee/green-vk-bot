from vkbottle import API
from vkbottle.bot import Bot, Message, rules
import random
import bs4, requests
from bs4 import BeautifulSoup
import sys
import wikipedia
import json
import aiomojang
import asyncio
import sqlite3
import time
from threading import Thread
import schedule
from simpledemotivators import Demotivator, Quote
from vkbottle import PhotoMessageUploader
import os
import io
from io import BytesIO
import contextlib
from aioconsole import aexec
from utils import http
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import urllib.request, urllib.parse, re
import fandom

def main_loop():
	thread = Thread(target=do_schedule)
	thread.start()

def NAME():
	db = sqlite3.connect('data.db')
	cursor = db.cursor()
	cursor.execute("UPDATE botdata SET cooldown = ? WHERE cooldown = ?", (0, 1))
	db.commit()
	cursor.close()
	db.close()
	print('Очистили КД!')

def do_schedule():
	schedule.every().day.at("23:00").do(NAME)
	while True:
		schedule.run_pending()
		time.sleep(1)

wikipedia.set_lang("RU")

bot = Bot(token="ur token")
bot.labeler.vbml_ignore_case = True
watermark = 'Гринмашин'
arrange = True
groupid = 213174308

bot.labeler.message_view.replace_mention = True

meeting = "Привет, поздравляю с вступлением в беседу!"

dir_to_txt = 'Genb/id'

@bot.on.chat_message(text=".писюн")
async def chat_game_handler(message: Message):
	user = await bot.api.users.get(message.from_id)
	db = sqlite3.connect('data.db')
	cursor = db.cursor()
	pom1 = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3]
	pom = random.choice(pom1)
	cursor.execute("SELECT user FROM botdata WHERE id = ? AND user = ?", (message.peer_id, user[0].id,))
	data = cursor.fetchone()
	cursor.execute("SELECT cm FROM botdata WHERE id = ? AND user = ?", (message.peer_id, user[0].id,))
	data3 = cursor.fetchone()
	cursor.execute("SELECT cooldown FROM botdata WHERE id = ? AND user = ?", (message.peer_id, user[0].id,))
	data4 = cursor.fetchone()
	amount = 0
	start = random.randint(1,25)
	startm = random.randint(3,20)
	startmega = random.randint(50,120)
	if data is None:
		cursor.execute("INSERT INTO botdata(cm, cooldown, id, user) VALUES(?,?,?,?)", (start, 1, message.peer_id, user[0].id,))
		await message.reply(f"Козаче, твоя піська отримала початковий ріст в {start} см! Бажаю тобі успіхів!")
	elif data3[0] < amount:
		cursor.execute("DELETE FROM botdata WHERE id = ? AND user = ?", (message.peer_id, user[0].id,))
		await message.reply(f"Козаче, твоя піська відвалилася :(")
	else:
		if data4[0] == 1:
			await message.reply(f'@id{user[0].id} ({user[0].first_name}), ти вже грав сьогодні!\n(Кожен день в 7:00 (GMT+3) весь кулдаун очищається!)')
		elif data4[0] == 0:
			if pom == 1:
				cursor.execute("SELECT cm FROM botdata WHERE id = ? AND user = ?", (message.peer_id, user[0].id,))
				data1 = cursor.fetchone()
				cursor.execute(f"UPDATE botdata SET cm = cm + {start} WHERE id = ? AND user = ?", (message.peer_id, user[0].id,))
				await message.reply(f"Козаче, твоя піська вирісла на {start} см. Так тримати!")
				cursor.execute(f"UPDATE botdata SET cooldown = ? WHERE id = ? AND user = ?", (1, message.peer_id, user[0].id,))
			elif pom == 2: 
				cursor.execute("SELECT cm FROM botdata WHERE id = ? AND user = ?", (message.peer_id, user[0].id,))
				data1 = cursor.fetchone()
				cursor.execute(f"UPDATE botdata SET cm = cm - {startm} WHERE id = ? AND user = ?", (message.peer_id, user[0].id,))
				await message.reply(f"Козаче, твоя піська зменшилася на {startm} см. Бідненький!")
				cursor.execute(f"UPDATE botdata SET cooldown = ? WHERE id = ? AND user = ?", (1, message.peer_id, user[0].id,))
			elif pom == 3:
				cursor.execute("SELECT cm FROM botdata WHERE id = ? AND user = ?", (message.peer_id, user[0].id,))
				data1 = cursor.fetchone()
				cursor.execute(f"UPDATE botdata SET cm = cm + {startmega} WHERE id = ? AND user = ?", (message.peer_id, user[0].id,))
				await message.reply(f"КОЗАЧЕ, ТИ ОТРИМАВ МЕГА-РІСТ! Твоя піська виросла на {startmega} см.")
				cursor.execute(f"UPDATE botdata SET cooldown = ? WHERE id = ? AND user = ?", (1, message.peer_id, user[0].id,))

	db.commit()
	cursor.close()
	db.close()

@bot.on.chat_message(text=".мой_писюн")
async def chat_game_handler2(message: Message):
	user = await bot.api.users.get(message.from_id)
	db = sqlite3.connect('data.db')
	cursor = db.cursor()
	cursor.execute("SELECT cm FROM botdata WHERE id = ? AND user = ?", (message.peer_id, user[0].id,))
	data = cursor.fetchone()
	start = random.randint(0,15)
	if data is None:
		await message.reply(f"Козаче, в тебе нема піськи! Напиши .писюн, щоб виправити цю помилку!")
	else:
		await message.reply(f"Козаче, твоя піська має розмір {str(data[0])} см!")
	db.commit()
	cursor.close()
	db.close()

@bot.on.chat_message(text=".топ")
async def chat_game_handler24(message: Message):
	top = []
	db = sqlite3.connect('data.db')
	cursor = db.cursor()
	counter = 1
	for row in cursor.execute("SELECT user, id, cm FROM botdata WHERE id = ? ORDER BY cm DESC LIMIT 30", (message.peer_id,)):
		user2 = await bot.api.users.get(row[0])
		top.append(f"#{counter} {user2[0].first_name} {user2[0].last_name} - {row[2]} см.\n")
		query = "".join(top)
		counter += 1
	await message.reply(f"Топ 30 игроков!\n\n{query}")
	db.commit()
	cursor.close()
	db.close()

@bot.on.chat_message(mention=True)
async def mention_handler(message: Message):
	user = await bot.api.users.get(message.from_id)
	await message.reply(f"@id{user[0].id} ({user[0].first_name}), для вывода списка команд - .помощь")

@bot.on.chat_message(text=[".test",".тест"])
async def chat_message_handler(message: Message):
	user = await bot.api.users.get(message.from_id)
	if user[0].id == 567447984:
		await message.reply(f"@id{user[0].id} ({user[0].first_name}). Hello, World! Command: {message.text}")
	else:
		await message.reply(f"@id{user[0].id} ({user[0].first_name}), вы не разработчик!")

@bot.on.chat_message(text=[".скажи <text>",".скажи"])
async def chat_message_handler(message: Message, text=None):
	user = await bot.api.users.get(message.from_id)
	if user[0].id == 567447984:
		if text is not None:
			await message.answer(f"{text}")
	else:
		await message.reply(f"@id{user[0].id} ({user[0].first_name}), вы не разработчик!")

@bot.on.chat_message(text=[".ролл",".roll"])
async def e8ball2(message: Message):
	user = await bot.api.users.get(message.from_id)
	await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}) бросил(а) кости.\n🎲 Выпало: {random.randint(1,6)}!")

@bot.on.chat_message(text=[".шар <question>",".шар"])
async def e8ball(message: Message, question=None):
	user = await bot.api.users.get(message.from_id)
	choice = ['Я вижу... да! ✅','Я вижу... нет! 🚫','Лучше не говорить сейчас об этом. ❓','Мой ответ - нет. 🚫','Не могу сейчас предсказать.. ❓','Не зацикливайся на этом. ❓','Попробуй снова! ❓','Мои источники говорят нет! 🚫','Конечно! ✅','Вероятнее всего - да! ✅','Да. ✅','Моё мнение - да! ✅','Скорее всего - нет. 🚫','Даже не думай! 🚫']
	if question is not None:
		await message.reply(f"🔮 Магический шар! 🔮\n@id{user[0].id} ({user[0].first_name}), твой вопрос: \n{question}\n\nМой ответ:\n{random.choice(choice)}")
	else:
		await message.reply(f"@id{user[0].id} ({user[0].first_name}), вы не указали вопрос!")

@bot.on.chat_message(text=[".совместимость <question>",".совместимость"])
async def e8ball3(message: Message, question=None):
	user = await bot.api.users.get(message.from_id)
	if question is not None:
		await message.reply(f"💞 @id{user[0].id} ({user[0].first_name}), ты совместим(а) с {question} на {random.randint(0, 100)}%")
	else:
		await message.reply(f"@id{user[0].id} ({user[0].first_name}), вы не указали аргумент!")

@bot.on.chat_message(text=[".насколько <question>",".насколько"])
async def e8ball3434(message: Message, question=None):
	user = await bot.api.users.get(message.from_id)
	if question is not None:
		if question.startswith('-'):
			await message.reply(f"🎲 {question[1:100000]} на {random.randint(0, 101)}%")
		else:
			await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), ты {question} на {random.randint(0, 101)}%")		
	else:
		await message.reply(f"@id{user[0].id} ({user[0].first_name}), вы не указали аргумент!")

@bot.on.chat_message(text=[".вики <question>",".вики"])
async def e8ball3342(message: Message, question=None):
	user = await bot.api.users.get(message.from_id)
	idlist = [585988117, 447956362] # 447956362
	if user[0].id in idlist:
		await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), тебе нельзя использовать эту команду.\nОшибка? Обратись к @mqchinee")
	else:
		if question is not None:
			try:
				query = "".join(question)
				searchs = wikipedia.search(query,results = 1)
				page = wikipedia.page(searchs)
				await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), вот что я нашел по твоему запросу:\n\n{str(wikipedia.summary(query)[:1000])}. . .\n\nТвой запрос: {question}\nЧитать дальше: {page.url}")
			except wikipedia.exceptions.DisambiguationError:
				await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), слишком много страниц по твоему запросу. Может конкретнее?")
			except wikipedia.exceptions.PageError:
				await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), ничего не найдено.")
			except wikipedia.exceptions.WikipediaException:
				await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), неизвестная ошибка, попробуй позже.")
			except requests.exceptions.ProxyError:
				await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), соединение оборвалось, попробуй позже.")
		else:
			await message.reply(f"@id{user[0].id} ({user[0].first_name}), вы не указали аргумент!")

@bot.on.chat_message(text=[".помощь <page>",".помощь"])
async def e8ball1(message: Message, page=None):
	user = await bot.api.users.get(message.from_id)
	if page is None:
		await message.reply(f"❗ Укажите страницу! Например: .помощь 1\nВсего страниц: [5]\n\n🚫 Версия: 1.2.1 🚫")
	elif page == "1":
		await message.reply(f"🔮 Меню помощи [1/5]:\n\nОбычные команды:\n❗ .шар [ваш_вопрос] - отвечу вам на любой ваш вопрос!\n❗ .ролл - бросить кости.\n❗ .анекдот - случайный анекдот для вас! (источник: http://rzhunemogu.ru/)\n❗ .разраб - мой разработчик.\n❗ .совместимость [аргумент] - проверяю твою совместимость!\n❗ .вики [запрос] - найду для вас статью в Wikipedia\n❗ .ник [ник] - найду информацию о лицензии Minecraft\n❗ .насколько [аргумент] или [-аргумент (без приставки 'ты')] - узнать, на сколько процентов ты (твой аргумент).\n❗ .covid [страна_eng] - статистика covid-19 для выбранной страны.\n❗ .yt [запрос] - найду видео по вашему запросу (YouTube).\n❗ .майнвики [запрос] - найду для вас статью в Fandom (Minecraft)")
	elif page == "2":
		await message.reply(f"🔮 Меню помощи [2/5]:\n\nДля разработчиков:\n❗ .скажи - повторю твоё сообщение.\n❗ .ddb - принудительно очистить базу генератора текущей беседы.\n❗ .аген_вкл - принудительно включить генератор\n❗ .аген_выкл - принудительно выключить генератор\n❗ .ghoul - я только прошу, не забывай меня...\n❗ .eval [код] - запущу код.")
	elif page == "3":
		await message.reply(f"🔮 Меню помощи [3/5]:\n\nИгровые команды (українською, для фана :D)\n❗ .писюн - главная команда игры\n❗ .мой_писюн - твоя статистика\n❗ .топ - топ игроков (30)\nПримечание:\nКаждый день в 7:00 (GMT+3) кулдаун очищается у всех!")
	elif page == "4":
		await message.reply(f"🔮 Меню помощи [4/5]:\n\nРабота с картинками: \n❗ .дем [текст1]\n[текст 2] - создать демотиватор. (вы можете прикрепить фотографию, либо ответить на сообщение с фотографией)\n❗ .ц - создать цитату. (нужно ответить на сообщение, которое вы хотите процитировать)\n\nПримечание: Если бот не отправляет картинку, попробуй процитировать сообщение бота, тогда всё заработает!\n\nПрочее:\n❗ .cat\n❗ .duck \n❗ .wanted\n❗ .wtf \n❗ .rip (текст)\n❗ .fire")
	elif page == "5":
		await message.reply(f"🔮 Меню помощи [5/5]:\n\nГенератор случайных слов/фраз:\n❗ .вайп - очистить базу данных\n❗ .инфо - узнать, сколько сохранено слов\n❗ .ген_вкл - включить генератор\n❗ .ген_выкл - выключить генератор\n\nПримечание: бот сохраняет ваши сообщения в беседе, иногда отправляет их, составляя из них фразы. Помогает поднять актив в беседе.")
	else:
		await message.reply(f"❗ Такой страницы нет, укажите страницу! Например: .помощь 1\nВсего страниц: [5]\n\n🚫 Версия: 1.2.1 🚫")

@bot.on.chat_message(text=[".анекдот",".смешнява"])
async def e8ball11(message: Message):
	user = await bot.api.users.get(message.from_id)
	response = requests.get('http://rzhunemogu.ru/')
	soup = BeautifulSoup(response.text, 'html.parser')
	text = soup.find(id='ctl00_ContentPlaceHolder1_Accordion1_Pane_0_content_LabelText').getText()
	try:
		await message.reply(f"😀 @id{user[0].id} ({user[0].first_name}), случайный анекдот для тебя:\n\n----*\n{text}\n*----")
	except requests.exceptions.ProxyError:
		await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), соединение оборвалось, попробуй позже.")

@bot.on.chat_message(text=[".разраб",".разработчик"])
async def e8ball1244(message: Message):
	user = await bot.api.users.get(message.from_id)
	await message.reply(f"🎲 Мой разработчик:\n@mqchinee (Никита Лесной)!")

@bot.on.chat_message(text=[".ник <question>",".ник"])
async def e8ball35(message: Message, question=None):
	user = await bot.api.users.get(message.from_id)
	player = question
	if question is not None:
		try:
			profile = aiomojang.Player(player)
			skin = aiomojang.Skin(player)
			nicks = []
			i = 1 
			for x in await profile.get_history():
				nicks.append(f"Имя #{i}: {x['name']}\n")
				i = i + 1
			names = "".join(nicks)
			await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), вот что я нашел по запросу {player}:\n\nНикнейм: {await aiomojang.Player(await profile.uuid).name}\n\nUUID: {await profile.uuid}\nSKIN: {await skin.url}\nИстория никнеймов:\n {str(names)}")
		except aiomojang.exceptions.ApiException:
			await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), ничего не найдено.")

	else:
		await message.reply(f"@id{user[0].id} ({user[0].first_name}), вы не указали аргумент!")


@bot.on.message(text=['.дем <text1>\n<text2>', '.демотиватор <text1>\n<text2>', '.dem <text1>\n<text2>'])
async def dem(ans: Message, text1=None, text2=None):
	try:
		if text1 and text2 == None:
			ans.reply("Укажите текст.")
		else:
			if ans.reply_message is not None:

				if ans.reply_message.attachments:
					image_url = ans.reply_message.attachments[0].photo.sizes[-5].url
					img_data = requests.get(image_url).content
					with open('demimg.jpg', 'wb') as handler:
						handler.write(img_data)
					dem = Demotivator(text1, text2)
					dem.create('demimg.jpg', arrange=arrange)
					photo_upd = PhotoMessageUploader(bot.api)
					photo = await photo_upd.upload("demresult.jpg")
					await ans.reply('Вот твоё фото:', attachment=photo)

			elif ans.attachments is not None:
				image_url = ans.attachments[0].photo.sizes[-5].url
				img_data = requests.get(image_url).content
				with open('demimg.jpg', 'wb') as handler:
					handler.write(img_data)
				dem = Demotivator(text1, text2)
				dem.create('demimg.jpg', arrange=arrange)
				photo_upd = PhotoMessageUploader(bot.api)
				photo = await photo_upd.upload("demresult.jpg")
				await ans.reply('Вот твоё фото:', attachment=photo)
	except IndexError:
		await ans.reply('Вы не прикрепили изображение')

@bot.on.message(text='.ц')
async def quote(ans: Message):
	try:
		group_id = ans.reply_message.from_id
		user_ava = await bot.api.users.get(user_ids=ans.reply_message.from_id, fields='photo_max')
		user_photo = user_ava[0].photo_max
		name = user_ava[0].first_name + ' ' + user_ava[0].last_name
		img_data = requests.get(user_photo).content
		with open('userphoto.jpg', 'wb') as handler:
			handler.write(img_data)
		dem = Quote(ans.reply_message.text, name)
		photo = dem.create(user_photo, use_url=True, quote_text_size=45)
		photo_upd = PhotoMessageUploader(bot.api)
		photo = await photo_upd.upload("qresult.png")
		await ans.reply("", attachment=photo)
	except:
		group_id = ans.reply_message.from_id * (-1)
		user_ava = await bot.api.groups.get_by_id(group_id=group_id)
		user_photo = user_ava[0].photo_200
		name = user_ava[0].name
		img_data = requests.get(user_photo).content
		with open('userphoto.jpg', 'wb') as handler:
			handler.write(img_data)
		dem = Quote(ans.reply_message.text, name)
		photo = dem.create(user_photo, use_url=True, quote_text_size=45, headline_text='Цитаты великих ботов')
		photo_upd = PhotoMessageUploader(bot.api)
		photo = await photo_upd.upload("qresult.png")
		await ans.reply("", attachment=photo)

async def check(ans, id: int) -> bool:
	items = (await bot.api.messages.get_conversations_by_id(peer_ids=ans.peer_id)).items
	if not items:
		return False
	chat_settings = items[0].chat_settings
	admins = []
	admins.extend(chat_settings.admin_ids)
	admins.append(chat_settings.owner_id)
	return id in admins

async def addtobd(peerid):
	if not os.path.exists(dir_to_txt + str(peerid) + '.txt'):
		f = open(dir_to_txt + str(peerid) + '.txt', 'w', encoding='utf8')
		f.write('')
		f.close()

@bot.on.chat_message(rules.ChatActionRule('chat_invite_user'))
async def on_bot_invite(ans: Message):
	await addtobd(ans.peer_id)
	await ans.answer(meeting)

@bot.on.chat_message(text=['.ddb'])
async def adddbd(ans: Message):
	user = await bot.api.users.get(ans.from_id)
	if user[0].id == 567447984:
		await addtobd(ans.peer_id)
		await ans.reply(f"@mqchinee (Господин), вы добавили этой беседе базу диалогов! dialogs{str(ans.peer_id)}.txt")
	else:
		await ans.reply(f"@id{user[0].id} ({user[0].first_name}), вы не разработчик!")

@bot.on.chat_message(text=['.info', '.инфо'])
async def info(ans: Message):
	await addtobd(ans.peer_id)
	with open(dir_to_txt + str(ans.peer_id) + '.txt', encoding="utf8") as file:
		txt = file.read().split(",")
	await ans.reply(f'Сохранил слов: {len(txt)}')

@bot.on.chat_message(text=['.вайп'])
async def wipe(ans: Message):
	await addtobd(ans.peer_id)
	if not await check(ans, id=ans.from_id):
		await ans.reply('Вы не администратор беседы')
	else:
		f = open(dir_to_txt + str(ans.peer_id) + '.txt', 'w', encoding='utf8')
		f.write('')
		f.close()
		await ans.reply('База была успешно очищена.')

@bot.on.chat_message(text=['.ген_вкл'])
async def wipeon(message: Message):
	if not await check(message, id=message.from_id):
		await message.reply('Вы не администратор беседы')
	else:
		db = sqlite3.connect('status.db')
		cursor = db.cursor()
		cursor.execute("SELECT status FROM onoff WHERE id = ?", (message.peer_id,))
		data = cursor.fetchone()
		if data is None:
			cursor.execute("INSERT INTO onoff(status, id) VALUES(?,?)", (1, message.peer_id,))
			await message.reply("Вы включили генератор.")
		elif data[0] == 0:
			cursor.execute("UPDATE onoff SET status = ? WHERE id = ?", (1, message.peer_id,))
			await message.reply("Вы включили генератор.")
		elif data[0] == 1:
			await message.reply("Генератор уже включен.")
		db.commit()
		cursor.close()
		db.close()

@bot.on.chat_message(text=['.ген_выкл'])
async def wipeoff(message: Message):
	if not await check(message, id=message.from_id):
		await message.reply('Вы не администратор беседы')
	else:
		db = sqlite3.connect('status.db')
		cursor = db.cursor()
		cursor.execute("SELECT status FROM onoff WHERE id = ?", (message.peer_id,))
		data = cursor.fetchone()
		if data is None:
			cursor.execute("INSERT INTO onoff(status, id) VALUES(?,?)", (0, message.peer_id,))
			await message.reply("Вы выключили генератор.")
		elif data[0] == 1:
			cursor.execute("UPDATE onoff SET status = ? WHERE id = ?", (0, message.peer_id,))
			await message.reply("Вы выключили генератор.")
		elif data[0] == 0:
			await message.reply("Генератор уже выключен.")
		db.commit()
		cursor.close()
		db.close()

@bot.on.chat_message(text=['.аген_вкл'])
async def wipeon1(message: Message):
	user = await bot.api.users.get(message.from_id)
	if user[0].id == 567447984:
		db = sqlite3.connect('status.db')
		cursor = db.cursor()
		cursor.execute("SELECT status FROM onoff WHERE id = ?", (message.peer_id,))
		data = cursor.fetchone()
		if data is None:
			cursor.execute("INSERT INTO onoff(status, id) VALUES(?,?)", (1, message.peer_id,))
			await message.reply("Вы включили генератор.")
		elif data[0] == 0:
			cursor.execute("UPDATE onoff SET status = ? WHERE id = ?", (1, message.peer_id,))
			await message.reply("Вы включили генератор.")
		elif data[0] == 1:
			await message.reply("Генератор уже включен.")
		db.commit()
		cursor.close()
		db.close()
	else:
		await message.reply(f"@id{user[0].id} ({user[0].first_name}), вы не разработчик!")

@bot.on.chat_message(text=['.аген_выкл'])
async def wipeoff1(message: Message):
	user = await bot.api.users.get(message.from_id)
	if user[0].id == 567447984:
		db = sqlite3.connect('status.db')
		cursor = db.cursor()
		cursor.execute("SELECT status FROM onoff WHERE id = ?", (message.peer_id,))
		data = cursor.fetchone()
		if data is None:
			cursor.execute("INSERT INTO onoff(status, id) VALUES(?,?)", (0, message.peer_id,))
			await message.reply("Вы выключили генератор.")
		elif data[0] == 1:
			cursor.execute("UPDATE onoff SET status = ? WHERE id = ?", (0, message.peer_id,))
			await message.reply("Вы выключили генератор.")
		elif data[0] == 0:
			await message.reply("Генератор уже выключен.")
		db.commit()
		cursor.close()
		db.close()
	else:
		await message.reply(f"@id{user[0].id} ({user[0].first_name}), вы не разработчик!")

@bot.on.chat_message(text=['.eval <code>', '.eval'])
async def evl(ans: Message, code=None):
	user = await bot.api.users.get(ans.from_id)
	if user[0].id == 567447984:
		if code is not None:
			str_obj = io.StringIO() #Retrieves a stream of data
			try:
				with contextlib.redirect_stdout(str_obj):
					await aexec(code)
			except Exception as e:
				await ans.reply(f"{e.__class__.__name__}: {e}")
			if not str_obj.getvalue():
				await ans.reply(f'Команда выполнена, сообщений нет!')
			else:
				await ans.reply(f'{str_obj.getvalue()}')
		else:
			await ans.reply(f'Укажите аргумент.')
	else:
		await ans.reply(f"@id{user[0].id} ({user[0].first_name}), вы не разработчик!")

@bot.on.chat_message(text=".ghoul")
async def ghoul(ans: Message):
	user = await bot.api.users.get(ans.from_id)
	if user[0].id == 567447984:
		await ans.answer('Скажи теперь')
		await asyncio.sleep(1)
		await ans.answer('Скажи мне точно')
		await asyncio.sleep(2)
		await ans.answer('Как всё это понять?')
		await asyncio.sleep(3)
		await ans.answer('Какой-то странный зверь')
		await asyncio.sleep(1)
		await ans.answer('Живёт внутри меня.')
		await asyncio.sleep(2)
		await ans.answer('Я уничтожен, уничтожен')
		await asyncio.sleep(2)
		await ans.answer('Есть лёд, но нет огня.')
		await asyncio.sleep(1)
		await ans.answer('И на исходе дня')
		await asyncio.sleep(1)
		await ans.answer('Твоей улыбки дверь.')
		await asyncio.sleep(3)
		await ans.answer('Иду вперёд я не спеша')
		await asyncio.sleep(1)
		await ans.answer('Мне тяжело дышать')
		await asyncio.sleep(1)
		await ans.answer('Не разрушай нет, не разрушай!')
		await asyncio.sleep(1)
		await ans.answer('После будет жаль..')
		await asyncio.sleep(1)
		await ans.answer('Стой!')
		await asyncio.sleep(1)
		await ans.answer('То сильный я, то слаб весьма')
		await asyncio.sleep(1)
		await ans.answer('Спокойный, но схожу с ума')
		await asyncio.sleep(1)
		await ans.answer('В смятении моя душа..')
		await asyncio.sleep(1)
		await ans.answer('Я здесь, я стою, я один в кругу порочном')
		await asyncio.sleep(2)
		await ans.answer('Душа пуста, мир вокруг непрочный.')
		await asyncio.sleep(1)
		await ans.answer('Не усложняй же и не ищи меня.')
		await asyncio.sleep(1)
		await ans.answer('Я знаю точно')
		await asyncio.sleep(1)
		await ans.answer('В придуманный мир я попал невольно')
		await asyncio.sleep(1)
		await ans.answer('Теперь не хочу тебе делать больно')
		await asyncio.sleep(1)
		await ans.answer('Но иногда ты вспоминай меня')
		await asyncio.sleep(1)
		await ans.answer('Таким, каким был я')
		await asyncio.sleep(1)
		await ans.answer('Я в одиночестве вплетён')
		await asyncio.sleep(1)
		await ans.answer('Как в странный и безумный сон')
		await asyncio.sleep(1)
		await ans.answer('И памяти больше нет')
		await asyncio.sleep(1)
		await ans.answer('Лишь только холодный бред')
		await asyncio.sleep(1)
		await ans.answer('Движенья нет!')
		await asyncio.sleep(1)
		await ans.answer('Движенья нет!')
		await asyncio.sleep(1)
		await ans.answer('Движенья нет!')
		await asyncio.sleep(1)
		await ans.answer('Движенья нет!')
		await asyncio.sleep(1)
		await ans.answer('Движенья нет!')
		await asyncio.sleep(1)
		await ans.answer('Движенья нет!')
		await asyncio.sleep(1)
		await ans.answer('И только бред!')
		await asyncio.sleep(3)
		await ans.answer('Я в мире невзрачном')
		await asyncio.sleep(1)
		await ans.answer('Нелепом прозрачном')
		await asyncio.sleep(1)
		await ans.answer('Я сам не свой, во мне другой')
		await asyncio.sleep(1)
		await ans.answer('Он мне чужой, но он со мной')
		await asyncio.sleep(1)
		await ans.answer('То сильный я, то слаб весьма')
		await asyncio.sleep(1)
		await ans.answer('Спокойный, но схожу с ума')
		await asyncio.sleep(1)
		await ans.answer('В смятении моя душа')
		await asyncio.sleep(3)
		await ans.answer('Только')
		await asyncio.sleep(1)
		await ans.answer('Я здесь, я стою, я один в кругу порочном')
		await asyncio.sleep(1)
		await ans.answer('Душа пуста, мир вокруг непрочный')
		await asyncio.sleep(1)
		await ans.answer('Не усложняй же и не ищи меня')
		await asyncio.sleep(1)
		await ans.answer('Я знаю точно')
		await asyncio.sleep(1)
		await ans.answer('В придуманный мир я попал невольно')
		await asyncio.sleep(1)
		await ans.answer('Теперь не хочу тебе делать больно')
		await asyncio.sleep(1)
		await ans.answer('Но иногда ты вспоминай меня')
		await asyncio.sleep(1)
		await ans.answer('Таким, каким был я..')
		await asyncio.sleep(3)
		await ans.answer('Ты только помни.')
		await asyncio.sleep(1)
		await ans.answer('Ты только помни.')
		await asyncio.sleep(1)
		await ans.answer('Ты только помни.')
		await asyncio.sleep(1)
		await ans.answer('Ты только помни.')
		await asyncio.sleep(1)
		await ans.answer('Прими то, что есть, что уже случилось')
		await asyncio.sleep(1)
		await ans.answer('И боготвори, что не изменилось')
		await asyncio.sleep(1)
		await ans.answer('Я только прошу, не забывай меня')
	else:
		await ans.reply(f"@id{user[0].id} ({user[0].first_name}), вы не разработчик!")

@bot.on.chat_message(text=[".covid <country>",".covid"])
async def covid(ans: Message, country=None):
	if country is not None:
		datas = []
		r = await http.get(f"https://disease.sh/v3/covid-19/countries/{country.lower()}", res_method="json")

		if "message" in r:
			await ans.reply(f"API отклонило запрос:\n{r['message']}")

		json_data = [
			("Случаев заражения", r["cases"]), ("Смертей", r["deaths"]),
			("Случаев выздоровления", r["recovered"]), ("Активных случаев", r["active"]),
			("Общее критическое состояние", r["critical"]), ("Случаев сегодня", r["todayCases"]),
			("Умерли сегодня", r["todayDeaths"]), ("Выздоровели сегодня", r["todayRecovered"])
		]

		for name, value in json_data:
			datas.append(f"{name}: {value:,}")
		query = " \n♻ -------- 💬\n".join(datas)

		await ans.reply(
			f"COVID-19: статистика {country.capitalize()}\n({r['countryInfo']['iso3']})\n\n{query}"
		)
	else:
		await ans.reply("Укажите аргумент.")

@bot.on.chat_message(text=[".wanted"])
async def wanted(ans: Message):
	wanted = Image.open("IMG/imagemanipulation2.jpg")
	user_ava = await bot.api.users.get(user_ids=ans.from_id, fields='photo_max')
	user_photo = user_ava[0].photo_max
	urllib.request.urlretrieve(f"{user_photo}", "IMG/vk-avatar.jpg")
	test = Image.open("IMG/vk-avatar.jpg")
	profilepic = test

	profilepic = profilepic.resize((423, 403))

	wanted.paste(profilepic, (98, 211))

	wanted.save("IMG/wantedpic.png")

	photo_upd = PhotoMessageUploader(bot.api)
	photo = await photo_upd.upload("IMG/wantedpic.png")
	await ans.reply("", attachment=photo)

@bot.on.chat_message(text=[".rip <text>",".rip"])
async def wanteddd(ans: Message, text=None):
	if text == None:
		rip = Image.open("IMG/manipulationcommand1.jpg")
		user_ava = await bot.api.users.get(user_ids=ans.from_id, fields='photo_max')
		user_photo = user_ava[0].photo_max
		urllib.request.urlretrieve(f"{user_photo}", "IMG/vk-avatar.jpg")
		test = Image.open("IMG/vk-avatar.jpg")
		profilepic = test
		profilepic = profilepic.resize((145, 139))
		rip.paste(profilepic, (108, 73))
		rip.save("IMG/rippic.png")
		photo_upd = PhotoMessageUploader(bot.api)
		photo = await photo_upd.upload("IMG/rippic.png")
		await ans.reply("", attachment=photo)
	else:
		rip = Image.open("IMG/manipulationcommand1.jpg")
		user_ava = await bot.api.users.get(user_ids=ans.from_id, fields='photo_max')
		user_photo = user_ava[0].photo_max
		urllib.request.urlretrieve(f"{user_photo}", "IMG/vk-avatar.jpg")
		test = Image.open("IMG/vk-avatar.jpg")
		profilepic = test
		profilepic = profilepic.resize((145, 139))
		idraw = ImageDraw.Draw(rip)
		headline = ImageFont.truetype('fonts/sans.otf', size = 12)
		idraw.text((97, 233), text, font = headline, fill="#000")
		rip.paste(profilepic, (108, 73))
		rip.save("IMG/rippictext.png")
		photo_upd = PhotoMessageUploader(bot.api)
		photo = await photo_upd.upload("IMG/rippictext.png")
		await ans.reply("", attachment=photo)

@bot.on.chat_message(text=[".fire"])
async def wanted1231(ans: Message):
	rip = Image.open("IMG/fire.jpg")

	user_ava = await bot.api.users.get(user_ids=ans.from_id, fields='photo_max')
	user_photo = user_ava[0].photo_max
	urllib.request.urlretrieve(f"{user_photo}", "IMG/vk-avatar.jpg")
	test = Image.open("IMG/vk-avatar.jpg")
	profilepic = test

	profilepic = profilepic.resize((228, 238))

	rip.paste(profilepic, (398, 98))

	rip.save("IMG/firepic.png")
	photo_upd = PhotoMessageUploader(bot.api)
	photo = await photo_upd.upload("IMG/firepic.png")

	await ans.reply("", attachment=photo)

@bot.on.chat_message(text=[".duck"])
async def wanted1233241(ans: Message):
	rip = Image.open("IMG/duck.jpg")

	user_ava = await bot.api.users.get(user_ids=ans.from_id, fields='photo_max')
	user_photo = user_ava[0].photo_max
	urllib.request.urlretrieve(f"{user_photo}", "IMG/vk-avatar.jpg")
	test = Image.open("IMG/vk-avatar.jpg")
	profilepic = test

	profilepic = profilepic.resize((389, 392))

	rip.paste(profilepic, (152, 101))

	rip.save("IMG/duckpic.png")
	photo_upd = PhotoMessageUploader(bot.api)
	photo = await photo_upd.upload("IMG/duckpic.png")

	await ans.reply("", attachment=photo)

@bot.on.chat_message(text=[".cat"])
async def wanted123323241(ans: Message):
	rip = Image.open("IMG/cat.jpg")

	user_ava = await bot.api.users.get(user_ids=ans.from_id, fields='photo_max')
	user_photo = user_ava[0].photo_max
	urllib.request.urlretrieve(f"{user_photo}", "IMG/vk-avatar.jpg")
	test = Image.open("IMG/vk-avatar.jpg")
	profilepic = test

	profilepic = profilepic.resize((498, 432))

	rip.paste(profilepic, (388, 262))

	rip.save("IMG/catpic.png")
	photo_upd = PhotoMessageUploader(bot.api)
	photo = await photo_upd.upload("IMG/catpic.png")

	await ans.reply("", attachment=photo)

@bot.on.chat_message(text=[".wtf"])
async def wanted1233243433241(ans: Message):
	rip = Image.open("IMG/wtf.png")

	user_ava = await bot.api.users.get(user_ids=ans.from_id, fields='photo_max')
	user_photo = user_ava[0].photo_max
	urllib.request.urlretrieve(f"{user_photo}", "IMG/vk-avatar.jpg")
	test = Image.open("IMG/vk-avatar.jpg")
	profilepic = test

	profilepic = profilepic.resize((339, 335))

	rip.paste(profilepic, (449, 232))

	rip.save("IMG/wtfpic.png")
	photo_upd = PhotoMessageUploader(bot.api)
	photo = await photo_upd.upload("IMG/wtfpic.png")

	await ans.reply("", attachment=photo)

@bot.on.chat_message(text=[".кмур"])
async def cmur(ans: Message):
	user = await bot.api.users.get(ans.from_id)
	idlist = [527269527]
	if user[0].id in idlist:
		await ans.reply('Кмур крутой!!!')
	else:
		await ans.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), ты не Кмур!")

@bot.on.chat_message(text=[".кто я на vc"]) #white - , rocksoft - , sasha_3345 - , niekorun - , teket4 - , volgare - , shemivet - , zxctrueinside - 
async def ktoya(ans: Message):
	user = await bot.api.users.get(ans.from_id)
	if user[0].id == 527269527:
		await ans.reply(f'@id{user[0].id} ({user[0].first_name}), ты cmur123')
	elif user[0].id == 567447984:
		await ans.reply(f'@id{user[0].id} ({user[0].first_name}), ты greenMachine1123')
	elif user[0].id == 271024044:
		await ans.reply(f'@id{user[0].id} ({user[0].first_name}), ты white (whitebelyash)')
	elif user[0].id == 471559882:
		await ans.reply(f'@id{user[0].id} ({user[0].first_name}), ты rocksoft')
	elif user[0].id == 447956362:
		await ans.reply(f'@id{user[0].id} ({user[0].first_name}), ты sasha_3345 (лох)')
	elif user[0].id == 694223618:
		await ans.reply(f'@id{user[0].id} ({user[0].first_name}), ты Niekorun')
	elif user[0].id == 303794271:
		await ans.reply(f'@id{user[0].id} ({user[0].first_name}), ты teket4')
	elif user[0].id == 259697642:
		await ans.reply(f'@id{user[0].id} ({user[0].first_name}), ты Volgare')
	elif user[0].id == 490661431:
		await ans.reply(f'@id{user[0].id} ({user[0].first_name}), ты Sheminet')
	elif user[0].id == 572971816:
		await ans.reply(f'@id{user[0].id} ({user[0].first_name}), ты zxctrueinside')
	else:
		await ans.reply(f"@id{user[0].id} ({user[0].first_name}), ты нн (я рил хз кто ты).")

@bot.on.chat_message(text=[".yt <word>",".yt"])
async def sayword(ans: Message, word=None):
	user = await bot.api.users.get(ans.from_id)
	if user[0].id != 490661431:
		if word is not None:
			query_string = urllib.parse.urlencode({
				"search_query": word
			})
			html_content = urllib.request.urlopen(
				"http://www.youtube.com/results?" + query_string
			)
			search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
			await ans.reply("http://www.youtube.com/watch?v=" + search_results[0])
		else:
			pass
	else:
		pass

@bot.on.message(text=[".майнвики <question>",".майнвики"])
async def e8ball3342(message: Message, question=None):
	user = await bot.api.users.get(message.from_id)
	fandom.set_wiki("Minecraft")
	fandom.set_lang("ru")
	if user[0].id != 490661431:
		if question is not None:
			try:
				query = fandom.page(question)
				title = query.title
				url = query.url
				summary = fandom.summary(f"{question}", "Minecraft", sentences=50)
				await message.reply(f"{title}\n\n{summary}. . .\n\nЧитать дальше:\n{url}")
			except:
				await message.reply(f"🎲 @id{user[0].id} ({user[0].first_name}), соединение оборвалось, попробуй позже.")
		else:
			await message.reply(f"@id{user[0].id} ({user[0].first_name}), вы не указали аргумент!")
	else:
		pass

@bot.on.chat_message()
async def chat_message(ans: Message):
	db = sqlite3.connect('status.db')
	cursor = db.cursor()
	cursor.execute("SELECT status FROM onoff WHERE id = ?", (ans.peer_id,))
	data = cursor.fetchone()
	if data[0] == 1:
		await addtobd(ans.peer_id)
		if len(ans.text) <= 60 and ans.text != '' and ans.from_id > 0 and ans.text[:3] != '[id' and ans.text[:1] != '!': # Проверяем на допустимое сообщение
			with open(dir_to_txt + str(ans.peer_id) + '.txt', "a", encoding="utf8") as f:
				f.write(ans.text + ",")
			with open(dir_to_txt + str(ans.peer_id) + '.txt', encoding="utf8") as file:
				txt = file.read().split(",")
			if len(txt) >= 4 and random.randint(0, 2) == 0:
				generator = random.choice(txt)
				message = generator
				if message == '':
					return "че"
				await ans.answer(message.lower())
	else:
		pass

if __name__ == '__main__':
	main_loop()
	print('Я жив!') 
	bot.run_forever()