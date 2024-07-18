from aiogram import Bot, Dispatcher, types, F, filters
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
import asyncio
import openai
import os
from pytubefix import YouTube
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



openai.api_key = "sk-proj-bZ2XEBWPfMqcoojhQEVGT3BlbkFJ1IvU6DrYpZXoU8Ivil8B"
bot = Bot(token="7089119554:AAHRINcIj7opCLHqDdhbyynjCstgL2AYkXg")
dp = Dispatcher(bot=bot)

class Reg(StatesGroup):
    lang = State()
    name = State()
    surname = State()
    number = State()
    credit_num = State()

basket_uz = []
basket_ru = []
total = []

about_us = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📹", callback_data="video"), InlineKeyboardButton(text="🔗", url="https://www.pdp.uz/")]
])

phone_num = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📞", request_contact=True)]
], resize_keyboard=True)

lang_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="ru"), KeyboardButton(text="uz")],
],resize_keyboard=True)

main_kb_uz = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="kurslar"), KeyboardButton(text="savatcha"), KeyboardButton(text="Qo'llab quvvatlash")],
    [KeyboardButton(text="Biz haqimizda"), KeyboardButton(text="Tilni o'zgartirish")]
],resize_keyboard=True)

main_kb_ru = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="курсы"), KeyboardButton(text="корзина"), KeyboardButton(text="поддержка")],
    [KeyboardButton(text="о нас"), KeyboardButton(text="изменить язык")]
],resize_keyboard=True)

courses_kb_uz = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Front-end", callback_data="front-uz"),InlineKeyboardButton(text="Back-end", callback_data="back-uz")],
    [InlineKeyboardButton(text="Starter", callback_data="start-uz"),InlineKeyboardButton(text="Dizayn", callback_data="dizayn-uz")],
    [InlineKeyboardButton(text="❌", callback_data="delete")]
])

courses_kb_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Front-end", callback_data="front-ru"),InlineKeyboardButton(text="Back-end", callback_data="back-ru")],
    [InlineKeyboardButton(text="Starter", callback_data="start-ru"),InlineKeyboardButton(text="Dizayn", callback_data="dizayn-ru")],
    [InlineKeyboardButton(text="❌", callback_data="delete")]
])

front_buy = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛒", callback_data="front_buy"), InlineKeyboardButton(text="❌", callback_data="delete")]
])

back_buy = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛒", callback_data="back_buy"), InlineKeyboardButton(text="❌", callback_data="delete")]
])

dizayn_buy = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛒", callback_data="dizayn_buy"), InlineKeyboardButton(text="❌", callback_data="delete")]
])

start_buy = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛒", callback_data="start_buy"), InlineKeyboardButton(text="❌", callback_data="delete")]
])

basket_kb_uz = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Sotib olish"), KeyboardButton(text="Bekor qilish"), KeyboardButton(text="Ortga")]
], resize_keyboard=True)

basket_kb_ru = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="купить"), KeyboardButton(text="отменить"), KeyboardButton(text="назад")]
], resize_keyboard=True)

@dp.message(F.text == "Ortga")
async def ortga(message: Message):
    await message.answer("Bosh menuga qaytdingiz", reply_markup=main_kb_uz)

@dp.message(F.text == "назад")
async def ortga_ru(message: Message):
    await message.answer("вы вернулись в главное меню", reply_markup=main_kb_ru)

