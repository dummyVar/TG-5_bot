import discord
from discord.ext import commands
from discord.ui import View, Button
import requests
from bs4 import BeautifulSoup
import random

config = {
    'token': 'MTAzOTQ5OTk0NDE2OTU4NjczOA.GWWhAf.g353MrcaUihwzLJVjajIazULMGYf5TWXMAeEC8',
    'prefix': '#',
}


async def random_news():
    response = requests.get('https://ria.ru/')
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.findAll(class_='cell-list__item-link')
    rand = random.randint(0, len(news) - 1)
    return news[rand].text, news[rand]['href']


async def wiki_info(request):
    a = request.replace(" ", "_")
    resp = requests.get(f'https://ru.wikipedia.org/wiki/{a}')
    soup = BeautifulSoup(resp.text, 'html.parser')
    wiki_text = soup.find('p').text
    another_wiki = soup.find_all(class_='mw-redirect')
    wiki_img = soup.find(class_='thumbinner').find('img')
    if wiki_img != None:
        return wiki_text, f'https://ru.wikipedia.org/wiki/{a}', another_wiki, wiki_img['src']
    else:
        return wiki_text, f'https://ru.wikipedia.org/wiki/{a}', another_wiki


bot = commands.Bot(intents=discord.Intents.all(),
                   command_prefix=config['prefix'])


@bot.command(name='новости')
async def news(ctx):
    msg = await random_news()
    text = msg[0]
    href = msg[1]
    await ctx.reply(f"{text}, \nЧитать далее: {href}")


@bot.command(name='вики')
async def studere(ctx, *args):
    request = '_'.join(args)
    result = await wiki_info(request)
    for href in result[2]:
        emb = discord.Embed(
            title=f'См. также: {href.text}',
            url=f'https://ru.wikipedia.org{href["href"]}'
        )
        await ctx.reply(embed=emb)
    embinfo = discord.Embed(
        title=f'{" ".join(args)}',
        description=str(result[0]),
        url=result[1]
    )
    if result[3] != None:
        embinfo.set_thumbnail(url=f'https:{result[3]}')
    await ctx.reply(embed=embinfo)


@bot.command(name='помощь')
async def help_bot(ctx):
    async def get_news(interaction):
        msg = await random_news()
        text = msg[0]
        href = msg[1]
        await interaction.response.send_message(f'{text}\nЧитать полную новость: {href}')

    async def get_wiki(interaction):
        await interaction.response.send_message(f'Введите ваш запрос используя команду #вики')

    news_btn = Button(label='Новости', style=discord.ButtonStyle.red)
    news_btn.callback = get_news
    wiki = Button(label='Справка', style=discord.ButtonStyle.green)
    wiki.callback = get_wiki
    view = View()
    view.add_item(news_btn)
    view.add_item(wiki)
    await ctx.reply(view=view)

@bot.command(name='меню')
async def menu(ctx):
    embed = discord.Embed(title="Помощник бота ТГ-5", description="Тут вы сможете найти всю информацию для работы с ботом", color=0xff2600)
    embed.set_author(name='ТГ-5', icon_url='https://www.pngmart.com/files/16/Vector-Help-PNG-Photos-1.png')
    embed.set_thumbnail(url='https://abali.ru/wp-content/uploads/2010/12/gerb_ussr.png')
    embed.add_field(name="__**Команды бота:**__", value="\a", inline=False)
    embed.add_field(name="ℹ️ #помощь;", value="вызов справки", inline=False)
    embed.add_field(name="📰 #новости", value="получить случайную новость с сайта РИА Новости", inline=False)
    embed.add_field(name="📖 #вики", value="получить информацию с сайта Википедия", inline=False)
    embed.add_field(name="🇷🇺 #товарищи", value="Почетный список товарищей", inline=False)
    embed.add_field(name='\a', value='\a', inline=False)
    embed.add_field(name='\a', value='\a', inline=False)
    embed.set_image(url='https://www.freepnglogos.com/uploads/youtube-logo-hd-8.png')
    embed.add_field(name='Полезные каналы:', value='\a', inline=False)
    embed.add_field(name='Иван Дымов', value='История, политика, справедливость. Канал товарища Дымова.\nhttps://www.youtube.com/@dymovivan/', inline=True)
    embed.add_field(name='Easy History', value='Привет, я очень люблю исторические видео, особенно когда они изложены в простом удобном формате, на этом канале история разных времен от античности до современности.\nhttps://www.youtube.com/@EasyHistory/', inline=True)
    embed.add_field(name='\a', value='\a', inline=False)
    embed.add_field(name='Мудреныч', value='\nhttps://www.youtube.com/@user-hd2im9sl5x', inline=True)
    embed.add_field(name='Сторик', value='Интересные и полезные  исторические видео на пальцах!\nhttps://www.youtube.com/@Storick', inline=True)
    embed.add_field(name='\a', value='\a', inline=False)
    embed.add_field(name='Epic History', value='Эпичная История познакомит вас с самыми драматичными и удивительными событиями в истории, от гигантских конфликтов, таких как Первая мировая война, до эпичной истории таких стран, как Россия.\nhttps://www.youtube.com/@EpicHistoryRu', inline=True)
    embed.add_field(name='Гео-История', value='Исторические и текущие события, коротко отображённые на карте. Канал является совместным проектом франкоязычного Histoire Géo и русскоязычного The Curious.\nhttps://www.youtube.com/@GeoHistory_Ru', inline=True)
    embed.add_field(name='\a', value='\a', inline=False)
    embed.add_field(name='Гамлен', value='Привет! Здесь ты найдешь самые топовые исторические видео на пальцах. Подписывайся чтобы не пропустить!\nhttps://www.youtube.com/@Gamlen/', inline=True)

    embed.set_footer(text="Разработано Павлом")
    await ctx.send(embed=embed)

@bot.command(name='товарищи')
async def friends_yt(ctx):
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
            'thumb': 'http://b445539u.beget.tech/epic.png',
        },
        'f_3': {
            'name': 'Мудреныч',
            'desc': 'История, политика, справедливость. Канал товарища Дымова.',
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

    for friend in friends.values():
        embed = discord.Embed(title=friend['name'], description=friend['desc'], color=0xff2600, url=friend['url'])
        embed.set_author(name='ТГ-5', icon_url='https://www.pngmart.com/files/16/Vector-Help-PNG-Photos-1.png')
        embed.set_image(url=friend['thumb'])

        await ctx.send(embed=embed)


bot.run(config['token'])


