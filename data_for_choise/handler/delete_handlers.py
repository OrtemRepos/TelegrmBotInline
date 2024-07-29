from aiogram import Router, F
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from ..createState import DeleteCommon
from ..characters import ListChoise

router = Router()


@router.message(DeleteCommon.delete_list)
async def delete_list(message, state: FSMContext):
    lists = ListChoise.load_from_file('characters.json')
    lists.delete_list_by_name(message.text)
    lists.serialize('characters.json')
    await state.set_state('None')
    await message.answer(text="Список удален", reply_markup=ReplyKeyboardRemove())

@router.message(DeleteCommon.choise_list)
async def delete_character(message, state: FSMContext):
    lists = ListChoise.load_from_file('characters.json')
    list_id = lists.get_charecter_list_by_name(message.text)
    await state.update_data(list_id=list_id)
    kb = [[KeyboardButton(text=char._name)] for char in lists._lists[list_id]._charecters]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери персонажа для удаления"
    )
    await state.set_state(DeleteCommon.delete_character)
    await message.answer(text="Выбери персонажа для удаления", reply_markup=keyboard)

@router.message(DeleteCommon.delete_character)
async def delete_character(message, state: FSMContext):
    data = await state.get_data()
    lists = ListChoise.load_from_file('characters.json')
    lists.delete_charater_from_list(data['list_id'], message.text)
    lists.serialize('characters.json')
    await state.set_state('None')
    await message.answer(text="Персонаж удален", reply_markup=ReplyKeyboardRemove())