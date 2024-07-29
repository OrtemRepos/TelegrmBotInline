from aiogram import BaseMiddleware

class OnlyAdminMiddleware(BaseMiddleware):
    def __init__(self):
        self.admin_ids = ['1309443087', '772843648']

    async def __call__(self,
                       handler,
                       event,
                       data):
        user_id = data['event_from_user'].id
        if str(user_id) in self.admin_ids:
            return await handler(event, data)
        await event.answer('Ты не админ. Твой id: ' + str(user_id), show_alert=True)
        return