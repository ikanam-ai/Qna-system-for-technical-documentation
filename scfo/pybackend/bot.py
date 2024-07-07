import asyncio
import aiohttp
import markdown
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram.utils.exceptions import TelegramAPIError

TOKEN = '7345238327:AAHt47JdeClvWMojB7uwWaaqdpCLFBx1RZU'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


class Form(StatesGroup):
    start = State()
    question = State()


@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await Form.start.set()
    link_to_rustore = 'https://www.rustore.ru/help/'
    link_to_web = 'http://147.45.139.59/'
    await bot.send_message(message['chat']['id'], 'Привет!\n'
                                                  f'Это ваш личный AI ассистент по <a href="{link_to_rustore}">документации RuStore</a> – лучшего '
                                                  'магазина приложений в Рунете.\n\n'
                                                  f'При желании вы можете воспользоваться моей <a href="{link_to_web}">web-версией</a>',
                           reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
    await start(state, message['chat']['id'])


async def start(state: FSMContext, chat_id: int):
    await bot.send_message(chat_id, "Задайте мне любой вопрос, и я постараюсь вам помочь!",
                           reply_markup=ReplyKeyboardRemove())
    await Form.question.set()


@dp.message_handler(state=Form.question)
async def get_question(message: types.Message, state: FSMContext):
    user_input = message.text
    try:
        response = await send_to_server(user_input)
        response_message = response.get('message', 'Нет ответа от сервера')
        response_message = adapt_html_for_telegram(response_message)
        try:
            await message.reply(response_message, parse_mode='HTML')
        except TelegramAPIError as e:
            if "Bad Gateway" in str(e):
                await message.reply(response_message, parse_mode='HTML')
            else:
                await message.reply("К сожалению, произошла техническая ошибка. Отправьте вопрос ещё раз", parse_mode='HTML')
    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")


async def send_to_server(prompt_text):
    url = 'http://localhost:8000/receive-prompt'
    data = {"text": prompt_text + '\nобязательно разметь ответ в формате html. Можно использовать строго только тэги <b>, <strong>, <i>, <em>, <u> , <s>, <strike>, <del>,<a href="URL">, <code>,<pre>. В тексте никак не упомянай про html разметку'}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to receive data: {response.status}")


def adapt_html_for_telegram(html_text):
    html_text = markdown.markdown(html_text, extensions=['nl2br'])
    print(html_text)
    adapted_text = html_text.replace('<p>', '').replace('</p>', '')
    adapted_text = adapted_text.replace('<ol>', '$$$').replace('</ol>', '$$$')
    adapted_text = adapted_text.replace('<li>', '$$$').replace('</li>', '$$$')
    adapted_text = adapted_text.replace('<ul>', '$$$').replace('</ul>', '$$$')
    adapted_text = adapted_text.replace('<br>', '').replace('<br/>', '')
    adapted_text = adapted_text.replace('<br />', '')
    test = adapted_text.split('$$$')
    res = []
    for i in range(len(test)):
        if i != len(test) - 1 and i != 0:
            if not(test[i-1][-2:] == '\n' and test[i+1][:2] == '\n' and test[i] == '\n'):
                res.append(test[i])
        elif i == 0:
            if test[i] != '\n':
                res.append(test[i])
        else:
            res.append(test[i])
    return ''.join(res)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if loop is None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    executor.start_polling(dp, skip_updates=True, loop=loop)
