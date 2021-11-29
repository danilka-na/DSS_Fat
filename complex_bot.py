from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import time
from standardfuncs import create_new_patient
from standardfuncs import print_patient
from standardfuncs import set_dict_to_patient
from standardfuncs import set_patient
from standardfuncs import Patient
import numpy as np

token = '2139315889:AAH5MZWTQQhnNOE6LpIOSYAxkaFq9ubB4Bk'


last_question = {}
answers = {}

def options1(bot, update):
    global last_question

    options = ["Ввод данных вручную", "Загрузка файла"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' Выберите способ ввода данных', reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'options1'

def Sex(bot, update):
    global last_question

    options = ["Жен", "Муж"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' Выберете пол', reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'Sex'



def standardfuncs_set_patient_set_age(bot, update):
    global answers

    answers[bot.message.chat_id]["set_age"] = set_patient(answers[bot.message.chat_id]["Age"], "age")
    bot.message.reply_text(" Введите рост в метрах")
    last_question[bot.message.chat_id] = "Height"

def standardfuncs_create_new_patient_create_patient(bot, update):
    global answers
    global patient
    patient = create_new_patient(answers[bot.message.chat_id]["options1"])
    Sex(bot, update)

def standardfuncs_print_patient_debug_print(bot, update):
    global answers
    answers[bot.message.chat_id]["debug_print"] = print_patient()
    bot.message.reply_text(" Все")
    last_question[bot.message.chat_id] = "Name3"

def standardfuncs_set_dict_to_patient_sex_m(bot, update):
    global answers
    answers[bot.message.chat_id]["sex_m"] = set_dict_to_patient(answers[bot.message.chat_id]["Sex"],{"sex":0})
    bot.message.reply_text(" Введите возраст в годах")
    last_question[bot.message.chat_id] = "Age"

def standardfuncs_set_dict_to_patient_sex_w(bot, update):
    global answers
    answers[bot.message.chat_id]["sex_w"] = set_dict_to_patient(answers[bot.message.chat_id]["Sex"],{"sex":1})
    bot.message.reply_text(" Введите возраст в годах")
    last_question[bot.message.chat_id] = "Age"

def standardfuncs_set_patient_set_height(bot, update):
    global answers
    answers[bot.message.chat_id]["set_height"] = set_patient(answers[bot.message.chat_id]["Height"], "height")
    bot.message.reply_text(" Введите вес в кг")
    last_question[bot.message.chat_id] = "Weight"

def standardfuncs_set_patient_set_weight(bot, update):
    global answers
    answers[bot.message.chat_id]["set_weight"] = set_patient(answers[bot.message.chat_id]["Weight"], "weight")
    print_IMT(bot)

def print_IMT(bot):
    bmi = patient["weight"]/(patient["height"]**2)
    patient['bmi'] = bmi

    bot.message.reply_text(f" ИМТ пациента: {patient['bmi']}")

    if bmi<18:
        bot.message.reply_text(f"Ожирение отсутсвует. Возможны сопутсвующие заболевания в связи с низким "
                               f"ИМТ")
        updater.idle()
    if bmi>18 and bmi<=24:
        bot.message.reply_text(f"Ожирение отсутсвует. ИМТ в норме")
        updater.idle()
    if bmi>24 and bmi<30:
        bot.message.reply_text(f"Пациент находится в зоне риска, нужны рекомендации по уменьшению веса.")
        updater.idle()
    if bmi>30:
        bot.message.reply_text(f"У пациента ожирение")
        bot.message.reply_text(" Введите размер талии в см")
        last_question[bot.message.chat_id] = "waist_size"


def waist_size(bot, update):

    waist = answers[bot.message.chat_id]["waist_size"]
    waist = set_patient(waist, "waist")
    patient['visceral'] = 0

    if waist>80 and patient['sex']==1:
        patient['visceral'] == 1

    if waist > 94 and patient['sex'] == 0:
        patient['visceral'] == 1

    if patient['visceral'] == 1:
        bot.message.reply_text(f"У пациента висцеральное ожирение")
    bot.message.reply_text(" Введите текущее потребление каллорий для пациента в ккал")
    last_question[bot.message.chat_id] = "calories"

def calculate_calories(bot, update):
    waist = answers[bot.message.chat_id]["calories"]
    set_patient(waist, "current_calories")

    anamnez(bot, update)
def get_recomendation_string(letter, num):
    return f"Уровень убедительности рекомендаций {letter} (уровень достоверности " \
           f"доказательств – {num})"

def anamnez(bot, update):
    last_question[bot.message.chat_id] = "anamnez"
    bot.message.reply_text(" Начало диагностики")
    AG(bot, update)


def AG(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' У пациента есть Артериальная Гипертензия?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'AG'

def cvd(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' У пациента есть Ишимическая болезнь сердца?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'cvd'

def chf(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' У пациента есть Хроническая сердечная недостаточность?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'chf'


def pancreatitis(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' У пациента есть Панкреатит?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'pancreatitis'

def mtc(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' У пациента есть Медулярный рак щитовидной железы?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'mtc'

def cholelithiasis(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' У пациента есть Желчекаменная болезнь?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'cholelithiasis'

def cholestasis(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' У пациента есть Холестаз?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'cholestasis'

def gastrointestinal_diseases(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' У пациента есть Заболевания ЖКТ?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'gastrointestinal_diseases'

def prediabetes(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' У пациента есть Предиабет?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'prediabetes'

def eco(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' У пациента есть Экзогенно-конституциональное ожирение?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'eco'

def life_modification(bot, update):

    last_question[bot.message.chat_id] = 'life_modification'
    bot.message.reply_text(' Пациенту необходимо изменить образ жизни. Так же '
                           'рекомендуется снижение массы тела на  5-10%  за  3–6  '
                           'месяцев  терапии  и  удержание результата  в  течение  года ')
    bot.message.reply_text(get_recomendation_string("B", 2))
    bot.message.reply_text(' Терапия включает в себя расширения объема физических '
                           'нагрузок и гипокаллорийная диета (дефицит 500-700 ккал от '
                           'физиологической потребности) ')
    bot.message.reply_text(' Цель: привести ИМТ к целевым значениям')
    bot.message.reply_text(get_recomendation_string("A", 2))

    bot.message.reply_text(' Проверка результатов через 3 месяца')

    time.sleep(3)

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' Прошло 3 месяца?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'visit_2'

def visit_2(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' Есть снижение массы тела на 5-10%?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'visit_2_q'
    time.sleep(3)

def visit_3(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' Есть снижение массы тела на 5-10%?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'visit_3_q'

def additional_consultation(bot, update):
    bot.message.reply_text(' Необходимо направить пациента на дополнительную '
                           'консультацию к Эндокринологу')
    last_question[bot.message.chat_id] = 'end'

def all_well(bot, update):
    bot.message.reply_text(' Терапия работает. Нужна повторная явка через 3 месяца')
    last_question[bot.message.chat_id] = 'end'

def drug_avaliable(drug_name):
    dct = {
        'ah': np.array([True, False, True]),
        'cvd': np.array([True, False, True]),
        'chf': np.array([True, False, True]),
        'pancreatitis': np.array([True, True, False]),
        'mtc': np.array([True, True, False]),
        'cholelithiasis': np.array([False, True, False]),
        'cholestasis': np.array([False, True, True]),
        'gastrointestinal_diseases': np.array([False, True, True]),
        'prediabetes': np.array([True, True, True])
    }
    return dct[drug_name]

def get_drug_by_mask(mask):
    drugs = np.array(['Орлистат', "Сибутрамин", "Лираглутид"])
    return drugs[mask]

def get_drug_for_patient(patient):
    call_name = ['ah', 'cvd', 'chf','pancreatitis','mtc','cholelithiasis','cholestasis',
    'gastrointestinal_diseases', 'prediabetes']
    arr = list()
    for call in call_name:
        if call in patient:
            if patient[call] == 1:
                arr.append(drug_avaliable(call))
    result = np.array([True, True, True])
    for a in arr:
        result = result*a

    drugs = get_drug_by_mask(result)
    if len(drugs)<1:
        drugs = None
    return drugs

def drugs(bot, update):

    bot.message.reply_text(' Рекомендуется медикаментозная терапия')
    time.sleep(1)
    bot.message.reply_text(' Идет подбор препарата.....')
    time.sleep(3)
    drugs = get_drug_for_patient(patient)

    if drugs is None:
        bot.message.reply_text(' Невозможно выбрать препарат из-за конфликта по '
                               'заболеваниям.')
        bot.message.reply_text(' Рекомендуется выбрать препарат самостоятельно')

    else:
        string = ""
        for i in drugs:
            string+= f" {i}"
        bot.message.reply_text(f" Рекомендуемые препараты {string}")
    bot.message.reply_text(f" Проверка результатов через 3 месяца")
    time.sleep(3)
    global last_question
    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' Прошло 3 месяца?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'visit_3'


def visit_4(bot, update):
    global last_question

    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' Есть снижение массы тела на 5-10%?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'visit_4_q'

def drug_change(bot, update):

    bot.message.reply_text(' Рекомендуется смена препарата  на один из ниже предложенных')
    drugs = get_drug_for_patient(patient)

    if drugs is None:
        bot.message.reply_text(' Невозможно выбрать препарат из-за конфликта по '
                               'заболеваниям.')
        bot.message.reply_text(' Рекомендуется выбрать препарат самостоятельно')

    else:
        string = ""
        for i in drugs:
            string += f" {i}"
        bot.message.reply_text(f" Рекомендуемые препараты: {string}")

    bot.message.reply_text(f" Проверка результатов через 3 месяца")
    time.sleep(3)
    global last_question
    options = ["Нет", "Да"]
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(option, callback_data=option)])
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.message.reply_text(' Прошло 3 месяца?',
                           reply_markup=reply_markup)
    last_question[bot.message.chat_id] = 'visit_4'

def surgery(bot, update):
    update.idle()
    bot.message.reply_text(f" Для лечения ожирения необходимо хирургическое "
                           f"вмешательство!")
    last_question[bot.message.chat_id] = 'end'

def start(bot, update):
    global last_question
    global answers
    answers[bot.message.chat_id] = {}
    last_question[bot.message.chat_id] = ''
    bot.message.reply_text("СППР для диагностики Ожирения Ссылка на клинические рекомендации (https://rae-org.ru/system/files/documents/pdf/ozhirenie_vzroslye.pdf)")
    options1(bot, update)

def patient_set_0_dict_parameter(name):
    set_dict_to_patient(dct={name:0})

def patient_set_1_dict_parameter(name):
    set_dict_to_patient(dct={name:1})

def patient_set_2_dict_parameter(name):
    set_dict_to_patient(dct={name:1})



def buttons(bot, update):
    global last_question
    global answers
    query = bot.callback_query
    answer = "Нет"
    if last_question[query.message.chat_id] == 'options1':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        if answer == 'Ввод данных вручную':
             standardfuncs_create_new_patient_create_patient(query, update)
        if answer == 'Загрузка файла':
             query.message.reply_text(" Файл должен быть в формате  .csv")
             last_question[query.message.chat_id] = "CSV_file"
             

    if last_question[query.message.chat_id] == 'Sex':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        if answer == 'Жен':
             standardfuncs_set_dict_to_patient_sex_w(query, update)
        if answer == 'Муж':
             standardfuncs_set_dict_to_patient_sex_m(query, update)

    if last_question[query.message.chat_id] == 'AG':
        time.sleep(3)
        answer = query.data
        parameter = "ah"
        if answer == 'Нет':
             patient_set_0_dict_parameter(parameter)
        if answer == 'Да':
             patient_set_1_dict_parameter(parameter)

        cvd(query, update)

    if last_question[query.message.chat_id] == 'cvd':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "cvd"
        if answer == 'Нет':
             patient_set_0_dict_parameter(parameter)
        if answer == 'Да':
             patient_set_1_dict_parameter(parameter)

        chf(query, update)

    if last_question[query.message.chat_id] == 'chf':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "chf"
        if answer == 'Нет':
             patient_set_0_dict_parameter(parameter)
        if answer == 'Да':
             patient_set_1_dict_parameter(parameter)

        pancreatitis(query, update)

    if last_question[query.message.chat_id] == 'pancreatitis':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "pancreatitis"
        if answer == 'Нет':
             patient_set_0_dict_parameter(parameter)
        if answer == 'Да':
             patient_set_1_dict_parameter(parameter)

        mtc(query, update)

    if last_question[query.message.chat_id] == 'mtc':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "mtc"
        if answer == 'Нет':
             patient_set_0_dict_parameter(parameter)
        if answer == 'Да':
             patient_set_1_dict_parameter(parameter)

        cholelithiasis(query, update)

    if last_question[query.message.chat_id] == 'cholelithiasis':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "cholelithiasis"
        if answer == 'Нет':
             patient_set_0_dict_parameter(parameter)
        if answer == 'Да':
             patient_set_1_dict_parameter(parameter)

        cholestasis(query, update)

    if last_question[query.message.chat_id] == 'cholestasis':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "cholestasis"
        if answer == 'Нет':
             patient_set_0_dict_parameter(parameter)
        if answer == 'Да':
             patient_set_1_dict_parameter(parameter)

        gastrointestinal_diseases(query, update)

    if last_question[query.message.chat_id] == 'gastrointestinal_diseases':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "gastrointestinal_diseases"
        if answer == 'Нет':
             patient_set_0_dict_parameter(parameter)
        if answer == 'Да':
             patient_set_1_dict_parameter(parameter)

        prediabetes(query, update)

    if last_question[query.message.chat_id] == 'prediabetes':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "prediabetes"
        if answer == 'Нет':
             patient_set_0_dict_parameter(parameter)
        if answer == 'Да':
             patient_set_1_dict_parameter(parameter)

        eco(query, update)

    if last_question[query.message.chat_id] == 'eco':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "eco"
        if answer == 'Нет':
            patient_set_0_dict_parameter(parameter)
            additional_consultation(query, update)
        if answer == 'Да':
            patient_set_1_dict_parameter(parameter)
            patient_set_1_dict_parameter("visit_1")
            life_modification(query, parameter)

    if last_question[query.message.chat_id] == 'visit_2':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "visit_2"
        if answer == 'Нет':
            query.message.reply_text(' Должно пройти 3 месяца')
            patient_set_0_dict_parameter(parameter)
            last_question[query.message.chat_id] = 'end'
        if answer == 'Да':
            patient_set_1_dict_parameter(parameter)
            visit_2(query, parameter)



    if last_question[query.message.chat_id] == 'visit_2_q':
        patient = print_patient()
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        if answer == 'Нет':
            drugs(query, parameter)
        if answer == 'Да':
            drugs(query, parameter)


    if last_question[query.message.chat_id] == 'visit_3':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "visit_3"
        if answer == 'Нет':
            patient_set_0_dict_parameter(parameter)
            query.message.reply_text(' Должно пройти 3 месяца')
            last_question[query.message.chat_id] = 'end'
        if answer == 'Да':
            patient_set_1_dict_parameter(parameter)
            visit_3(query, parameter)


    if last_question[query.message.chat_id] == 'visit_3_q':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "visit_3_q"
        if answer == 'Нет':
            drug_change(query, parameter)
        if answer == 'Да':
            all_well(query, parameter)


    if last_question[query.message.chat_id] == 'visit_4':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "visit_4"
        if answer == 'Нет':
            query.message.reply_text(' Должно пройти 3 месяца')
            last_question[query.message.chat_id] = 'end'
            patient_set_0_dict_parameter(parameter)
        if answer == 'Да':
            patient_set_0_dict_parameter(parameter)
            visit_4(query, parameter)

    if last_question[query.message.chat_id] == 'visit_4_q':
        time.sleep(3)
        answer = query.data
        answers[query.message.chat_id][last_question[query.message.chat_id]] = answer
        parameter = "visit_4_q"
        if answer == 'Нет':
            surgery(query, parameter)
        if answer == 'Да':
            all_well(query, parameter)










def text(bot, update):
    global last_question
    global answers
    got_answer = False
    if last_question[bot.message.chat_id] == 'Age' and not got_answer:
        answers[bot.message.chat_id][last_question[bot.message.chat_id]] = bot.message.text
        standardfuncs_set_patient_set_age(bot, update)

        got_answer = True
    if last_question[bot.message.chat_id] == 'Height' and not got_answer:
        answers[bot.message.chat_id][last_question[bot.message.chat_id]] = bot.message.text
        standardfuncs_set_patient_set_height(bot, update)

        got_answer = True
    if last_question[bot.message.chat_id] == 'Weight' and not got_answer:
        answers[bot.message.chat_id][last_question[bot.message.chat_id]] = bot.message.text
        standardfuncs_set_patient_set_weight(bot, update)

        got_answer = True

    if last_question[bot.message.chat_id] == 'waist_size' and not got_answer:
        answers[bot.message.chat_id][last_question[bot.message.chat_id]] = bot.message.text
        waist_size(bot, update)
        got_answer = True

    if last_question[bot.message.chat_id] == 'calories' and not got_answer:
        answers[bot.message.chat_id][last_question[bot.message.chat_id]] = bot.message.text
        calculate_calories(bot, update)
        got_answer = True

updater = Updater(token=token)

dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)



text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(text_handler)

buttons_handler = CallbackQueryHandler(buttons)
dispatcher.add_handler(buttons_handler)

while True:
    try:
        updater.start_polling()
        updater.idle()

    except Exception as e:
        time.sleep(5)