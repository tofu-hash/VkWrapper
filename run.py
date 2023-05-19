from handlers.messages import *
from handlers.callback_query import *
from handlers.init import *

dp.register_callback_query_handler(cancel_cmd_handler, lambda msg: msg.data == 'cancel', state='*')
dp.register_message_handler(start_cmd_handler, commands=['start'], state='*')
dp.register_message_handler(get_sticker_id_handler, content_types=['sticker'], state='*')

dp.register_message_handler(set_api_key_cmd_handler, commands=['changekey'], state='*')
dp.register_message_handler(set_api_key_handler, state=states.Settings.set_openai_api_key)
dp.register_message_handler(reset_api_key_cmd_handler, commands='resetkey', state='*')


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            BotCommand('changekey', 'Установить API ключ'),
            BotCommand('resetkey', 'Сбросить ключ'),
            BotCommand('start', 'Перезапуск бота'),
        ]
    )


async def start(dispatcher) -> None:
    bot_name = dict(await dispatcher.bot.get_me()).get('username')
    await set_default_commands(dispatcher)
    print(f'#    start on @{bot_name}')


async def end(dispatcher) -> None:
    bot_name = dict(await dispatcher.bot.get_me()).get('username')
    print(f'#    end on @{bot_name}')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           on_startup=start,
                           on_shutdown=end)
