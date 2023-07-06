from telebot.async_telebot import AsyncTeleBot
import requests
import librosa
import soundfile as sf

API_TOKEN = '6286035570:AAGUyK_aRQaZdERTc3ZDYB5fqY-mcH6UWQM'
bot = AsyncTeleBot(API_TOKEN)
async def convert_to_wav(mp3_file, chat_id):
    # Загрузка аудиофайла MP3
    audio, sample_rate = sf.read(mp3_file)

    # Получение пути и имени файла без расширения
    wav_file = mp3_file.rsplit('.', 1)[0] + '.wav'

    # Сохранение аудиофайла в формате WAV
    sf.write(wav_file, audio, sample_rate)

    y, sr = librosa.load(wav_file)

    # 3. Run the default beat tracker
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    txt = 'Расчетный темп: {:.2f} ударов в минуту'.format(tempo)
    await bot.send_message(chat_id, txt)



@bot.message_handler(content_types=['text'])
async def handle_text(message):
    chat_id = message.chat.id
    url = message.text

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Extract the filename from the URL
        filename = url.split('/')[-1]

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


        await convert_to_wav(filename, chat_id)
        await bot.send_audio(chat_id, message.text)

    except requests.exceptions.HTTPError as err:
        await bot.send_message(chat_id, f"HTTP Error occurred: {err}")
    except:
        await bot.send_message(chat_id, f"Попробуйте снова!")


import asyncio

asyncio.run(bot.polling())
