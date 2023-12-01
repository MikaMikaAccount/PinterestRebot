import telebot
import requests
import re

TOKEN = "SEU TOKEN"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    man = f'{user_name}'
    image_url = 'https://uploadhub.io/download/IaENnigtxTLDbdB/B9AqGQxVbzMn6/Picsart_23-11-29_19-26-47-649.jpg'
    description = f"""
Olá {man} Seja bem vindo(a)

Esse é um novo bot para fazer download dos vídeos do Pinterest de forma totalmente gratuita.

Para usar nosso sistema, basta enviar:
/pindl <LINK DESEJADO>
Por exemplo:
    /pindl https://pin.it/bgbXTye

© Copyright - @MikaVirus / @Ferid_Barthory
"""
    bot.send_photo(chat_id, image_url, caption=description)

@bot.message_handler(commands=['pindl'])
def handle_url(message):
    user_id = message.chat.id
    url_command = message.text.split(' ', 1)
    if len(url_command) == 2:
        URL = url_command[1]
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
        }
        preparing_message = bot.reply_to(message, "🔎 Enviando seu vídeo, aguarde...\n\n@memes_de_animes #Mika #Ferid")
        s = requests.get(url=URL, headers=headers)
        url_pattern = re.compile(r'"url":"(https://v1.pinimg.com/videos/mc/[^"]+\.mp4)"')
        matches = url_pattern.findall(s.text)
        if not matches:
            bot.reply_to(message, "❌ Não foi possível encontrar esse vídeo!!\n\n1- Verifique o post para ver se realmente existe.\n2- Verifique se é mesmo um link do Pinterest.\n\n@memes_de_animes #Mika #Ferid")
            bot.delete_message(user_id, preparing_message.message_id)
            return
        first_video_url = matches[0]
        response = requests.get(URL)
        html_text = response.text
        nome_match = re.search(r'<div class="tBJ dyH iFc sAJ O2T zDA IZT H2s CKL" title="(.*?)"', html_text)
        nome = nome_match.group(1).strip() if nome_match else "Nome não encontrado"
        msg = f"<b>🔎 VÍDEO ENCONTRADO 🔎</b>\n\n<b>» LINK:</b> {URL}\n<b>» POSTADO POR:</b> <code>{nome}</code>\n<b>» NATIVE:</b> {first_video_url}\n\n<b>© Direitos Reservados™ - #Pinterest</b>"
        bot.send_video(user_id, first_video_url, caption=msg, parse_mode='HTML', reply_to_message_id=message.message_id)
        bot.delete_message(user_id, preparing_message.message_id)

bot.infinity_polling()
