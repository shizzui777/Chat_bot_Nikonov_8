import os
from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

# Загружаем русскую модель spaCy
nlp = spacy.load("ru_core_news_sm")

#Клавиатуры
def main_menu_keyboard():
    return [
        [{"text": "Проблемы со входом"}],
        [{"text": "Ошибка в работе"}],
        [{"text": "Частые вопросы"}],
        [{"text": "Связаться с поддержкой"}]
    ]

def faq_keyboard():
    return [
        [{"text": "Вход в систему"}],
        [{"text": "Ошибка"}],
        [{"text": "Инструкция"}],
        [{"text": "Другое"}],
        [{"text": "Назад"}]
    ]

def login_problem_keyboard():
    return [
        [{"text": "Забыл пароль"}],
        [{"text": "Ошибка входа"}],
        [{"text": "Аккаунт заблокирован"}],
        [{"text": "Назад"}]
    ]

def service_error_keyboard():
    return [
        [{"text": "Не открывается"}],
        [{"text": "Зависает"}],
        [{"text": "Ошибка при действии"}],
        [{"text": "Назад"}]
    ]

def support_keyboard():
    return [
        [{"text": "Создать заявку"}],
        [{"text": "Позвонить в поддержку"}],
        [{"text": "Написать в чат"}],
        [{"text": "Назад"}]
    ]

def back_keyboard():
    return [[{"text": "Назад"}]]

#Продвинутый Fallback
def analyze_fallback(message):
    doc = nlp(message.lower())
    tokens = [token.lemma_ for token in doc]  # Лемматизация для улучшения поиска

    # Словари для семантической классификации
    login_words = {"вход", "логин", "пароль", "не могу войти", "login", "signin"}
    error_words = {"ошибка", "не работает", "зависает", "не открывается", "error", "fail"}
    faq_words = {"инструкция", "как", "помощь", "что делать", "faq"}
    support_words = {"поддержка", "связаться", "оператор", "заявка", "contact"}

    # Проверка токенов по словарям
    if any(token in login_words for token in tokens):
        return "login_problem", "Похоже, у вас проблема со входом. Выберите из меню:", login_problem_keyboard()
    elif any(token in error_words for token in tokens):
        return "service_error", "Похоже, возникла ошибка в работе. Выберите из меню:", service_error_keyboard()
    elif any(token in faq_words for token in tokens):
        return "faq", "Выберите категорию:", faq_keyboard()
    elif any(token in support_words for token in tokens):
        return "support", "Выберите способ связи:", support_keyboard()
    else:
        return "unknown", "Извините, я пока не знаю, как ответить на это. Попробуйте переформулировать вопрос.", None

#Основной маршрут webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req['queryResult']['intent']['displayName']
    user_message = req['queryResult'].get('queryText', '')

    payload = None
    response_text = "Извините, я пока не знаю, как ответить на это."

    #Главное меню
    if intent in ["Greeting", "Go_Back"]:
        payload = {
            "telegram": {
                "text": "Главное меню:",
                "reply_markup": {
                    "keyboard": main_menu_keyboard(),
                    "one_time_keyboard": True,
                    "resize_keyboard": True
                }
            }
        }
        response_text = "Главное меню:"

    #Частые вопросы
    elif intent == "Частые_вопросы":
        payload = {
            "telegram": {
                "text": "Выберите категорию:",
                "reply_markup": {
                    "keyboard": faq_keyboard(),
                    "one_time_keyboard": True,
                    "resize_keyboard": True
                }
            }
        }
        response_text = "Выберите категорию:"

    #Проблемы со входом
    elif intent == "Проблемы_со_входом":
        payload = {
            "telegram": {
                "text": "Выберите проблему со входом:",
                "reply_markup": {
                    "keyboard": login_problem_keyboard(),
                    "one_time_keyboard": True,
                    "resize_keyboard": True
                }
            }
        }
        response_text = "Выберите проблему со входом:"

    #Ошибка в работе
    elif intent == "Ошибка_в_работе":
        payload = {
            "telegram": {
                "text": "Выберите тип ошибки:",
                "reply_markup": {
                    "keyboard": service_error_keyboard(),
                    "one_time_keyboard": True,
                    "resize_keyboard": True
                }
            }
        }
        response_text = "Выберите тип ошибки:"

    #Связаться с поддержкой
    elif intent == "Связаться_с_поддержкой":
        payload = {
            "telegram": {
                "text": "Выберите способ связи:",
                "reply_markup": {
                    "keyboard": support_keyboard(),
                    "one_time_keyboard": True,
                    "resize_keyboard": True
                }
            }
        }
        response_text = "Выберите способ связи:"

    #Подменю
    elif intent == "Забыл_пароль":
        payload = {
            "telegram": {
                "text": "Чтобы восстановить пароль, воспользуйтесь ссылкой 'Забыли пароль?' или обратитесь в поддержку.",
                "reply_markup": {
                    "keyboard": back_keyboard(),
                    "one_time_keyboard": True,
                    "resize_keyboard": True
                }
            }
        }
        response_text = "Инструкция по восстановлению пароля:"

    elif intent == "Ошибка_входа":
        payload = {
            "telegram": {
                "text": "Ошибка входа может быть вызвана некорректным логином или паролем. Проверьте данные и попробуйте снова.",
                "reply_markup": {
                    "keyboard": back_keyboard(),
                    "one_time_keyboard": True,
                    "resize_keyboard": True
                }
            }
        }
        response_text = "Ошибка входа:"

    elif intent == "Аккаунт_заблокирован":
        payload = {
            "telegram": {
                "text": "Ваш аккаунт заблокирован. Свяжитесь с поддержкой для разблокировки.",
                "reply_markup": {
                    "keyboard": back_keyboard(),
                    "one_time_keyboard": True,
                    "resize_keyboard": True
                }
            }
        }
        response_text = "Аккаунт заблокирован:"

    #Продвинутый Fallback
    else:
        intent_name, response_text, kb = analyze_fallback(user_message)
        if kb:
            payload = {
                "telegram": {
                    "text": response_text,
                    "reply_markup": {
                        "keyboard": kb,
                        "one_time_keyboard": True,
                        "resize_keyboard": True
                    }
                }
            }

    #Отправка ответа
    if payload:
        return jsonify({
            "fulfillmentText": response_text,
            "payload": payload
        })
    else:
        return jsonify({
            "fulfillmentText": response_text
        })

#Запуск сервера
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




