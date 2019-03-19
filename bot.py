import discord
import time
import asyncio
import random
import os
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import find
from discord.utils import get
from itertools import cycle


prefix = ["бот","Бот"]
Bot = commands.Bot(command_prefix= prefix)
Bot.remove_command('help')
status = ["Version: 1.4"]
#                   Масивы для чата
Miku = ["miku","мику","бота в студию",]
Mat = ["пидр","бляд","сука","ебать","хуй","пизд","ска","пздц","хуя","бля","ебал","курва",]
OffMat = ["Базар фильтруй {}, а то забаню))","Не матерись! Это плохо!"]
Ypom = ["Привет {}, как дела?","Ты звал меня {} ?","Прости {}, но у меня уже есть создатель 😓","こんにちは {0} !\nЯпонский:\"Привет {0} !\""]
SmailR_one = ["Мило))","Ваау","Мне нравится)", "А что так можно было ?"]
Smail_one = [":Msmail:",]
SmailR_two = ["Это страшно","Что-то не так {}?","Брутально))", "Не смотри на меня так"]
Smail_two = [":WOT:",]
Del = ["Удалено сообщений"]
#               Временно
Man= [":Orel:",":Reshka:"]
#Консоль запуска бота
@Bot.event
async def on_ready():
    print("Бот :",format(Bot.user.name))
    print("Версия ",format(Bot.user.name),": 1.3")
    print("Дата создания : 8.03.2019")
    print("Бот успешно запушен!")

@Bot.event
async def on_message(message):
    for i in Miku: #Призыв к рандомномму дружелюбному сообщению
        if i in message.content.lower():
            await Bot.send_message(message.channel,random.choice(Ypom).format(message.author.mention))
    for s in Smail_one: #Реакция на смайлик
        if s in message.content:
            await Bot.send_message(message.channel,random.choice(SmailR_one))
    for s in Smail_two: #Реакция на смайлик
        if s in message.content:
            await Bot.send_message(message.channel,random.choice(SmailR_two).format(message.author.mention))
    for b in Mat: #Фильтр мата
        if b in message.content.lower():
            await Bot.send_message(message.channel,random.choice(OffMat).format(message.author.mention))
            await Bot.delete_message(message)
    for c in Del: #Удаление "побочныйх" сообщений
        if c in message.content:
            time.sleep(5)
            await Bot.delete_message(message)
    #       Временно
    for s in Man: #Реакция на смайлик
        if s in message.content:
            await Bot.send_message(message.channel,"Кажется скоро будет игра) Но это не точно")

    await Bot.process_commands(message)
    
# Выдоча новым участникам роли Новичка
@Bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="👶 Новичек")
    await Bot.add_roles(member,role)
    
# Команда рандома
@Bot.command(pass_context=True)
async def рандом(ctx, one, two):
    try:
        one= int(one)
        two= int(two)
        arg = random.randint(one,two)
    except ValueError:
        await Bot.say("У нас так не принято, повтори нормально")
    else:
        await Bot.say("Твоё число: "+str(arg))
@рандом.error
async def рандом_error(ctx, error):
    await Bot.say("Ты забыл ввести число, повтори попытку")

#Выдача боту рандомного статуса
async def change_status():
    await Bot.wait_until_ready()
    msgs= cycle(status)

    while not Bot.is_closed:
        current_status = next(msgs)
        await Bot.change_presence(game=discord.Game(name=(current_status)))
        await asyncio.sleep(60)

#_____________________________ИЗУЧИТЬ http://qaru.site/questions/15101732/permission-system-for-discordpy-bot

#Тестовая комманда
@Bot.command(pass_context= True)
async def тест(ctx):
    await Bot.say("Привет {0} это тестовое сообщение,созданное для проверки работоспособности".format(ctx.message.author.mention))

# Подключение и Отключение бота от голосового чата
@Bot.command(pass_context=True)
async def сюда(ctx):
    channel = ctx.message.author.voice.voice_channel
    await Bot.join_voice_channel(channel)
@Bot.command(pass_context=True)
async def отсюда(ctx):
    server = ctx.message.server
    voise_channel = Bot.voice_client_in(server)
    await voise_channel.disconnect()

#Информация о пользователе
@Bot.command(pass_context= True)
async def инфо(ctx, user: discord.User):
    emb = discord.Embed(title= "Информация о пользователе:",color = 0x32cd32)
    emb.add_field(name="Имя", value= user.name) #add_field - заполнение каким-либо текстом(универсальнвя вешь)
    emb.add_field(name="Дата подключения",value=str(user.joined_at)[:16])
    if user.bot !=  False:
        emb.add_field(name="Бот",value= "Да")
    if user.game != None:
        emb.add_field(name="Игра", value= user.game)
    emb.add_field(name= "ID",value=user.id)
    emb.set_thumbnail(url= user.avatar_url)
    emb.set_author(name="Рассказывает "+Bot.user.name, url="https://discordapp.com/oauth2/authorize?&client_id=553538873825689600&scope=bot&permissions=8") #Научился вставлять ссылки в текст
    emb.set_footer(text="Все права защищены Miku©", icon_url= Bot.user.avatar_url )
    await Bot.say(embed = emb)
    await Bot.delete_message(ctx.message) #удаление отправленного сообщения
