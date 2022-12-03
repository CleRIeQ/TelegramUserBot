import time
from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import PeerFlood
from config import api_id, api_hash, bot_token

app = Client("my_bot", api_id, api_hash, bot_token)
app2 = Client("account", api_id, api_hash)


def get_members(name):
	members = app2.get_chat_members(name) #Получаем участников
	for member in members:
		member = member.user.username # Получаем username
		if member is not None: # Проверка на наличие username-а
			print(member)
			time.sleep(20)
			try:
				app2.send_message(member, "text") #Пишем сообщение участнику по его username
			except PeerFlood:
				print("Остановка за флуд... Отдохнем 20 минут")
				time.sleep(1200)
				continue

@app.on_message()
async def main(client, message):
	group_name = message.text #Название группы
	get_members(group_name)


app2.start() #Запускаем юзербота
app.run() #Включаем ожидание сообщения




#
#with Client("account", api_id, api_hash) as app:
#	app.send_message("vrednaya_deva", "Как жизнь?")