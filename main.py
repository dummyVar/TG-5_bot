# Библиотека для работы с дискорд
import discord
from discord.ext import commands
# Библиотека для работы с веб-сайтами
import requests
# Библиотека для обработки данных полученных с веб-сайта
from bs4 import BeautifulSoup
# Библиотека генерации случайных значений
import random

# Конфигурация бота
config = {
    # Уникальный ключ доступа к созданному боту
    'token': 'TOKEN',
    # Префикс для вызова комманд бота
    'prefix': '!',
}

# Функция для получения случайной новости с сайта РИА
async def random_news():
    # Мы отправляем запрос на сайт и получаем ответ от него
    response = requests.get('https://ria.ru/')
    # Ответ от сайта преобразуем для работы с python
    soup = BeautifulSoup(response.text, 'html.parser')
    # В преобразованном файле ищем новости
    news = soup.findAll(class_='cell-list__item-link')
    # Генерируем ключ для случайной новости
    rand = random.randint(0, len(news) - 1)
    # Передаем случайную новость
    return news[rand].text, news[rand]['href']

# Функция получения статей с Википедии
async def wiki_info(request):
    # Подготавливаем запрос на сайт, заменяя пробелы нижним подчеркиванием
    a = request.replace(" ", "_")
    # Отправляем запрос на википедию, и сохраняем ответ
    resp = requests.get(f'https://ru.wikipedia.org/wiki/{a}')
    # Преобразуем ответ для работы с python
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Ищем текст определения по запросу
    wiki_text = soup.find('p').text
    # Собираем все "смежные" ссылки из статьи
    another_wiki = soup.find_all(class_='mw-redirect')
    # Получаем изображение к статье
    wiki_img = soup.find(class_='thumbinner').find('img')
    # Если изображение есть - передаем набор данных (текст статьи, ссылка на статью, ссылки на "смежные" статьи, ссылка на картинку к статье)
    if wiki_img != None:
        return wiki_text, f'https://ru.wikipedia.org/wiki/{a}', another_wiki, wiki_img['src']
    # Иначе передаем набор данных (текст статьи, ссылка на статью, ссылки на "смежные" статьи)
    else:
        return wiki_text, f'https://ru.wikipedia.org/wiki/{a}', another_wiki

# Заводим переменную для бота, настраеваем его разешения, и задаем префикс для вызова
bot = commands.Bot(intents=discord.Intents.all(),
                   command_prefix=config['prefix'])


# Команда бота для запроса случайной новости
@bot.command(name='новости')
async def news(ctx):
    # Запрашиваем новость
    msg = await random_news()
    # Берем её текст
    text = msg[0]
    # Берем ссылку на неё
    href = msg[1]
    # Отправляем сообщение в дискорд (Текст + ссылка на полную новость)
    await ctx.reply(f"{text}, \nЧитать далее: {href}")

# Команда для запроса статьи с википедии
@bot.command(name='вики')
async def studere(ctx, *args):
    # Собираем из слов единую фразу
    request = '_'.join(args)
    # Запрашиваем статью на википедии
    result = await wiki_info(request)
    # Отправляем сообщение со всеми "смежными" ссылками
    for href in result[2]:
        emb = discord.Embed(
            title=f'См. также: {href.text}',
            url=f'https://ru.wikipedia.org{href["href"]}'
        )
        await ctx.reply(embed=emb)
    # Отправляем текст статьи
    embinfo = discord.Embed(
        title=f'{" ".join(args)}',
        description=str(result[0]),
        url=result[1]
    )
    # Картинка к статье
    if result[3] != None:
        embinfo.set_thumbnail(url=f'https:{result[3]}')
    await ctx.reply(embed=embinfo)

