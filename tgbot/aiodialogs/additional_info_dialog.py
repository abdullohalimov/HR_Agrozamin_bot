import operator
import json
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window
from aiogram_dialog.widgets.kbd import Multiselect, Button
from aiogram_dialog.widgets.text import Format, Const
from tgbot.misc.states import UserInfo
from tgbot.keyboards.inline import tasdiqlash_inl_kb
from tgbot.hr_i18n import _
from aiogram_dialog.context.context import Context



# let's assume this is our window data getter
async def get_data(dialog_manager: DialogManager, **kwargs):
    extra_categories = [
        ("SQL", '1'),
        ("HTML", '2'),
        ("CSS", '3'),
        ("Git", '4'),
        ("Linux OS", '5'),
    ]
    return {
        "extra_categories": extra_categories,
        "count": len(extra_categories),
    }

async def tasdiqlash_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    data = dialog_manager.current_context().start_data()
    print(dialog_manager.current_context().widget_data.get('extra_category'))
    print(data)    
    await callback.message.edit_text(_("""
Анкетангиз тузилди: 
ФИО: {name}
Телефон: {phone}
Ёшингиз: {age}
Маълумотингиз: {educ}
Дастурлаш тили: {prog_lang}
Кошимча маьлумотлар: {add_info}
""".format(
    name=data.get('fio'),
    phone=data.get('phone'),
    age=data.get('age'),
    educ=data.get('education'),
    prog_lang=data.get('prog_lang'),
    add_info=data.get('additional')
    )), reply_markup=tasdiqlash_inl_kb)

    await UserInfo.next()
    await dialog_manager.done()


window = Window(
    Const("Қўшимча нималарни биласиз?"),
    Multiselect(
    Format("✅ {item[0]}"),  # E.g `✓ Apple`
    Format("{item[0]}"),
    id="extra_category",
    item_id_getter=operator.itemgetter(1),
    items='extra_categories',
    ),
    Button(
        Const("Тасдиклаш"),
        on_click=tasdiqlash_button,
        id='finish'
    ),

    state=UserInfo.additional,
    getter=get_data
)

dialog = Dialog(window)

def register_dialog(dp: Dispatcher):
    registry = DialogRegistry(dp)
    registry.register(dialog)