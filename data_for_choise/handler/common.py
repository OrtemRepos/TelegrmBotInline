from aiogram import Router, F
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from ..createState import DeleteCommon
from ..characters import ListChoise

router = Router()

@router.message(Command('cancel'))
async def cancel(message, state: FSMContext):
    await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
    await state.set_state('None')

@router.message(Command('delete'))
async def cmd_delete(message):
    kb = []
    kb.append([KeyboardButton(text="Удалить список")])
    kb.append([KeyboardButton(text="Удалить персонажа")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери что будем удалять"
    )
    await message.answer(text="Что будем удалять?", reply_markup=keyboard)


@router.message(F.text.contains("список"))
async def cmd_delete_list(message, state: FSMContext):
    await state.set_state(DeleteCommon.delete_list)
    lists = ListChoise.load_from_file('characters.json')
    kb = [[KeyboardButton(text=list._name)] for list in lists._lists]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(text="Выбери список для удаления", reply_markup=keyboard)

@router.message(F.text.contains("персонажа"))
async def cmd_delete_character(message, state: FSMContext):
    await state.set_state(DeleteCommon.choise_list)
    lists = ListChoise.load_from_file('characters.json')
    kb = [[KeyboardButton(text=list._name)] for list in lists.get_lists()]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери список из которого нужно удалить персонажа"
    )
    await message.answer(text="Выбери список из которого нужно удалить персонажа", reply_markup=keyboard)