# Команда для вызова меню
@bot.command(name='меню')
async def menu(ctx):
    embed = discord.Embed(title="Помощник бота Learn History", description="Тут вы сможете найти всю информацию для работы с ботом", color=0xff2600)
    embed.set_author(name='Learn History', icon_url='https://www.pngmart.com/files/16/Vector-Help-PNG-Photos-1.png')
    embed.set_thumbnail(url='https://abali.ru/wp-content/uploads/2010/12/gerb_ussr.png')
    embed.add_field(name="__**О сервере:**__", value="Сервер создан для изучения и обсуждения истории. Используя наш сервер вы можете не только обсуждать исторические темы и текущие новости, но и познавать мир посредствам нашего бота ТГ-5.", inline=False)
    embed.add_field(name='\a', value='\a', inline=False)
    embed.add_field(name="__**Команды бота:**__", value="\a", inline=False)
    embed.add_field(name="📰 #новости", value="получить случайную новость с сайта РИА Новости", inline=False)
    embed.add_field(name="📖 #вики", value="получить информацию с сайта Википедия", inline=False)
    embed.add_field(name="🇷🇺 #товарищи", value="Почетный список товарищей", inline=False)
    embed.add_field(name='\a', value='\a', inline=False)
    embed.set_image(url='https://www.freepnglogos.com/uploads/youtube-logo-hd-8.png')
    embed.add_field(name='Полезные каналы:', value='\a', inline=False)
    embed.add_field(name='Иван Дымов', value='История, политика, справедливость. Канал товарища Дымова.\nhttps://www.youtube.com/@dymovivan/', inline=True)
    embed.add_field(name='Easy History', value='Привет, я очень люблю исторические видео, особенно когда они изложены в простом удобном формате, на этом канале история разных времен от античности до современности.\nhttps://www.youtube.com/@EasyHistory/', inline=True)
    embed.add_field(name='\a', value='\a', inline=False)
    embed.add_field(name='Мудреныч', value='Короткие ролики до 10 минут про историю. Классная подача через комиксы.\nhttps://www.youtube.com/@user-hd2im9sl5x', inline=True)
    embed.add_field(name='Сторик', value='Интересные и полезные  исторические видео на пальцах!\nhttps://www.youtube.com/@Storick', inline=True)
    embed.add_field(name='\a', value='\a', inline=False)
    embed.add_field(name='Epic History', value='Эпичная История познакомит вас с самыми драматичными и удивительными событиями в истории, от гигантских конфликтов, таких как Первая мировая война, до эпичной истории таких стран, как Россия.\nhttps://www.youtube.com/@EpicHistoryRu', inline=True)
    embed.add_field(name='Гео-История', value='Исторические и текущие события, коротко отображённые на карте. Канал является совместным проектом франкоязычного Histoire Géo и русскоязычного The Curious.\nhttps://www.youtube.com/@GeoHistory_Ru', inline=True)
    embed.add_field(name='\a', value='\a', inline=False)
    embed.add_field(name='Гамлен', value='Привет! Здесь ты найдешь самые топовые исторические видео на пальцах. Подписывайся чтобы не пропустить!\nhttps://www.youtube.com/@Gamlen/', inline=True)

    embed.set_footer(text="Разработано Павлом")
    # отправляем сообщение с нашим набором информации о боте
    await ctx.send(embed=embed)

# Функция вывода интересных ютуб каналов
@bot.command(name='товарищи')
async def friends_yt(ctx):
    # Словарь из каналов
    friends = {
        'f_1': {
            'name': 'Иван Дымов',
            'desc': 'История, политика, справедливость. Канал товарища Дымова.',
            'url': 'https://www.youtube.com/@dymovivan/',
            'thumb': 'http://b445539u.beget.tech/Дымов.png',
        },
        'f_2': {
            'name': 'Easy History',
            'desc': 'Привет, я очень люблю исторические видео, особенно когда они изложены в простом удобном формате, на этом канале история разных времен от античности до современности.',
            'url': 'https://www.youtube.com/@EasyHistory/',
            'thumb': 'http://b445539u.beget.tech/изи.png',
        },
        'f_3': {
            'name': 'Мудреныч',
            'desc': 'Короткие ролики до 10 минут про историю. Классная подача через комиксы.',
            'url': 'https://www.youtube.com/@user-hd2im9sl5x',
            'thumb': 'http://b445539u.beget.tech/мудреныч.png',
        },
        'f_4': {
            'name': 'Сторик',
            'desc': 'Интересные и полезные  исторические видео на пальцах!',
            'url': 'https://www.youtube.com/@Storick',
            'thumb': 'http://b445539u.beget.tech/сторик.png',
        },
        'f_5': {
            'name': 'Epic History',
            'desc': 'Эпичная История познакомит вас с самыми драматичными и удивительными событиями в истории, от гигантских конфликтов, таких как Первая мировая война, до эпичной истории таких стран, как Россия.',
            'url': 'https://www.youtube.com/@EpicHistoryRu',
            'thumb': 'http://b445539u.beget.tech/epic.png',
        },
        'f_6': {
            'name': 'Гео-История',
            'desc': 'Исторические и текущие события, коротко отображённые на карте. Канал является совместным проектом франкоязычного Histoire Géo и русскоязычного The Curious.',
            'url': 'https://www.youtube.com/@GeoHistory_Ru',
            'thumb': 'http://b445539u.beget.tech/его.png',
        },
        'f_7': {
            'name': 'Гамлен',
            'desc': 'Привет! Здесь ты найдешь самые топовые исторические видео на пальцах. Подписывайся чтобы не пропустить!',
            'url': 'https://www.youtube.com/@Gamlen/',
            'thumb': 'http://b445539u.beget.tech/гамлен.png',
        },
    }
    # Отправляем каждый отдельный канал с описанием в сообщении
    for friend in friends.values():
        embed = discord.Embed(title=friend['name'], description=friend['desc'], color=0xff2600, url=friend['url'])
        embed.set_author(name='Learn History', icon_url='https://www.pngmart.com/files/16/Vector-Help-PNG-Photos-1.png')
        embed.set_image(url=friend['thumb'])

        await ctx.send(embed=embed)

# Запуск бота в работу
bot.run(config['token'])


