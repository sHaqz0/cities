import json
import os
import discord
from config import settings


def parse_name_json(json_file='citiesss.json'):
    content = {}
    p_obj = None
    try:
        js_obj = open(json_file, "r", encoding="utf-8")
        p_obj = json.load(js_obj)
    except Exception as err:
        print(err)
        return None
    finally:
        js_obj.close()
    return [name['name'].lower() for name in p_obj]


def get_name(name):
    normilize_name = name.strip().lower()[1:]
    if is_correct_name_namme(normilize_name):
        if get_name.previous_name != "" and normilize_name[0] != get_name.previous_name[-1]:
            return 'Город должен начинаться на "{0}"!'.format(get_name.previous_name[-1])

        if normilize_name not in cities_already_nammed:
            cities_already_nammed.add(normilize_name)
            last_latter_name = normilize_name[-1]
            proposed_nammes = list(filter(lambda x: x[0] == last_latter_name, cities))
            if proposed_nammes:
                for name in proposed_nammes:
                    if name not in cities_already_nammed:
                        cities_already_nammed.add(name)
                        get_name.previous_name = name
                        return name.capitalize()
            return 'Я не знаю города на эту букву. Ты выиграл'
        else:
            return 'Город уже был. Повторите попытку'
    else:
        return 'Некорректное название города. Повторите попытку'


get_name.previous_name = ""


def is_correct_name_namme(name):
    return name[-1].isalpha() and name[-1] not in ('ь', 'ъ')


def refresh():
    cities = parse_name_json()[:1000]
    cities_already_nammed = set()


cities = parse_name_json()[:1000]  # города которые знает бот
cities_already_nammed = set()  # города, которые уже называли

TOKEN = settings['token']

bot = discord.Client()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!'):
        if message.content == '!refresh':
            refresh()
        else:
            response = get_name(message.content)
            await message.channel.send(response)


bot.run(TOKEN)