@инфо.error
async def инфо_error(ctx, error):
    await Bot.say("Ты забыл ввести участника, повтори попытку)")
#Очистка чата
@Bot.command(pass_context=True)
async def чистить(ctx, amount = 10):
    channel= ctx.message.channel
    messages = []
    async for message in Bot.logs_from(channel, limit=int(amount)+1):
        messages.append(message)
    await Bot.delete_messages(messages)
    await Bot.say("Удалено сообщений  {}".format(int(amount)))
    #time.sleep(5) #Пауза в скрипте

#________________________команды управления
#@Bot.command(pass_context=True)
#async def бан(ctx, user: discord.Member):
#    await Bot.ban(user)
#    await Bot.say("{} был забанен".format(user.name))
#@бан.error
#async def ban_error(ctx, error):
#    emb = discord.Embed(title= "Ахтунг",color = 0xff0000)
#    emb.add_field(name="Ошибка:",value="Такого пользователя нет")
#    await Bot.say(embed = emb)

#@Bot.command(pass_context=True)
#async def кик(ctx, user: discord.Member):
#    await Bot.kick(user)
#    await Bot.say("{} был кикнут".format(user.name))
#@кик.error
#async def kick_error(ctx, error):
#    emb = discord.Embed(title= "Ахтунг",color = 0xff0000)
#    emb.add_field(name="Ошибка:",value="Такого пользователя нет")
#    await Bot.say(embed = emb)

#@Bot.command(pass_context=True)
#async def мут(ctx, user: discord.Member):
#    await Bot.server_voice_state(user)
#    await Bot.say("Я замутила {}".format(user.name))
#@мут.error
#async def server_voice_state_error(ctx, error):
#    emb = discord.Embed(title= "Ахтунг",color = 0xff0000)
#    emb.add_field(name="Ошибка:",value="Такого пользователя нет")
#    await Bot.say(embed = emb)

@Bot.command(pass_context=True)
async def хелп(ctx):
    emb = discord.Embed(title= "",color = 0xffff00)
    emb.set_author(name= "Доступные команды")
    emb.add_field(name="ботинфо",value="Выдает краткую информацию о пользователе.\"ботинфо @Miku#8252\"")
    emb.add_field(name="ботктоты",value="Мику расскажет о себе")
    emb.add_field(name="ботчистить",value="Удаляет сообщения в чате.\"ботчистить 5\"")
    emb.add_field(name="ботранд",value="Выведет пользователю рандомное число в заданном ранее диапозоне")
    emb.add_field(name="ботсюда",value="Мику подключится к голосовому каналу на котором находитесь вы")
    emb.add_field(name="бототсюда",value="Мику отключится от вашего голосового канала(к сожалению работает не идеально, скоро будет исправленно)")
    emb.add_field(name="__Версия бота:__",value="1.4")
    emb.set_footer(text="Все права защищены Miku©", icon_url= Bot.user.avatar_url )
    await Bot.say(embed = emb)
    await Bot.delete_message(ctx.message)

@Bot.command(pass_context=True)
async def ктоты(ctx):
    emb= discord.Embed(title="",color = 0x00bfff)
    emb.set_author(name= "Мику Хацунэ\nHatsune Miku", url="https://ru.wikipedia.org/wiki/%D0%9C%D0%B8%D0%BA%D1%83_%D0%A5%D0%B0%D1%86%D1%83%D0%BD%D1%8D")
    emb.add_field(name="1.Кто ты ?",value="Я японская виртуальная певица, созданная компанией Crypton Future Media 31 августа 2007 года.\nШутка, на самом деле я Бот созданный для управления сервером Skrip_men")
    emb.add_field(name="2.Зачем ты нужна ?",value="Как я уже сказала, я нужна для помощи в управлении сервером Skrip_men")
    emb.add_field(name="3.Когда создана ?",value="Моей официальной датой создания является 8 марта 2019\n(вот я вас мужиков трести в 2 раза больше буду в марте)...Хехе...мда неловко получиловь")
    emb.add_field(name="4.Кто тебя написал и на каком языке ?",value="Я была написана Skrip_men'ом, на языке Python")
    emb.add_field(name="__Версия бота:__",value="1.3")
    emb.add_field(name="__Помошь в создании:__",value="alex jonas,Southpaw,\__STRAYKERRR__")

    emb.set_thumbnail(url= "https://cs11.pikabu.ru/post_img/2019/03/14/9/1552577750188312532.jpg")
    emb.set_footer(text="Все права защищены Miku©", icon_url= Bot.user.avatar_url )
    await Bot.say(embed = emb)
    await Bot.delete_message(ctx.message)

Bot.loop.create_task(change_status())
token = os.environ.get('bot_token')
Bot.run(str(token))
