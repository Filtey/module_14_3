from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

api = "key"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text = "Рассчитать")
button2 = KeyboardButton(text = "Информация")
button3 = KeyboardButton(text = "Купить")

kb.add(button)
kb.add(button2)
kb.row(button3)


kb2 = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data='calories')
b2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data='formulas')
kb2.add(b1)
kb2.add(b2)


kb3 = InlineKeyboardMarkup()
but1 = InlineKeyboardButton(text = 'Product1', callback_data='product_buying')
but2 = InlineKeyboardButton(text = 'Product2', callback_data='product_buying')
but3 = InlineKeyboardButton(text = 'Product3', callback_data='product_buying')
but4 = InlineKeyboardButton(text = 'Product4', callback_data='product_buying')
kb3.add(but1)
kb3.add(but2)
kb3.add(but3)
kb3.add(but4)






class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    print(message.text)
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup = kb)

@dp.message_handler(text = "Информация")
async def infor(message):
    print(message.text)
    await message.answer("ЭТО СДЕЛАЛ Я!)")

############
@dp.callback_query_handler(text = "calories")
async def set_age(call):
    print(call.message.text)
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    print(message.text)
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    print(message.text)
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    print(message.text)
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(f'Ваша норма калорий: {result} ккал в сутки (для женщин)')
    await UserState.weight.set()
    await state.finish()






###########
@dp.message_handler(text = "Рассчитать")
async def main_menu(message):
    print(message.text)
    await message.answer("Выберите опцию:", reply_markup=kb2)

@dp.callback_query_handler(text = "formulas")
async def get_formulas(call):
    print(call.message.text)
    await call.message.answer("10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()


#############
@dp.message_handler(text = "Купить")
async def get_buying_list(message):
    for i in range(1, 5):
        await message.answer(f"Название: Product{i} | Описание: описание {i} | Цена: {i * 100}")
        with open(f'{i}.jpg', 'rb') as img:
            await message.answer_photo(img)

    await message.answer("Выберите продукт для покупки:", reply_markup = kb3)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
