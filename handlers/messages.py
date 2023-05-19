from utils.image_processing import *
from handlers.init import *
import asyncio
import os
import io


async def start_cmd_handler(msg: Message, state: FSMContext):
    await state.finish()

    execute(
        ('INSERT OR IGNORE INTO users '
         '(user_id) VALUES (%s);') %
        msg.from_user.id
    )

    if msg.get_args():
        args = msg.get_args()

        if args == 'changekey':
            await states.Settings.set_openai_api_key.set()

            answer = '🔑 Отправь мне новый API ключ.'
            await msg.answer(text=answer,
                             reply_markup=keyboards.add_openai_api_key)

    else:

        api_key = execute(
            ('SELECT api_key FROM users '
             'WHERE user_id=%s') % msg.from_user.id,
            fetchone=True
        )[0]

        if not api_key:
            answer = '🤔 Отправь мне ссылку с API ключом и я загружу фото в твой профиль как ' \
                     'на картинке выше\n\n' \
                     '⚙ Инструкция по получению ключа:\n' \
                     '1. Перейдите на сайт https://vkhost.github.io\n' \
                     '2. Нажмите на кнопку vk.com\n' \
                     '3. После перехода на страницу вк нажмите "разрешить"\n' \
                     '4. Скопируйте ссылку, на которую вас перебросило в бота'
            await states.Settings.set_openai_api_key.set()
        else:
            answer = '😇 Отправь мне фото и я загружу его в твой профиль как ' \
                     'на картинке выше'
        await msg.answer_sticker(sticker='CAACAgIAAxkBAAN7ZFD2m2SgAxweWK9uflY2iieRfEQAAlEAAyRxYhrpRxtfxj-nIy8E')
        await msg.answer_photo(caption=answer,
                               photo=open('source/service/test_template.jpg', 'rb'),
                               parse_mode='markdown')


async def set_api_key_cmd_handler(msg: Message):
    await states.Settings.set_openai_api_key.set()

    answer = '🔑 Отправь мне API ключ.'
    await msg.answer(text=answer,
                     reply_markup=keyboards.add_openai_api_key)


async def set_api_key_handler(msg: Message, state: FSMContext):
    try:
        key = msg.text.split('access_token=')[1]
        key = key.split('&')[0]

        execute(
            ('UPDATE users SET api_key="%s" '
             'WHERE user_id=%s') %
            (key, msg.from_user.id)
        )

        answer = '💾 Сохранено. Теперь вы можете отправлять фото.'
        await msg.delete()
        await state.finish()
    except:
        answer = '⚠ Некорректная ссылка'

    await msg.answer(text=answer)


async def reset_api_key_cmd_handler(msg: Message, state: FSMContext):
    await state.finish()
    execute(
        ('UPDATE users SET api_key=NULL '
         'WHERE user_id=%s') %
        msg.from_user.id
    )
    answer = '💾 Ключ удалён.'
    await msg.answer(text=answer)


@dp.message_handler(content_types=['photo'], state='*')
async def photo_handler(msg: Message):
    api_key = execute(
        ('SELECT api_key FROM users '
         'WHERE user_id=%s') % msg.from_user.id,
        fetchone=True
    )[0]

    if not api_key:
        bot_data = await bot.get_me()
        bot_name = bot_data['username']
        link = 'https://t.me/' + bot_name + '?start=changekey'
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton(text='🔑 Установить ключ',
                                              url=link))

        await msg.answer(text='⚠ Ключ не установлен.\n\n',
                         reply_markup=reply_markup)
    else:
        await msg.answer(text='⚙ Обрабатываю')
        await msg.photo[-1].download(destination_file='source/service/%s.jpg' % msg.from_user.id)

        crop(msg.from_user.id, 2)
        make_template(msg.from_user.id)
        image_id = str(msg.from_user.id)

        api_session = vk_api.VkApi(token=api_key)
        upload_session = vk_api.upload.VkUpload(api_session)

        path = 'source/service/results/{}/'.format(image_id)
        photos = ['{}{}__processed.jpg'.format(path, item) for item in range(1, 7)][::-1]

        album = api_session.method('photos.createAlbum', values={
            'title': 'Wrapper'
        })
        album_id = album['id']

        upload_session.photo(photos=photos,
                             album_id=album_id,
                             caption='Wrapper 👻')

        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton(text='🗑 Удалить фото',
                                              callback_data='remove_%s' % album_id))

        await msg.answer_photo(caption='✅ Фото загружено\n\n'
                                       'Выше пример блока фотографий в твоём профиле\n\n',
                               photo=open('source/service/result_template.jpg', 'rb'),
                               reply_markup=reply_markup)
        remove_path = 'source/service/results/%s' % msg.from_user.id
        for file in os.listdir(remove_path):
            os.remove('%s/%s' % (remove_path, file))
        os.rmdir(remove_path)
        os.remove('source/service/%s.jpg' % msg.from_user.id)
        os.remove('source/service/result_template.jpg')


async def get_sticker_id_handler(msg: Message):
    await msg.answer_sticker(sticker=msg.sticker.file_id)
    print(msg.sticker.file_id)
