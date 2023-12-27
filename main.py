from telegram import Update

import requests
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue, Job
from datetime import datetime
from datetime import time
from datetime import datetime
from telegram.ext import MessageHandler
from telegram.ext import Filters
from datetime import datetime
from pytz import timezone




today = datetime.now().strftime("%d")
month = datetime.now().strftime("%m")
year = datetime.now().strftime("%Y")

def set_location(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text('You must provide a city and a country. Example: /city Oran Algeria')
        return

    city, country = context.args
    user_id = update.message.from_user.id

    # Store the city and country for this user
    context.user_data['city'] = city
    context.user_data['country'] = country

    # Write the user's ID, city, and country to a file
    with open('users.txt', 'a') as f:
        f.write(f'{user_id},{city},{country}\n')

    update.message.reply_text(f'Location set to {city}, {country}.')

def get_time(year, month, day, city, country):
    api_url = f'http://api.aladhan.com/v1/calendarByCity/{year}/{month}?city={city}&country={country}&method=2'
    response = requests.get(api_url)
    data = response.json()
    day = int(day) - 1
    salawat = []
    prayer_times = data['data'][day]['timings']
    salat_fajr = prayer_times['Fajr']
    salat_sunrise = prayer_times['Sunrise']
    salat_dhuhr = prayer_times['Dhuhr']
    salat_asr = prayer_times['Asr']
    salat_maghrib = prayer_times['Maghrib']
    salat_isha = prayer_times['Isha']
    salawat.append(salat_fajr)
    salawat.append(salat_sunrise)
    salawat.append(salat_dhuhr)
    salawat.append(salat_asr)
    salawat.append(salat_maghrib)
    salawat.append(salat_isha)
    return salawat



def get_prayer_times(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text('You must provide both city and country.')
        return
    
    city = context.args[0]
    country = context.args[1]

    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    

    api_url = f'http://api.aladhan.com/v1/calendarByCity/{year}/{month}?city={city}&country={country}&method=2'
    
    response = requests.get(api_url)
    data = response.json()
    
    day = day - 1
    prayer_times = data['data'][day]['timings']
    
    date_miladi = data['data'][day]['date']['readable']
    meta = data['data'][day]['meta']['timezone']
    #mosque emoji = 🕌
   
    #moon emoji = 🌙
    #sun emoji = 🌞
    #sunrise emoji = 🌅
    #sunset emoji = 🌇
    #night emoji = 🌃
    #day emoji = 🌄
    #prayer emoji = 🙏
    #mosque emoji = 🕌
    #mosque emoji = 🕌
    #kaaba emoji = 🕋
    #time emoji = ⏰
    #clock emoji = 🕰
    #clock emoji = 🕛

    
    message = f"🕌🕋 Here are the prayer times for {date_miladi} in {city.capitalize()}, {country.capitalize()}:\n\n"
    message += f"🕋 🌙 Fajr: {prayer_times['Fajr']} 🕋\n"
    message += f"🕋 🌅 Sunrise: {prayer_times['Sunrise']} 🕋\n"
    message += f"🕋 🌄 Dhuhr: {prayer_times['Dhuhr']} 🕋\n"
    message += f"🕋 🌄 Asr: {prayer_times['Asr']} 🕋\n"
    message += f"🕋 🌇 Sunset: {prayer_times['Sunset']} 🕋\n"
    message += f"🕋 🌇 Maghrib: {prayer_times['Maghrib']} 🕋\n"
    message += f"🕋 🌃 Isha: {prayer_times['Isha']} 🕋\n"
    message += f"🕋 🌙 Imsak: {prayer_times['Imsak']} 🕋\n"
    message += f"🕋 🌙 Midnight: {prayer_times['Midnight']} 🕋\n"
    message += f"🕋 🌙 Firstthird: {prayer_times['Firstthird']} 🕋\n"
    message += f"🕋 🌙 Lastthird: {prayer_times['Lastthird']} 🕋\n\n"
    message += f"🕛 Timezone: {meta}"

    update.message.reply_text(message)

user_chat_ids = set()

def load_user_chat_ids() -> None:
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                user_chat_ids.add(int(line.strip().split(',')[0]))
    except FileNotFoundError:
        pass  # It's okay if the file doesn't exist donc makalah takharbou

load_user_chat_ids()

def send_adhan_auto(context: CallbackContext, job: Job = None) -> None:
    with open('users.txt', 'r') as f:
        for line in f:
            user_id, city, country = line.strip().split(',')
            user_id = int(user_id)

            now = datetime.now()
            year = now.year
            month = now.month
            day = now.day

            api_url = f'http://api.aladhan.com/v1/calendarByCity/{year}/{month}?city={city}&country={country}&method=2'
            response = requests.get(api_url)
            data = response.json()
            day = day - 1
            prayer_times = data['data'][day]['timings']
            
            date_miladi = data['data'][day]['date']['readable']
            meta = data['data'][day]['meta']['timezone']
            #mosque emoji = 🕌
           
            #moon emoji = 🌙
            #sun emoji = 🌞
            #sunrise emoji = 🌅
            #sunset emoji = 🌇
            #night emoji = 🌃
            #day emoji = 🌄
            #prayer emoji = 🙏
            #mosque emoji = 🕌
            #mosque emoji = 🕌
            #kaaba emoji = 🕋
            #time emoji = ⏰
            #clock emoji = 🕰
            #clock emoji = 🕛

            
            message = f"🕌🕋 Here are the prayer times for {date_miladi} in {city.capitalize()}, {country.capitalize()}:\n\n"
            message += f"🕋 🌙 Fajr: {prayer_times['Fajr']} 🕋\n"
            message += f"🕋 🌅 Sunrise: {prayer_times['Sunrise']} 🕋\n"
            message += f"🕋 🌄 Dhuhr: {prayer_times['Dhuhr']} 🕋\n"
            message += f"🕋 🌄 Asr: {prayer_times['Asr']} 🕋\n"
            message += f"🕋 🌇 Sunset: {prayer_times['Sunset']} 🕋\n"
            message += f"🕋 🌇 Maghrib: {prayer_times['Maghrib']} 🕋\n"
            message += f"🕋 🌃 Isha: {prayer_times['Isha']} 🕋\n"
            message += f"🕋 🌙 Imsak: {prayer_times['Imsak']} 🕋\n"
            message += f"🕋 🌙 Midnight: {prayer_times['Midnight']} 🕋\n"
            message += f"🕋 🌙 Firstthird: {prayer_times['Firstthird']} 🕋\n"
            message += f"🕋 🌙 Lastthird: {prayer_times['Lastthird']} 🕋\n\n"
            message += f"🕛 Timezone: {meta}"

            context.bot.send_message(chat_id=user_id, text=message)
           
def register_user(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_chat_ids.add(chat_id)

    with open('user_chat_ids.txt', 'a') as f:
        f.write(f'{chat_id}\n')

def get_adkhar(context: CallbackContext, job: Job = None) -> None:
    api = job.context if job else "https://ayah.nawafdev.com/api/dekr?types=random"
    

    response = requests.get(api)
    data = response.json()
    adkar = data['content']

    for chat_id in user_chat_ids:
        context.bot.send_message(chat_id=chat_id, text=adkar)



def add_jobs_for_each_user(job_queue: JobQueue) -> None:
    # Define the API endpoints for each prayer time
    api_endpoints = {
        'salat_fajr': "https://ayah.nawafdev.com/api/dekr?types=m",
        'salat_sunrise': "https://ayah.nawafdev.com/api/dekr?types=wu",
        'salat_dhuhr': "https://ayah.nawafdev.com/api/dekr?types=pd",
        'salat_asr': "https://ayah.nawafdev.com/api/dekr?types=e",
        'salat_maghrib': "https://ayah.nawafdev.com/api/dekr?types=qd",
        'salat_isha': "https://ayah.nawafdev.com/api/dekr?types=bs"
    }

    with open('users.txt', 'r') as f:
        for line in f:
            user_id, city, country = line.strip().split(',')
            user_id = int(user_id)

            
            now = datetime.now()
            year = now.year
            month = now.month
            day = now.day

            
            salawat = get_time(year, month, day, city, country)

            
            for salat, api_endpoint in zip(salawat, api_endpoints.values()):
                salat_time, _ = salat.split(" ")
                salat_hour, salat_minute = map(int, salat_time.split(":"))

                job_queue.run_daily(
                    get_adkhar,
                    time(hour=salat_hour, minute=salat_minute),
                    context=api_endpoint,
                    name=f'{user_id}_{salat}'
                )
    job_queue.run_repeating(get_adkhar, interval=600, first=0, context="https://ayah.nawafdev.com/api/dekr?types=random")    

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello there! I'm a ISLAMPRAYER bot Develeped By: @yxxhixx on 27/12/2023 At 04:00 AM\n that sends you adkhar at specific times of the day. You can use the /prayers city country \n example USAGE : /prayers Oran Algeria \ncommand to get the prayer times for your city.\n Also /city command to set your city and country and get prayer times auto \nYou can also use the /help command to get this message again.")

def add_adhan_job(job_queue: JobQueue) -> None:
    # Schedule the send_adhan_auto function to run at 6 AM every day
    job_queue.run_daily(send_adhan_auto, time(hour=6))
updater = Updater("BOT_TOKEN")

updater.dispatcher.add_handler(CommandHandler('prayers', get_prayer_times, pass_args=True)) #ersel lel bot message /prayers city country
updater.dispatcher.add_handler(CommandHandler('help', help_command))
updater.dispatcher.add_handler(CommandHandler('city', set_location, pass_args=True))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, register_user))


add_jobs_for_each_user(updater.job_queue)
add_adhan_job(updater.job_queue)

updater.start_polling()
updater.idle()