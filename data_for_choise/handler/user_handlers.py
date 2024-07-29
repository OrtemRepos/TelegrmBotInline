from aiogram import Router, F, html
from aiogram.methods import SendPhoto
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, LinkPreviewOptions
from ..characters import ListChoise


router = Router()

def get_character(name):
    lists = ListChoise.load_from_file('characters.json')
    character = lists.rnd_character_in_list_by_name(name)
    text = [f"{html.bold(character._name)}"]
    if character._description:
        text.append(character._description)
    return '\n'.join(text), character._image

@router.inline_query(F.query.contains(''))
async def choise(inline_query):
    result = []
    lists = ListChoise.load_from_file('characters.json')
    for id, list in enumerate(lists.get_lists()):
        text, image = get_character(list._name)
        result.append(InlineQueryResultArticle(
            id=str(id),
            title=list._name,
            description=list._description,
            thumbnail_url=list._image,
            thumb_width=50,
            thumb_height=50,
            input_message_content=InputTextMessageContent(
                message_text=text,
                link_preview_options=LinkPreviewOptions(url=image, prefer_large_media=True),
                parse_mode='HTML'
            )
        ))
    await inline_query.answer(results=result, cache_time=0)