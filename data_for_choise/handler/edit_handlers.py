from aiogram import Router, F

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..characters import ListChoise
from ..createState import AddState
from ..middleware import OnlyAdminMiddleware

router = Router()
router.message.outer_middleware(OnlyAdminMiddleware)

@router.message(Command('add'))
async def cmd_edit(message, state: FSMContext):
    lists = ListChoise.load_from_file('characters.json')
    await state.set_state(AddState.choosing_list)
    builder = ReplyKeyboardBuilder()
    for list in lists._lists:
        builder.add(KeyboardButton(text=list._name))
    builder.adjust(10)
    await message.answer(text="Выбери список для редактирования", reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True))

@router.message(AddState.choosing_list)
async def choosing_list(message, state: FSMContext):
    await state.update_data(list=message.text)
    await state.set_state(AddState.choosing_name)
    await message.answer(text="Введи название")

@router.message(AddState.choosing_name)
async def choosing_name(message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddState.choosing_description)
    await message.answer(text="Введи описание")

@router.message(AddState.choosing_description)
async def choosing_description(message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddState.choosing_image)
    await message.answer(text="Введи картинку")


@router.message(AddState.choosing_image)
async def choosing_image(message, state: FSMContext):
    await state.update_data(image=message.text)
    user_data = await state.get_data()
    lists = ListChoise.load_from_file('characters.json')
    lists.add_charecter_in_list_by_name(list_name=user_data['list'], name=user_data['name'], description=user_data['description'], image=user_data['image'])
    lists.serialize('characters.json')
    await message.answer(text="Готово")
    await state.clear()