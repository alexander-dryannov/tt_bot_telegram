from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram import types
from init_bot import dp


class Form(StatesGroup):
    size = State()
    payment = State()
    confirm = State()


@dp.message_handler(commands=['заказ', 'start'], state=None)
@dp.message_handler(Text(equals='заказ', ignore_case=True), state=None)
async def message_welcome(message: types.Message):
    await Form.size.set()
    await message.answer('Какую вы хотите пиццу, большую или маленькую?')


@dp.message_handler(commands=['отмена'], state='*')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def message_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Операция отменена')


@dp.message_handler(state=Form.size)
async def get_size(message: types.Message, state: FSMContext):
    print(state)
    async with state.proxy() as data:
        data['size'] = message.text
    await Form.next()
    await message.answer('Как будете платить?')


@dp.message_handler(state=Form.payment)
async def get_type_payment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['payment'] = message.text.lower()
    await Form.next()
    await message.answer(f'Вы будете {data["size"]} пиццу, оплата {data["payment"]}, все верно?')


@dp.message_handler(state=Form.confirm)
async def confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
            data['confirm'] = message.text.lower()
        await message.answer(f'Спасибо за заказ! {data}')
        await state.finish()
    else:
        async with state.proxy() as data:
            data['confirm'] = 'failure'
        await message.answer('Заказ не подтвержден.')
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
