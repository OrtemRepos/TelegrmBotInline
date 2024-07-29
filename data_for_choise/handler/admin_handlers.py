from aiogram import Router, F
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..characters import ListChoise
from ..createState import CreateState, AddState
router = Router()

@router.message(Command('create'))
async def cmd_create(message, state: FSMContext):
    await state.set_state(CreateState.choosing_name)
    await message.answer(text="Введи название")



@router.message(CreateState.choosing_name)
async def choosing_name(message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateState.choosing_description)
    await message.answer(text="Введи описание", reply_markup=ReplyKeyboardRemove())

@router.message(CreateState.choosing_description)
async def choosing_description(message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text="Введи картинку")
    await state.set_state(CreateState.choosing_image)

@router.message(CreateState.choosing_image)
async def choosing_image(message, state: FSMContext):
    await state.update_data(image=message.text)
    await message.answer(text="Готово", reply_markup=ReplyKeyboardRemove())
    user_data = await state.get_data()
    await state.clear()
    lists = ListChoise.load_from_file('characters.json')
    lists.add_list(user_data['name'], user_data['description'], user_data['image'])
    lists.serialize('characters.json')
    


@router.message(Command('cancel'))
async def cancel(message, state: FSMContext):
    await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
    await state.set_state('None')

@router.message(Command('admin'))
async def admin_check(message, is_admin: bool):
    if is_admin:
        await message.answer('Ты админ')
    else:
        await message.answer('Ты не админ. Твой id: ' + str(message.from_user.id))
