# Для работы необходимо установить одну внешнюю библиотеку Telebot
# pip install pyTelegramBotAPI
import os
import time
import telebot
from telebot import types

# Укажем токен телеграм-бота из BotFather'а и зададим режим форматирования (parse_mode) с помощью HTML-тегов.
bot = telebot.TeleBot(token='Токен из Телеграм', parse_mode='html')
# Массив с доступными расширениями файлов. Можно изменить, и добавятся/удалятся кнопки выбора на клавиатуре.
formats = ['.jpg', '.png', '.svg', '.gif', '.ico', '.mp4', '.avi', '.webm', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.pdf', '.css', '.html', '.js', '.json', '.zip', '.rar']

# Добавим меню кастомных команд, и пропишем туда стандартную команду /start. С её помощью можно будет перезапустить бота и начать по-новой.
bot.set_my_commands([types.BotCommand('/start', 'перезапуск бота')])

# Начальный шаг #1. Функция приветствия, приветствует пользователя и предлагает выбрать расширение файла.
# С помощью хэндлера говорим, что данная функция будет запускаться при первом контакте с ботом командой /start.
@bot.message_handler(commands=['start'])
def welcome(message):
	# Получаем имя пользователя Telegram, чтобы можно было обратиться к нему по имени.
	username = message.from_user.first_name
	
	# Добавляем клавиатуру под поле ввода сообщения. Там отрисуются все кнопки из массива с расширениями.
	# Максимум будет 5 кнопок в ряд (параметр row_width=5).
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(*formats, row_width=5)

	# Отправляем приветственное сообщение.
	reply = bot.send_message(message.chat.id, f"Привет, <b>{username}</b>! 👋🏻\nЯ бот-генератор тестовых файлов. Помогу тебе проверить граничные значения при загрузке файлов разного веса в приложениях и на веб-сайтах. Я умею генерировать файлы различных расширений размерами от 1 байта до 45 мегабайт включительно.\n\nЧтобы начать, выбери одно из доступных расширений в меню ниже ⬇️", reply_markup=markup)

	# Регистрируем переход на следующий шаг #2. Введенный пользователем ответ будет обрабатываться в функции check_format().
	bot.register_next_step_handler(reply, check_format)

# Шаг #2. Проверка выбранного расширения. Если всё хорошо, отправляется сообщение с выбором единицы измерения.
def check_format(message):
	# Проверим, если на данном шаге получаем от пользователя команду "Вернуться в начало" или "/start".
	if (message.text == 'Вернуться в начало' or message.text == '/start'):
		# То возвращаемся на первый начальный шаг.
		welcome(message)

	# Иначе, проверяем расширение из сообщения, есть ли такое в нашем массиве с расширениями.
	elif (message.text in formats):
		# Добавляем клавиатуру с кнопками выбора единицы измерения.
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		markup.add("B (байты)", "KB (килобайты)", "MB (мегабайты)", "Вернуться в начало")

		# Отправляем сообщение с предложением выбрать единицу измерения.
		reply = bot.send_message(message.chat.id, f"🔹 Выбранное расширение — <b>{message.text}</b>\n\nТеперь выбери единицу измерения.\n<u>Небольшая памятка по размерам:</u>\n1 килобайт = 1 024 байта\n1 мегабайт = 1 024 килобайта = 1 048 576 байт", reply_markup=markup)

		# Регистрируем переход на следующий шаг #3. Введенный пользователем ответ будет обрабатываться в функции check_unit().
		# Дополнительно передаем туда объект текущего обработанного сообщения от пользователя (message).
		# Это позволит сохранить выбранное расширение для дальнейших шагов.
		bot.register_next_step_handler(reply, check_unit, message)

	# Иначе, если такого расширения не оказалось в массиве, отправляем сообщение с ошибкой и предложением выбрать корректное.
	else:
		# Добавляем клавиатуру с кнопками расширений из нашего массива, как на первом шаге.
		# Дополнительно в конце добавим кнопку "Вернуться в начало" для возврата на начальный шаг.
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		markup.add(*formats, row_width=5)
		markup.add("Вернуться в начало")

		# Отправляем сообщение с ошибкой.
		reply = bot.send_message(message.chat.id, f"Выбрано неверное расширение файла, пожалуйста выбери одно из меню ниже 🙂⬇️", reply_markup=markup)

		# Регистрируем переход снова на шаг #2. Введенный пользователем ответ будет обрабатываться в функции check_format().
		bot.register_next_step_handler(reply, check_format)

# Шаг #3. Проверка выбранной единицы измерения. Если всё хорошо, отправляется сообщение предложением ввести размер файла.
def check_unit(message, format):
	# Проверим, если на данном шаге получаем от пользователя команду "Назад".
	if (message.text == 'Назад'):
		# То возвращаемся на шаг #2 "Проверка расширения".
		# Дополнительн передаем сообщение с выбранным расширением (format), что оно сохранилось и не пришлось выбирать по-новой.
		check_format(format)
	
	# Иначе проверим, если на данном шаге получаем от пользователя команду "Вернуться в начало" или "/start".
	elif (message.text == 'Вернуться в начало' or message.text == '/start'):
		# То возвращаемся на первый начальный шаг.
		welcome(message)

	# Иначе
	elif (message.text in ['B (байты)', 'KB (килобайты)', 'MB (мегабайты)']):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		markup.add('Назад', 'Вернуться в начало')
		
		# Отправляем сообщение с предложением ввести размер файла.
		reply = bot.send_message(message.chat.id, f"🔹 Выбранное расширение — <b>{format.text}</b>\n🔹 Единица измерения — <b>{message.text}</b>\n\nОстался последний шаг, напиши размер файла. Я принимаю только целые числа, без пробелов и прочих символов.\n⛔️ <u>Ограничения по размеру:</u>\n<b>Минимум</b> — 1 байт\n<b>Максимум</b> — 45 MB (это 46 080 KB или 47 185 920 байт)", reply_markup=markup)

		# Регистрируем переход на следующий шаг #4. Введенный пользователем ответ будет обрабатываться в функции check_size().
		# Дополнительно передаем туда сообщение с выбранным расширением (format), чтобы сохранить его.
		# И также передаем туда сообщение с выбранной единицой измерения (message), чтобы сохранить её.
		bot.register_next_step_handler(reply, check_size, format, message)
	
	# Иначе, если единица измерения неверная, отправляем сообщение с ошибкой и предложением выбрать корректную.
	else:
		# Добавляем клавиатуру с кнопками выбора единицы измерения: байты, килобайты или мегабайты.
		# Также внизу добавляем кнопку "Вернуться в начало", она вернет на первый начальный шаг.
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		markup.add('B (байты)', 'KB (килобайты)', 'MB (мегабайты)', 'Вернуться в начало')

		# Отправляем сообщение с ошибкой.
		reply = bot.send_message(message.chat.id, f"Неверная единица измерения. Пожалуйста, выбери одну из меню ниже 🙂", reply_markup=markup)
		
		# Регистрируем переход снова на шаг #3. Введенный пользователем ответ будет обрабатываться в функции check_unit().
		# Дополнительно передаем туда сообщение с выбранным расширением (format), чтобы сохранить его.
		bot.register_next_step_handler(reply, check_unit, format)

# Шаг #4, последний шаг. Проверка введенного размера. Если всё хорошо, то генерируется и отправляется файл.
def check_size(message, format, unit):
	# Проверим, если на данном шаге получаем от пользователя команду "Назад".
	if (message.text == 'Назад'):
		# То возвращаемся на шаг #2 "Проверка расширения".
		# Дополнительн передаем сообщение с выбранным расширением (format), что оно сохранилось и не пришлось выбирать по-новой.
		check_format(format)

	# Иначе проверим, если на данном шаге получаем от пользователя команду "Вернуться в начало" или "/start".
	elif (message.text == 'Вернуться в начало' or message.text == '/start'):
		# То возвращаемся на первый начальный шаг.
		welcome(message)

	# Иначе проверим полученное собщение на некорректность. Если оно некорректное, то выведем ошибку и попросим ввести снова.
	# Проходим 2 проверки. Первая isinstance() проверит, что текст сообщения None (по-простому, что его нет).
	# Это позволит отсеять все сообщения, которые не содержат текст (например, когда отправляешь стикер или гифку).
	# Вторая проверка проверяет что сообщение НЕ является числом (not isdigit()). Она отсеивает числа с точками, знаками, буквами и прочими символами.
	# Между двумя проверками используем оператор ИЛИ (or). Получается, если наше сообщение не содержит текст ИЛИ наше сообщение не является числом, то выводим ошибку.
	elif (isinstance(message.text, type(None)) or not message.text.isdigit()):
		# Добавляем клавиатуру с кнопками "Назад" и "Вернуться в начало".
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		markup.add('Назад', 'Вернуться в начало')
		
		# Отправляем сообщение с ошибкой.
		reply = bot.send_message(message.chat.id, f"Неверный размер файла. Пожалуйста введи правильный, я принимаю только целые положительные числа, без пробелов и прочих символов 🙂", reply_markup=markup)

		# Регистрируем переход снова на шаг #4. Введенный пользователем ответ будет обрабатываться в функции check_size().
		# Дополнительно передаем туда сообщение с выбранным расширением (format) и единицой измерения (unit), чтобы сохранить их.
		bot.register_next_step_handler(reply, check_size, format, unit)

	# Иначе, если всё ОК и было введено корректное число, то переходим к проверке размера и генерации файла.
	else:
		# Переводим текст сообщения с размером файла в число для удобства дальнейших манипуляций.
		size = int(message.text)

		# Посчитаем и сохраним размер в байтах, а также сохраним единицу измерения в более кратком виде для финального сообщения.
		if (unit.text == 'MB (мегабайты)'):
			size_bytes = size * 1024 * 1024
			unit_result_text = 'MB'
		elif (unit.text == 'KB (килобайты)'):
			size_bytes = size * 1024
			unit_result_text = 'KB'
		else:
			size_bytes = size
			unit_result_text = 'B'

		# Добавим проверку на размер файла.
		# Если он меньше 1 байта или больше 45 мегабайт (47185920 байт), то выводим сообщение об ошибке.
		# Иначе переходим к генерации файла.
		if (size_bytes < 1 or size_bytes > 47185920):
			reply = bot.send_message(message.chat.id, f"Размер файла выходит за границы моих возможностей.\n<u>Мои ограничения:</u>\n<b>Минимум</b> — 1 байт\n<b>Максимум</b> — 45 MB (это 46 080 KB или 47 185 920 байт)\n\nПожалуйста, введи подходящий размер 🙂")
			# Возвращаемся снова на шаг #4 "Проверка размера" (функция check_size).
			# Не забываем передать туда сообщение с выбранным расширением файла (format) и выбранной единицой измерения (unit).
			bot.register_next_step_handler(reply, check_size, format, unit)
		else:
			# Если всё ОК и размер файла соответствует ограничениям, то перейдем к его генерации.
			# Для начала сделаем, чтобы у файла всегда было уникальное имя.
			# Для этого используя встроенный модуль time, получим текущий timestamp и конвертируем в целое число.
			# Имя файла будет содержать текущий timestamp, размер в байтах и приписку bytes (будет выглядеть так - 1681568233-43521321-bytes.png).
			timestamp = int(time.time())
			filename = f'{timestamp}-{size_bytes}-bytes{format.text}'

			# Генерируем и сохраняем файл с заданным названием, записываем туда случайные байты в нужном количестве с помощью os.urandom().
			f = open(filename,"wb")
			random_bytes = os.urandom(size_bytes)
			f.write(random_bytes)
			f.close()
			
			# Сделаем "умный" вывод финального сообщения, в зависимости от выбранных единиц измерения.
			# Если выбраны мегабайты или килобайты, выводим дополнительно в скобочках размер в байтах.
			# Если выбраны байты, то будем выводить только их.
			# Дополнительно добавим форматирование чисел с помощью .format(), чтобы большие числа красиво выглядели (пример - 2 330 200 байт).
			if (unit_result_text == 'MB' or unit_result_text == 'KB'):
				size_format = '{0:,}'.format(size).replace(',', ' ')
				size_bytes_format = '{0:,}'.format(size_bytes).replace(',', ' ')
				caption = f'🙌🏻 Ура, твой тестовый файлик с расширением <b>{format.text}</b> успешно сгенерирован!\n\nЕго размер — <b>{size_format} {unit_result_text}</b>\nВ байтах — <b>{size_bytes_format} B</b>'
			else:
				size_bytes_format = '{0:,}'.format(size_bytes).replace(',', ' ')
				caption = f'🙌🏻 Ура, твой тестовый файлик с расширением <b>{format.text}</b> успешно сгенерирован!\n\nЕго размер — <b>{size_bytes_format} {unit_result_text}</b>'

			# Открываем наш сгенерированный файл для чтения и отправляем его как документ.
			# Не забываем в подписи к нему (caption) добавить наш "умный" текст.
			# А также добавим клавиатуру с кнопкой "Вернуться в начало".
			f = open(filename,"rb")
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			markup.add('Вернуться в начало')
			reply = bot.send_document(message.chat.id, f, caption=caption, reply_markup=markup)

			# Закрываем процедуру чтения файла и удаляем его, чтобы он не занимал место на диске.
			# После возвращаемся на первый начальный шаг "Приветствие".
			f.close()
			os.unlink(filename)
			bot.register_next_step_handler(reply, welcome)

# Главная функция, запускаем поллинг бота.
def main():
	bot.infinity_polling()

# Специальная конструкция для точки входа программы (главной функции). В нашем случае это main().
if __name__ == '__main__':
	main()