@dp.callback_query(F.data == "delete")
async def del_message(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

# Registration 

@dp.message(filters.CommandStart())
async def start_bot(message: Message, state: FSMContext):
    await state.set_state(Reg.lang)
    await message.answer("Tilni tanlang\nвыберите язык", reply_markup=lang_kb)

@dp.message(Reg.lang)
async def language_bot(message: Message, state: FSMContext):
    await state.update_data(lang=message.text)
    await state.set_state(Reg.name)
    data = await state.get_data()
    if data['lang'] == "uz":
        await message.answer(text="Ismingizni kiriting", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text="введите ваше имя", reply_markup=ReplyKeyboardRemove())

@dp.message(Reg.name)
async def name_bot(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.surname)
    data = await state.get_data()
    if data['lang'] == "uz":
        await message.answer(text="familiyangizni kiriting")
    else:
        await message.answer(text="введите свою фамилию")

@dp.message(Reg.surname)
async def surname_bot(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(Reg.number)
    data = await state.get_data()
    if data['lang'] == "uz":
        await message.answer(text="Telefon raqamingizni jonating", reply_markup=phone_num)
    else:
        await message.answer(text="пришлите свой номер телефона", reply_markup=phone_num)

@dp.message(Reg.number)
async def number_bot(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await state.clear()
    if data['lang'] == "uz":
        await message.answer(text=f"{data["name"]}\n{data["surname"]}\n{data["number"]}", reply_markup=main_kb_uz)
    else:
        await message.answer(text=f"{data["name"]}\n{data["surname"]}\n{data["number"]}", reply_markup=main_kb_ru)
    

# Courses

@dp.message(F.text == "kurslar")
async def courses_uz(message: Message):
    await message.answer("Bizning online kurlarimiz haqida to'liq ma'lumotga ega bo'ling", reply_markup=courses_kb_uz)

@dp.message(F.text == "курсы")
async def courses_ru(message: Message):
    await message.answer("Узнайте больше о наших онлайн-курсах", reply_markup=courses_kb_ru)

@dp.callback_query(F.data == "front-uz")
async def front_uz(call: CallbackQuery):
    await call.message.answer_photo(photo="https://avatars.mds.yandex.net/i?id=2c8d0a422ecbb19aa372d7d61629112cdc573b32-9868376-images-thumbs&n=13", caption="Front end kurslarimizda siz web sayt qilishni o'rganasiz. Kurs davomida html, css va javascript kabi dasturlash tillarini o'rganasiz\n\nOyiga 500000 so'm", reply_markup=front_buy)

@dp.callback_query(F.data == "front-ru")
async def front_ru(call: CallbackQuery):
    await call.message.answer_photo(photo="https://avatars.mds.yandex.net/i?id=2c8d0a422ecbb19aa372d7d61629112cdc573b32-9868376-images-thumbs&n=13", caption="На наших курсах по интерфейсу вы научитесь создавать веб-сайты. В ходе курса вы изучите такие языки программирования, как html, css и javascript\n\n500000 сум в месяц", reply_markup=front_buy)


@dp.callback_query(F.data == "front_buy")
async def front_buyer(call: CallbackQuery, state: FSMContext):
    basket_uz.append("Front-end - 500000 so'm")
    basket_ru.append("Front-end - 500000 сум")
    total.append(500000)
    data = await state.get_data()
    await call.message.answer(text="🛒")

@dp.callback_query(F.data == "back-uz")
async def back_uz(call: CallbackQuery):
    await call.message.answer_photo(photo="https://avatars.mds.yandex.net/i?id=5bc97a5ff1db93730a56d39a03aeda660bcd803c7e6a17d7-11491093-images-thumbs&n=13", caption="Back end kurslarimizda siz sun'iy intellekt yaratishni va ma'lumotlar bilan ishlashni o'rganasiz. Kurs davomida python, c++ va java kabi dasturlash tillarini o'rganasiz\n\nOyiga 700000 so'm", reply_markup=back_buy)

@dp.callback_query(F.data == "back-ru")
async def back_ru(call: CallbackQuery):
    await call.message.answer_photo(photo="https://avatars.mds.yandex.net/i?id=5bc97a5ff1db93730a56d39a03aeda660bcd803c7e6a17d7-11491093-images-thumbs&n=13", caption="На наших курсах по серверной части вы научитесь создавать искусственный интеллект и работать с данными. В ходе курса вы изучите такие языки программирования, как Python, C++ и Java\n\n700000 сум в месяц", reply_markup=back_buy)


@dp.callback_query(F.data == "back_buy")
async def back_buyer(call: CallbackQuery, state: FSMContext):
    basket_uz.append("Back-end - 700000 so'm")
    basket_ru.append("Back-end - 700000 сум")
    total.append(700000)
    data = await state.get_data()
    await call.message.answer(text="🛒")

@dp.callback_query(F.data == "dizayn-uz")
async def dizayn_uz(call: CallbackQuery):
    await call.message.answer_photo(photo="https://avatars.mds.yandex.net/i?id=fad2794480190f70ba6173fed1041724d952dc07-5487333-images-thumbs&n=13", caption="Dizayn kurslarimizda siz Photoshop va unity bilan ishlashni o'rganasiz\n\nOyiga 450000 so'm", reply_markup=dizayn_buy)

@dp.callback_query(F.data == "dizayn-ru")
async def dizayn_ru(call: CallbackQuery):
    await call.message.answer_photo(photo="https://avatars.mds.yandex.net/i?id=fad2794480190f70ba6173fed1041724d952dc07-5487333-images-thumbs&n=13", caption="На наших курсах дизайна вы научитесь работать с Photoshop и Unity\n\n450000 сум в месяц", reply_markup=dizayn_buy)


@dp.callback_query(F.data == "dizayn_buy")
async def dizayn_buyer(call: CallbackQuery, state: FSMContext):
    basket_uz.append("Dizayn - 450000 so'm")
    basket_ru.append("дизайн - 450000 сум")
    total.append(450000)
    data = await state.get_data()
    await call.message.answer(text="🛒")

@dp.callback_query(F.data == "start-uz")
async def start_uz(call: CallbackQuery):
    await call.message.answer_photo(photo="https://avatars.mds.yandex.net/i?id=59120500a885f45f599e88fc8d55a279e10985b2-12510920-images-thumbs&n=13", caption="Starter kurslarimizda siz Scratch orqali o'yinlar yaratasiz, Canva bilan turli xil dizayni ishlarni amalga oshirasiz va yana boshqa web sahifalar bilan tanishasiz\n\nOyiga 275000 so'm", reply_markup=start_buy)

@dp.callback_query(F.data == "start-ru")
async def start_ru(call: CallbackQuery):
    await call.message.answer_photo(photo="https://avatars.mds.yandex.net/i?id=59120500a885f45f599e88fc8d55a279e10985b2-12510920-images-thumbs&n=13", caption="На наших стартовых курсах вы будете создавать игры в Scratch, выполнять различные дизайнерские работы в Canva и знакомиться с другими веб-страницами\n\n275 000 сум в месяц.", reply_markup=start_buy)


@dp.callback_query(F.data == "start_buy")
async def start_buyer(call: CallbackQuery, state: FSMContext):
    basket_uz.append("Starter - 275000 so'm")
    basket_ru.append("Cтартер - 275000 сум")
    total.append(275000)
    data = await state.get_data()
    await call.message.answer(text="🛒")

@dp.message(F.text == "savatcha")
async def savat_uz(message: Message):
    global basket_uz
    global total
    if basket_uz == []:
        await message.answer("Savatcha bo'sh")
    else:
        text = ""
        price = 0
        for i in basket_uz:
            text += f"{i}\n"
        for i in total:
            price += i
        await message.answer(text=f"{text}\nUmumiy hisob - {price} so'm", reply_markup=basket_kb_uz)

@dp.message(F.text == "Sotib olish")
async def buy_uz(message: Message, state: FSMContext):
    await state.set_state(Reg.credit_num)
    await message.answer(text="Karta raqamingizni kiriting", reply_markup=ReplyKeyboardRemove())

@dp.message(Reg.credit_num)
async def credit_uz(message: Message, state: FSMContext):
    await state.update_data(credit_num=message.text)
    if str(message.text).isdigit() and len(message.text) == 16:
        await message.answer("kursni sotib olganingiz uchun rahmat", reply_markup=main_kb_uz)
        await state.clear()
        global basket_uz, basket_ru, total
        basket_ru.clear()
        basket_uz.clear()
        total.clear()
    else:
        await message.answer("ERROR")

@dp.message(F.text == "Bekor qilish")
async def decline_uz(message: Message):
    global basket_uz, basket_ru, total
    basket_ru.clear()
    basket_uz.clear()
    total.clear()
    await message.answer("Xayrli kun", reply_markup=main_kb_uz)

@dp.message(F.text == "корзина")
async def savat_ru(message: Message):
    global basket_ru
    global total
    if basket_ru == []:
        await message.answer("корзина пуста")
    else:
        text = ""
        price = 0
        for i in basket_ru:
            text += f"{i}\n"
        for i in total:
            price += i
        await message.answer(text=f"{text}\nОбщая сумма - {price} сум", reply_markup=basket_kb_ru)

@dp.message(F.text == "купить")
async def buy_uz(message: Message, state: FSMContext):
    await state.set_state(Reg.credit_num)
    await message.answer(text="введите номер вашей карты", reply_markup=ReplyKeyboardRemove())

@dp.message(Reg.credit_num)
async def credit_ru(message: Message, state: FSMContext):
    await state.update_data(credit_num=message.text)
    if str(message.text).isdigit() and len(message.text) == 16:
        await message.answer("Спасибо за покупку курса", reply_markup=main_kb_ru)
        await state.clear()
        global basket_uz, basket_ru, total
        basket_ru.clear()
        basket_uz.clear()
        total.clear()
    else:
        await message.answer("Попробуйте еще раз")

@dp.message(F.text == "отменить")
async def decline_ru(message: Message):
    global basket_uz, basket_ru, total
    basket_ru.clear()
    basket_uz.clear()
    total.clear()
    await message.answer("Хорошего тебе дня", reply_markup=main_kb_ru)

@dp.message(F.text == "Biz haqimizda")
async def about(message: Message):
    await message.answer(text="Siz bu yerda Videoni ko'rib yoki havola orqali saytga o'tib biz haqimizda bilib olishingiz mumkin", reply_markup=about_us)

@dp.message(F.text == "о нас")
async def about_ru(message: Message):
    await message.answer(text="О нас вы можете узнать посмотрев видео здесь или перейдя на сайт по ссылке", reply_markup=about_us)

@dp.callback_query(F.data == "video")
async def videomp4(call: CallbackQuery):
    yt = YouTube(url="https://youtu.be/QyhwSYhX09s?si=c2Q4gNHX0_hAf34C")
    url = yt.streams.get_highest_resolution()
    stream = url.download()
    video = FSInputFile(stream)
    await call.message.answer_video(video=video)
    os.remove(stream)

@dp.message(F.text == "Qo'llab quvvatlash")
async def support_uz(message: Message):
    await message.answer(text="Men ChatGPTman istagan savolingizni so'rang")
    user_input = message.text
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=user_input,
        max_tokens=1000,
        temperature=0.7,
    )
    await message.answer(text=f"{response.choices[0].text.strip()}")

@dp.message(F.text == "поддержка")
async def support_uz(message: Message):
    await message.answer(text="Я ChatGPT. Задавайте любые вопросы, которые хотите.")
    user_input = message.text
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=user_input,
        max_tokens=1000,
        temperature=0.7,
    )
    await message.answer(text=f"{response.choices[0].text.strip()}")

@dp.message(F.text == "Tilni o'zgartirish")
async def change_lang_uz(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("Tilni tanlang", reply_markup=lang_kb)

@dp.message(F.text == "uz")
async def lang_uz(message: Message, state: FSMContext):
    await message.answer("Til o'zgartirildi", reply_markup=main_kb_uz)
    await state.clear()

@dp.message(F.text == "изменить язык")
async def change_lang_ru(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("выберите язык", reply_markup=lang_kb)

@dp.message(F.text == "ru")
async def lang_ru(message: Message, state: FSMContext):
    await message.answer("язык изменен", reply_markup=main_kb_ru)
    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())