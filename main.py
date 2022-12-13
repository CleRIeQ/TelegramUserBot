import time
from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import PeerFlood
from config import api_id, api_hash, bot_token
from pyrogram.raw.types import InputGeoPoint
from pyrogram.raw import functions
import asyncio
from db_routine import *


app = Client("my_bot", api_id, api_hash, bot_token)
app2 = Client("account", api_id, api_hash)

it_ran = False

COMMANDS = """Список команд:

!команды - это сообщение;

!рассылка - начать отправку сообщений людям;

!очистка - очистить базу данных, позволить боту отправлять сообщения тем людям, кому уже отправляли."""
		

async def send_m(from_user):
	global it_ran
	if not it_ran:
		it_ran = True
	else:
		await app2.stop()
	messages_count = 0
	c = InputGeoPoint(lat=55.165433, long=61.431765)
	async with app2:
		members = await app2.invoke(
			functions.contacts.GetLocated(geo_point=c)
		)
		for member in members.users:
			if member.username is not None:
				try:
					if check_is_new(member.username) is None:
						if messages_count >= 20:
							await app.send_message(from_user, f"Было отправлено {messages_count} сообщений")
							return 0
						add_new_user(member.username)
						await app2.send_message(member.username, """Приветствую! """)
						messages_count += 1
						time.sleep(20)
					else:
						print("skip")

				except PeerFlood:
					try:
						await app.send_message(from_user, "Получен мут за флуд")
						await app.send_message(from_user, f"Было отправлено {messages_count} сообщений")
					except Exception as e:
						print(repr(e))


@app.on_message()
async def main(client, message):
	from_user = message.chat.username

	if message.text.lower() == "/Start":
		await app.send_message(from_user, COMMANDS)
	if message.text.lower() == "!команды":
		await app.send_message(from_user, COMMANDS)
	if message.text.lower() == "!рассылка":
		await send_m(from_user)
	if message.text.lower() == "!очистка":
		delete_all_rows()
		await app.send_message(from_user, "Очищено..")

app.run()

