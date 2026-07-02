import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# ⚠️ ВСТАВЬ СВЕЖИЙ ТОКЕН ОТ BOTFATHER СЮДА (после сброса старого!)
BOT_TOKEN = "8881460663:AAHJAJ9hhXBFk5Jol_relmE0Dp3nIxz2ia4"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Описываем состояния опроса (FSM)
class AuditStates(StatesGroup):
    experience = State()
    main_pain = State()

# --- КНОПКИ ---
def get_experience_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Нет, только планирую разобраться")],
            [KeyboardButton(text="🏦 Да, пользуюсь биржами (Binance, Bybit)")],
            [KeyboardButton(text="🔒 Да, храню на кошельках (Metamask, Ledger)")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_pain_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛑 Боюсь блокировок, проверок AML и грязных монет")],
            [KeyboardButton(text="⚙️ Нужна автоматизация (скрипты, p2p-процессинг)")],
            [KeyboardButton(text="💸 Теряю огромные сумму на комиссиях сетей")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# --- ЛОГИКА ---

# 1. Старт бота
@dp.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):
    await state.clear() # Сбрасываем старые состояния
    
    welcome_text = (
        "🤖 *SYSTEM LOG: SESSION INITIALIZED*\n\n"
        f"Welcome to Core Intelligence node, {message.from_user.first_name}.\n\n"
        "Этот автоматизированный протокол позволит провести интерактивный аудит рисков и безопасности "
        "вашей текущей инфраструктуры цифровых активов.\n\n"
        "*Пожалуйста, выберите ваш текущий статус работы с активами:*"
    )
    await message.answer(welcome_text, reply_markup=get_experience_keyboard(), parse_mode="Markdown")
    await state.set_state(AuditStates.experience)

# 2. Обработка первого вопроса (Опыт)
@dp.message(AuditStates.experience)
async def process_experience(message: types.Message, state: FSMContext):
    user_answer = message.text or ""
    
    if "Нет, только планирую" in user_answer:
        await state.update_data(segment="beginner")
        offer_text = (
            "⚠️ *Ваш уровень риска: ВЫСОКИЙ (Отсутствие базы)*\n\n"
            "Без понимания матчасти вы можете потерять активы при первой же транзакции "
            "из-за фишинга или отправки не в ту сеть.\n\n"
            "📘 Специально для вас я подготовил закрытый видео-разбор: "
            "«Безопасный старт в Web3 для бизнеса и физлиц». Там пошагово показано, как "
            "создать защищенный кошелек, у которого никто не отберет доступ."
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎁 Получить разбор бесплатно", url="https://t.me/fisherswap")]
        ])
        await message.answer(offer_text, reply_markup=kb, parse_mode="Markdown")
        await state.clear()
        
    elif "Да, пользуюсь" in user_answer or "Да, храню" in user_answer:
        segment = "middle" if "биржами" in user_answer else "advanced"
        await state.update_data(segment=segment)
        
        await message.answer(
            "Принято. Базовые навыки у вас есть. Теперь выберите, какая *главная техническая или юридическая сложность* стоит перед вами сейчас?",
            reply_markup=get_pain_keyboard()
        )
        await state.set_state(AuditStates.main_pain)
    else:
        await message.answer("Пожалуйста, выберите один из вариантов на кнопках.")

# 3. Обработка второго вопроса + Закрытие на оффер
@dp.message(AuditStates.main_pain)
async def process_pain(message: types.Message, state: FSMContext):
    pain = message.text or ""
    
    if "Боюсь блокировок" in pain:
        response = (
            "🛡️ *Анализ риска: Уязвимость перед AML-сервисами*\n\n"
            "Биржи и мерчанты используют жесткий софт (Chainalysis, Crystal). Если к вам придет монета, "
            "которая 5 транзакций назад была в миксере — ваш аккаунт заблокируют без права апелляции.\n\n"
            "Вам необходим аудит вашей инфраструктуры. Напишите нашему инженеру фразу **'АМЛ АУДИТ'**, "
            "чтобы получить разбор вашей схемы переводов и закрыть уязвимости."
        )
    elif "Нужна автоматизация" in pain:
        response = (
            "⚙️ *Анализ задачи: Оптимизация процессов и автоматизация*\n\n"
            "Ручные переводы и p2p-ордера — это потеря времени и риск человеческой ошибки. Для объемов "
            "нужно разворачивать локальные скрипты мониторинга сети и автоматического сбора транзакций.\n\n"
            "Свяжитесь с нашим ведущим разработчиком. Мы покажем рабочие кейсы автоматизации p2p-процессинга "
            "под ключ под ваши задачи. Напишите в личку: **'АВТОМАТИЗАЦИЯ'**."
        )
    elif "Теряю огромные суммы" in pain:
        response = (
            "💸 *Анализ задачи: Оптимизация смарт-контрактов и комиссий*\n\n"
            "Переводы в сети Ethereum/Tron при больших объемах сжигают тысячи долларов в месяц на пустом месте. "
            "Существуют легальные инженерные методы оптимизации кастодиальных решений и снижения Gas Fee.\n\n"
            "Запишитесь на техническую консультацию. Напишите кодовое слово **'КОМИССИИ'**."
        )
    else:
        await message.answer("Пожалуйста, используйте кнопки для ответа.")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Связаться с экспертом напрямую", url="https://t.me/fisherswap")]
    ])
    await message.answer(response, reply_markup=kb, parse_mode="Markdown")
    await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
