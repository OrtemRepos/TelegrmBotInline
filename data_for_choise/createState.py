from aiogram.fsm.state import StatesGroup, State
class CreateState(StatesGroup):
    choosing_name = State()
    choosing_description = State()
    choosing_image = State()

class AddState(StatesGroup):
    choosing_list = State()
    choosing_name = State()
    choosing_description = State()
    choosing_image = State()

class DeleteCommon(StatesGroup):
    delete_list = State()
    delete_character = State()
    choise_list = State()
