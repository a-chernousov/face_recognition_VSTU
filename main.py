from typing import get_args
from xml.etree.ElementTree import tostring

from PIL.DdsImagePlugin import module
from deepface import DeepFace
import json
import telebot
from keras.src.ops import Empty
from telebot import types
import os
import numpy as np
from PIL import Image
import io

bot= telebot.TeleBot('7898992706:AAF5Dp9QPM4-0yDfAikv3Yxg06Iv66KorSU')
photo_folder = os.path.abspath('E:\\py_bot\\FaceRecognition\\userPhotos')

# В список дописывать id пользователей
allowed_ids = [959633736, #Андрей 6
                751997349,
                5690909942,
                998654872,
                826468586,
                814249133
               ]  # Замените на реальные ID

# Словарь для хранения фотографий пользователей
saved_photos = {}

@bot.message_handler(commands=['start', 'START', 'info', 'INFO', 'help'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('more info', callback_data='inf')
    user_id = message.chat.id
    if user_id not in allowed_ids:
        btn1 = types.InlineKeyboardButton('ID', callback_data='ID')
        markup.add(btn1, btn2)
    else: markup.add(btn2)
    if user_id not in allowed_ids:
        bot.send_message(message.chat.id,
                'Нажмите на <b>ID</b>, чтобы получить свой уникальный <b>ID</b> для дальнейшего использования бота \n'
                    'Отправьте свой ID администратору для активации бота',
                     parse_mode='html',
                     reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                         'Если вы видете это сообщение, значит вы зарегестрированы \n'
                         'Чтобы определить студента по фото, отправьте фотографию и напишите команду <b>/recognition </b>',
                         parse_mode='html',
                         reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_ID(callback):
    if callback.data == 'ID':
        bot.send_message(callback.message.chat.id, f'Ваш ID: {callback.message.chat.id}\n'
                                                   f'После регестрации введите команду <b>/info</b>')
    elif callback.data == 'inf':
        bot.send_message(callback.message.chat.id,
                    f'Этот бот создан для совместной разработки группой <i>БПИЭ-221, ВГТУ, ВОРОНЕЖ, 2024г</i>\n'
                        f'<b>Цель бота</b> - определить студента из группы по фотографии',
                         parse_mode='html')

# Обработчик для фотографий
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.chat.id
    if user_id in allowed_ids:
        # Получаем фотографию с наибольшим размером
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохраняем фотографию в словарь с ключом user_id
        saved_photos[user_id] = downloaded_file

        # Сохраняем фотографию на диск
        photo_path = os.path.join(photo_folder, f'photo_{user_id}.jpg')
        with open(photo_path, 'wb') as photo_file:
            photo_file.write(downloaded_file)

        bot.send_message(user_id, 'Фотография успешно сохранена.')
    else:
        bot.send_message(user_id, 'У вас нет доступа к отправке фотографий.')

# Команда для отправки сохраненной фотографии
@bot.message_handler(commands=['recognition'])
def send_photo(message):
    user_id = message.chat.id
    bot.send_message(user_id, 'Происходит магия')
    if user_id in allowed_ids:
        # Путь к сохраненной фотографии
        photo_path = os.path.join(photo_folder, f'photo_{user_id}.jpg')

        if os.path.exists(photo_path):
            # Отправляем сохраненную фотографию
            with open(photo_path, 'rb') as photo_file:
                recognition_result = face_recogn(message)
                bot.send_message(user_id, recognition_result)
        else:
            bot.send_message(user_id, 'Вы не отправили фотографию.')
    else:
        bot.send_message(user_id, 'У вас нет доступа к этой команде.')


def face_recogn(message):
    try:
        user_id = message.chat.id
        img_path = os.path.join(photo_folder, f'photo_{user_id}.jpg')
        db_path = "faceBPI"

        DeepFace.build_model("Facenet")
        result = DeepFace.find(img_path=img_path, db_path=db_path)

        # int_counter = tostring(result[0]).find('_')
        # substring = result[0][int_counter + len("World")]
        # print(substring)

        result_pars(result)

        return result
    except Exception as err:
        print(err)
        return "Лицо не распознано"

def result_pars(result):
    print("--------------------")
    print(result)
    print('--------------------')




bot.polling(none_stop=True)

# def face_recogn(message):
#     try:
#         user_id = message.chat.id
#         photo_path = os.path.join(photo_folder, f'photo_{user_id}.jpg')
#         db_path = "faceBPI"
#
#         DeepFace.build_model("Facenet")
#
#         # Добавляем параметр enforce_detection=False
#         result = DeepFace.find(photo_path, db_path=db_path, enforce_detection=False)
#
#         if result.empty:
#             return "Лицо не распознано"
#         else:
#             return f"Лицо распознано: {result}"
#     except Exception as err:
#         print("error")
#         return str(err)



#
# def face_verify(img_1, img_2):
#     try:
#         result_dict = DeepFace.verify(img1_path=img_1, img2_path=img_2, model_name='Facenet512')
#
#         with open('result.json', 'w') as file:
#             json.dump(result_dict, file, indent=4, ensure_ascii=False)
#
#         return result_dict
#     except Exception as _ex:
#         return _ex
#
# def face_recogn():
#     try:
#         img_path = "faceBPItest/img_3.png"
#         db_path = "faceBPI"
#
#         DeepFace.build_model("Facenet")
#
#         result = DeepFace.find(img_path=img_path, db_path=db_path)
#         return result
#     except Exception as err:
#         return err
#
#
# def face_analyze():
#     try:
#         # result_dict = DeepFace.analyze(img_path='faceBPI/img.png', actions=['age', 'gender', 'race', 'emotion'])
#         result_list = DeepFace.analyze(img_path='faceBPI/img.png', actions=['age', 'gender', 'race'])
#
#         for i, result_dict in enumerate(result_list):
#             print(f'[+] Лицо {i + 1}:')
#             print(f'[+] Возраст: {result_dict.get("age")}')
#             print(f'[+] Пол: {result_dict.get("gender")}')
#
#             print('[+] Раса:')
#             for k, v in result_dict.get('race').items():
#                 print(f'{k} - {round(v, 2)}%')
#
#         # print('[+] Emotions:')
#         # for k, v in result_dict.get('emotion').items(): print(f'{k} - {round(v, 2)}*')
#
#         with open('face_analyze.json', 'w') as file:
#             json.dump(result_dict, file, indent=4, ensure_ascii=False)
#
#         # return result_dict
#     except Exception as err:
#         return err
#
# def main():
#     # print(face_verify(img_1='faceBPItest/img_7.png', img_2='faceBPItest/img_6.png'))
#     # print(face_recogn())
#     print(face_analyze())
#
# if __name__ == "__main__":
#     main()
#
#
# def face_verify(img_1, img_2):
#
#     try:
#         result_dict = DeepFace.verify(img1_path=img_1, img2_path=img_2, model_name='Facenet512')
#
#         with open('result.json', 'w') as file:
#             json.dump(result_dict, file, indent=4, ensure_ascii=False)
#
#         return result_dict
#     except Exception as _ex:
#         return _ex
#
# def face_recogn():
#     try:
#         img_path = "faceBPItest/img_3.png"
#         db_path = "faceBPI"
#
#         DeepFace.build_model("Facenet")
#
#         result = DeepFace.find(img_path=img_path, db_path=db_path)
#         return result
#     except Exception as err:
#         return err
#
#
# def face_analyze():
#     try:
#         # result_dict = DeepFace.analyze(img_path='faceBPI/img.png', actions=['age', 'gender', 'race', 'emotion'])
#         result_list = DeepFace.analyze(img_path='faceBPI/img.png', actions=['age', 'gender', 'race'])
#
#         for i, result_dict in enumerate(result_list):
#             print(f'[+] Лицо {i + 1}:')
#             print(f'[+] Возраст: {result_dict.get("age")}')
#             print(f'[+] Пол: {result_dict.get("gender")}')
#
#             print('[+] Раса:')
#             for k, v in result_dict.get('race').items():
#                 print(f'{k} - {round(v, 2)}%')
#
#         # print('[+] Emotions:')
#         # for k, v in result_dict.get('emotion').items(): print(f'{k} - {round(v, 2)}*')
#
#         with open('face_analyze.json', 'w') as file:
#             json.dump(result_dict, file, indent=4, ensure_ascii=False)
#
#         # return result_dict
#     except Exception as err:
#         return err
#
# def main():
#     # print(face_verify(img_1='faceBPItest/img_7.png', img_2='faceBPItest/img_6.png'))
#     # print(face_recogn())
#     print(face_analyze())
#
#
#
#
# if __name__ == "__main__":
#     main()