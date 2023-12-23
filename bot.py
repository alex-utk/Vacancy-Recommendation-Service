from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils import executor
import yaml
from httpx import AsyncClient, Response, HTTPError
import requests
import asyncio

config_file = "config/config.yaml"
with open(config_file) as f:
    config = yaml.load(f, Loader=yaml.Loader)

API_TOKEN = config['bot']['token']

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    mode = State()
    city = State()
    age = State()
    experience = State()
    years = State()
    job_type = State()
    work_description = State()
    skills = State()
    employment_type = State()
    salary_expectation = State()  # Job Seeker
    vacancy_name = State()
    vacancy_city = State()
    vacancy_salary = State()
    vacancy_years = State()
    vacancy_text = State()


@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message):
    instructions = (
        "Welcome to the Job Seeker & HR Assistance Bot!\n\n"

        "**For Job Seekers:**\n"
        "1. **Start:** Type `/start` to begin.\n"
        "2. **Select Mode:** Choose the 'Job Seeker' button.\n"
        "3. **Enter Details:** You'll be prompted for various details like City, Age, Work Experience, etc.\n"
        "4. **Receive Resume:** After entering all details, you'll receive your resume.\n\n"

        "**For HR Representatives:**\n"
        "1. **Start:** Type `/start` to begin.\n"
        "2. **Select Mode:** Choose the 'HR' button.\n"
        "3. **Enter Vacancy Details:** Enter Vacancy Name and Description.\n"
        "4. **Post Vacancy:** After entering details, the vacancy info will be displayed.\n\n"

        "Type `/start` at any point to restart. Provide accurate information for the best results.\n"
        "Thank you for using our bot!"
    )

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('HR'), KeyboardButton('Job Seeker'))
    await message.reply(instructions, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
    await Form.mode.set()


@dp.message_handler(lambda message: message.text in ['HR', 'Job Seeker'], state=Form.mode)
async def process_mode(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mode'] = message.text
    if message.text == 'HR':
        await message.reply("Введите название вакансии:", reply_markup=ReplyKeyboardRemove())
        await Form.vacancy_name.set()
    else:
        await message.reply("Пожалуйста введите ваш город:", reply_markup=ReplyKeyboardRemove())
        await Form.city.set()


@dp.message_handler(state=Form.city)
async def process_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await message.reply("Введите ваш возраст:")
    await Form.age.set()


@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.reply("Есть у вас релевантный опыт работы? (Да/Нет)")
    await Form.experience.set()


@dp.message_handler(state=Form.experience)
async def process_experience(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['experience'] = message.text
    await message.reply("Сколько лет у вас опыта работы?")
    await Form.years.set()


@dp.message_handler(state=Form.years)
async def process_years(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['years'] = message.text
    await message.reply("Полная или частичная занятость?")
    await Form.job_type.set()


@dp.message_handler(state=Form.job_type)
async def process_job_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['job_type'] = message.text
    await message.reply("Опишите ваш опыт работы:")
    await Form.work_description.set()


@dp.message_handler(state=Form.work_description)
async def process_work_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['work_description'] = message.text
    await message.reply("Опишите ваши hard skills по ключевым словам:")
    await Form.skills.set()


@dp.message_handler(state=Form.skills)
async def process_skills(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['skills'] = message.text
    await message.reply("Какие ваши ожидания по зарплате?")
    await Form.salary_expectation.set()


@dp.message_handler(state=Form.salary_expectation)
async def process_salary_expectation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['salary_expectation'] = message.text
    await message.reply("Должности, на которые претендуете?")
    await Form.employment_type.set()


@dp.message_handler(state=Form.vacancy_name)
async def process_vacancy_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['vacancy_name'] = message.text
    await message.reply("Введите город для вакансии:")
    await Form.vacancy_city.set()


@dp.message_handler(state=Form.vacancy_city)
async def process_vacancy_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['vacancy_city'] = message.text
    await message.reply("Введите ожидаемую зарплату:")
    await Form.vacancy_salary.set()


@dp.message_handler(state=Form.vacancy_salary)
async def process_vacancy_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['vacancy_salary'] = message.text
    await message.reply("Введите количество лет опыта:")
    await Form.vacancy_years.set()


@dp.message_handler(state=Form.vacancy_years)
async def process_vacancy_salary(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['vacancy_years'] = message.text
    await message.reply("Введите описание вакансии:")
    await Form.vacancy_text.set()


async def send_post_request(url: str, data: dict) -> Response:
    async with AsyncClient(follow_redirects=True) as client:
        return await client.post(url, json=data)


def send_resume_request(resume):
    response = requests.post('https://congress-brian-maker-joint.trycloudflare.com/get_vacancies/', json=resume)
    return response


async def async_send_resume_request(resume):
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, send_resume_request, resume)
    return response


# Handler for sending resume
@dp.message_handler(state=Form.employment_type)
async def process_employment_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['employment_type'] = message.text
        resume = {
            'vacancy': data['employment_type'],
            'salary': int(data['salary_expectation']),
            'experience': int(data['years']),
            'description': data['work_description'],
            'city_name': data['city']
        }
        print(resume)

    # Sending resume data to FastAPI and receiving response
    try:
        response = await send_post_request('https://congress-brian-maker-joint.trycloudflare.com/get_vacancies/',
                                           resume)

        if response.status_code == 200:
            response_data = response.json()
            vacancies_list = response_data.get("results", [])
            response_text = "Resume sent successfully! Here are some matching vacancies:\n\n"
            for vacancy in vacancies_list:
                response_text += (f"Position: {vacancy['custom_position']}, "
                                  f"Experience: {vacancy['experience']} years, "
                                  f"Salary: {vacancy['salary']}, "
                                  f"City: {vacancy['city_name']}\n")
            await message.reply(response_text, reply_markup=ReplyKeyboardRemove())
        else:
            error_message = f"Failed to send resume. Status code: {response.status_code}"
            if response.content:
                error_message += f"\nResponse content: {response.text}"
            await message.reply(error_message, reply_markup=ReplyKeyboardRemove())
    except HTTPError as e:
        await message.reply(f"An HTTP error occurred: {e}", reply_markup=ReplyKeyboardRemove())

    await state.finish()


@dp.message_handler(state=Form.vacancy_text)
async def process_vacancy_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['vacancy_text'] = message.text
        vacancy = {
            'vacancy': data['vacancy_name'],
            'salary': data['vacancy_salary'],
            'experience': data['vacancy_years'],
            'city_name': data['vacancy_city'],
            'description': data['vacancy_text']
        }

    # Sending vacancy data to FastAPI and receiving response
    try:
        response = await send_post_request('https://congress-brian-maker-joint.trycloudflare.com/get_resumes/', vacancy)

        if response.status_code == 200:
            response_data = response.json()
            resumes_list = response_data.get("results", [])
            response_text = "Vacancy posted successfully! Here are some matching resumes:\n\n"
            for resume in resumes_list:
                response_text += (f"Description: {resume['employee_description']}, "
                                  f"Position: {resume['vacancy']}, "
                                  f"Salary: {resume['salary']}, "
                                  f"Education: {resume['education']}, "
                                  f"City: {resume['city_name']}\n\n")
            await message.reply(response_text, reply_markup=ReplyKeyboardRemove())
        else:
            error_message = f"Failed to post vacancy. Status code: {response.status_code}"
            if response.content:
                error_message += f"\nResponse content: {response.text}"
            await message.reply(error_message, reply_markup=ReplyKeyboardRemove())
    except HTTPError as e:
        await message.reply(f"An HTTP error occurred: {e}", reply_markup=ReplyKeyboardRemove())

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
