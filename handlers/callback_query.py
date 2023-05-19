from utils.image_processing import *
from handlers.init import *


@dp.callback_query_handler(lambda msg: 'remove_' in msg.data)
async def remove_album_handler(msg: CallbackQuery):
    album_id = msg.data.split('remove_')[1]
    api_key = execute(
        ('SELECT api_key FROM users '
         'WHERE user_id=%s') % msg.from_user.id,
        fetchone=True
    )[0]

    api_session = vk_api.VkApi(token=api_key)
    response = api_session.method('photos.deleteAlbum', values={
        'album_id': album_id
    })
    print(response)

    answer = '🗑 Фото удалено'
    await msg.message.edit_caption(caption=answer)


async def cancel_cmd_handler(cq: CallbackQuery, state: FSMContext):
    await cq.answer()
    await state.finish()

    answer = '✅ Действие отменено'
    await cq.message.edit_text(text=answer)
