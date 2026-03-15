from telebot import TeleBot
from telebot.types import (
    InlineKeyboardMarkup as Markup,
    InlineKeyboardButton as Button
)
from telebot import apihelper
from datetime import datetime
from json import load, dump
from time import sleep
import sqlite3


bot_token = '8182404332:AAEkPoLfpCWmxXSvc9BG7ECZvgjz4j3rVWU' # YOUR BOT TOKEN
ben = TeleBot(bot_token)

MAIN_OWNER = 1235694242 # YOUR ID
owners_ids = [] # OWNERS IDs
channel = 'soarabi' # YOUR CHANNEL
owners_ids.insert(0, MAIN_OWNER)
users_db = './users'
settings_db = './settings'
admins_db = './admins'

ADMINS_MARKUP = Markup([
    [
        Button('- الاحصائيات -', callback_data = 'statics')
    ],
    [
        Button('- اضافة مستخدم -', callback_data = 'adduser'),
        Button('- حذف مستخدم -', callback_data = 'popuser')
    ],
    [
        Button('- الوضع الحالي : {} -', callback_data = 'changemode')
    ],
    [
        Button('- الادمنيه -', callback_data = 'get_admins')
    ],
    [
        Button('- اضافة ادمن -', callback_data = 'add_admin'),
        Button('- حذف ادمن -', callback_data = 'pop_admin')
    ],
    [
        Button('- اذاعه -', callback_data = 'broadcast')
    ],
    [
        Button('- الاشتراك الاجباري -', callback_data = 'force_sub')
    ],
    [
        Button('- اظهار لوحة الاعضاء -', callback_data = 'users')
    ]
])


TO_ADMINS_MARKUP = Markup([
    [
        Button('- رجوع -', callback_data = 'admins')
    ]
])


CITIES_MARKUP = Markup([
    [
        Button('- مثنى -', callback_data = 'ct_muthana'),
        Button('- نجف -', callback_data = 'ct_najaf'),
        Button('- نينوى -', callback_data = 'ct_nineveh')
    ],
    [
        Button('- ديالى -', callback_data = 'ct_diyala'),
        Button('- دهوك -', callback_data = 'ct_duhok'),
        Button('- اربيل -', callback_data = 'ct_erbil')
    ],
    [
        Button('- كربلاء -', callback_data = 'ct_karbalaa'),
        Button('- كركوك -', callback_data = 'ct_kirkuk'),
        Button('- قادسيه -', callback_data = 'ct_qadisiya')
    ],
    [
        Button('- صلاح الدين -', callback_data = 'ct_salahaldeen'),
        Button('- سلمانيه -', callback_data = 'ct_sulaymaniyah'),
        Button('- واسط -', callback_data = 'ct_wasit')
    ],
    [
        Button('- بابل -', callback_data = 'ct_babylon'),
        Button('- بغداد -', callback_data = 'ct_baghdad'),
        Button('- بلد -', callback_data = 'ct_balad')
    ],
    [
        Button('- بصره -', callback_data = 'ct_basrah'),
        Button('- ذي قار -', callback_data = 'ct_dhiqar'),
        Button('- الانبار -', callback_data = 'ct_alanbar')
    ],
    [
        Button('- ميسان -', callback_data = 'ct_mesan')
    ],
    [
        Button('- البحث عن الرقم -', callback_data='sh_phone')
    ]
])


TO_USERS_MARKUP = Markup([
    [
        Button('- رجوع -', callback_data = 'users')
    ]
])


CITIES ={
	'mesan': 'ميسان',
	'muthana': 'مثنى',
	'najaf': 'نجف',
	'nineveh': 'نينوى',
	'diyala': 'ديالى',
	'duhok': 'دهوك',
	'erbil': 'اربيل',
	'karbalaa': 'كربلاء',
	'kirkuk': 'كركوك',
	'qadisiya': 'قادسية',
	'salahaldeen': 'صلاح الدين',
	'sulaymaniyah': 'سليمانية',
	'wasit': 'واسط',
	'babylon': 'بابل',
	'baghdad': 'بغداد',
	'balad': 'بلد',
	'basrah': 'بصرة',
	'dhiqar': 'ذي قار',
	'alanbar': 'الانبار',
}

@ben.message_handler(
    commands = ['start'],
    chat_types = ['private'],
)
def owners_start(message):
    user_id = message.from_user.id
    if user_id in owners_ids + admins:
        mode = 'مدفوع' if settings['mode'] == 'private' else 'مجاني'
        markup = ADMINS_MARKUP
        markup.keyboard[2][0].text = '- الوضع الحالي : {} -'.format(mode)
        ben.reply_to(
            message,
            '- مرحبا بك عزيزي المالك يمكنك التحكم بالبوت من خلال الازرار التاليه :',
            reply_markup = markup
        )
    else:
        subscribed = subscription(user_id)
        if subscribed is None: return ben.reply_to(message, '- عليك الاشتراك بقناة البوت أولا!', reply_markup = Markup([[Button('- اشتراك -', url = 't.me/%s' % settings['channel'])]]))
        if users.get(str(user_id)) is None:
            users[str(user_id)] = False
            write(users_db, users)
            ben.send_message(
                MAIN_OWNER,
                '- دخل شخص جديد الى البوت 🔥\n\n- ايديه : %s\n- معرفه: %s\n\n- عدد المستخدمين الكلي: %s' % (
                    user_id, '@' + message.from_user.username if message.from_user.username else 'لا يوجد',
                    len(users)
                )
            )
        if users.get(str(user_id)) or settings['mode'] != 'private':  
            ben.reply_to(
                message,
                '- مرحبا بك عزيزي في بوت بيانات العراق يمكنك البحث من خلال الازرار التاليه :',
                reply_markup = CITIES_MARKUP
            )
        else:
            if users.get(str(user_id)) is None:
                users[str(user_id)] = False
                write(users_db, users)
            ben.reply_to(
                message,
                'عذرا عزيزي لا يمكنك استخدام البوت قم بمراسلة المالك لتسطيع استخدام البوت!',
                reply_markup = Markup([[Button('- المالك -', url = f'tg://openmessage?user_id={MAIN_OWNER}')]])
            )    


@ben.callback_query_handler(
    func = lambda call: call.data in ['adduser', 'popuser', 'add_admin', 'pop_admin']
)
def add_pop_user(callback):
    user_id = callback.from_user.id
    if user_id not in owners_ids:
        if user_id not in admins: return ben.edit_message_text(
            message_id = callback.message.id,
            chat_id = user_id,
            text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
        )
        else:
            if callback.data in ['add_admin', 'pop_admin']:
                return ben.answer_callback_query(
                    callback.id, '- لا يمكنك استخدام هذه الميزهّ!' , show_alert = True
                )
    settings['get_id'][str(user_id)] = callback.data
    write(settings_db, settings)
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = '- حسنا عزيزي قم بارسال ايدي المستخدم!',
        reply_markup = TO_ADMINS_MARKUP
    )


@ben.callback_query_handler(
    func = lambda call: call.data == 'changemode'
)
def change_mode(callback):
    user_id = callback.from_user.id
    if user_id not in owners_ids + admins:return ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
    )
    settings['mode'] = 'public' if settings['mode'] == 'private' else 'private'
    write(settings_db, settings)
    mode = 'مدفوع' if settings['mode'] == 'private' else 'مجاني'
    ben.answer_callback_query(callback.id, f'- تم تغيير الوضع الى {mode}')
    markup = ADMINS_MARKUP
    markup.keyboard[2][0].text = '- الوضع الحالي : {} -'.format(mode)
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = '- مرحبا بك عزيزي المالك يمكنك التحكم بالبوت من خلال الازرار التاليه :',
        reply_markup = markup
    )


@ben.callback_query_handler(
    func = lambda call: call.data == 'admins'
)
def to_admins(callback):
    user_id = callback.from_user.id
    for setting in settings:
        if setting in ['mode', 'channel']: continue
        elif setting in ['get_num', 'get_broadcast', 'get_channel']:
            if user_id in settings[setting]: settings[setting].remove(user_id)
        elif settings[setting].get(str(user_id)): del settings[setting][str(user_id)]
    if user_id not in owners_ids + admins:return ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
    )
    mode = 'مدفوع' if settings['mode'] == 'private' else 'مجاني'
    markup = ADMINS_MARKUP
    markup.keyboard[2][0].text = '- الوضع الحالي : {} -'.format(mode)
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = '- مرحبا بك عزيزي المالك يمكنك التحكم بالبوت من خلال الازرار التاليه :',
        reply_markup = markup
    )


@ben.message_handler(
    content_types = ['text'],
    chat_types = ['private'],
    func = lambda msg: settings['get_id'].get(str(msg.from_user.id))
)
def get_id(message):
    data = settings['get_id'][str(message.from_user.id)]
    if data == 'adduser':
        if users.get(message.text):
            ben.reply_to(message, '- العضو موجود بالبوت من قبل!', reply_markup = TO_ADMINS_MARKUP)
        else:
            users[message.text] = True
            write(users_db, users)
            ben.reply_to(message, '- تم اضافة العضو للبوت بنجاح!', reply_markup = TO_ADMINS_MARKUP)
    elif data == 'popuser':
        if users.get(message.text) is None:
            ben.reply_to(message, '- العضو غير موجود بالبوت ليتم حذفه!', reply_markup = TO_ADMINS_MARKUP)
        else:
            users[message.text] = False
            write(users_db, users)
            ben.reply_to(message, '- تم حذف العضو من البوت!', reply_markup = TO_ADMINS_MARKUP)
    elif data == 'add_admin':
        if not message.text.isnumeric():
            ben.reply_to(message, '- الايدي غير صالح!', reply_markup = TO_ADMINS_MARKUP)
        elif int(message.text) in admins:
            ben.reply_to(message, '- الادمن موجود بالبوت من قبل!', reply_markup = TO_ADMINS_MARKUP)
        else:
            try: ben.get_chat(int(message.text))
            except:
                ben.reply_to(message ,'- لم يتم ايجاد هذا المستخدم!', reply_markup = TO_ADMINS_MARKUP)
                del settings['get_id'][str(message.from_user.id)]
                write(settings_db, settings)
                return
            admins.append(int(message.text))
            write(admins_db, admins)
            ben.reply_to(message, '- تم اضافة المستخدم لقائمة الادمنيه!', reply_markup = TO_ADMINS_MARKUP)
    elif data == 'pop_admin':
        if not message.text.isnumeric():
            ben.reply_to(message, '- الايدي غير صالح!', reply_markup = TO_ADMINS_MARKUP)
        elif int(message.text) not in admins:
            ben.reply_to(message, '- المستخدم ليس من ادمنية البوت!', reply_markup = TO_ADMINS_MARKUP)
        else:
            try: ben.get_chat(int(message.text))
            except:
                ben.reply_to(message ,'- لم يتم ايجاد هذا المستخدم!', reply_markup = TO_ADMINS_MARKUP)
                del settings['get_id'][str(message.from_user.id)]
                write(settings_db, settings)
                return
            admins.remove(int(message.text))
            write(admins_db, admins)
            ben.reply_to(message, '- تم حذف المستخدم من قائمة الادمنيه', reply_markup = TO_ADMINS_MARKUP)
    del settings['get_id'][str(message.from_user.id)]
    write(settings_db, settings)


@ben.callback_query_handler(
    func = lambda callback: callback.data == 'statics' and callback.from_user.id in (owners_ids + admins)
)
def statics(callback):
    ben.answer_callback_query(callback.id ,'- جاري الحصول على البيانات... -', show_alert = True)
    caption = '- حسنا عزيزي اليك احصائيات البوت!\n\n'
    vips = 0
    norm = 0
    for user in users:
        if users[user]: vips += 1
        else: norm += 1
    caption += '- عدد المستخدمين الكلي: %s\n' % len(users)
    caption += '- عدد المستخدمين المشتركين بالبوت: %s\n' % vips
    caption += '- عدد المستخدمين غير المشتركين بالبوت: %s\n' % norm
    ben.edit_message_text(
        chat_id = callback.from_user.id,
        message_id = callback.message.id,
        text = caption,
        reply_markup = TO_ADMINS_MARKUP
    )


@ben.callback_query_handler(
    func = lambda callback: callback.data == 'get_admins' and callback.from_user.id in (owners_ids + admins)
)
def get_admins(callback):
    ben.answer_callback_query(callback.id ,'- جاري الحصول على البيانات... -', show_alert = True)
    caption = '- حسنا عزيزي اليك ادمنية البوت!\n\n'
    for admin in admins:
        user = ben.get_chat(admin)
        caption += '- [%s](https://t.me/%s)\n' % (user.first_name, user.username)
    ben.edit_message_text(
        chat_id = callback.from_user.id,
        message_id = callback.message.id,
        text = caption,
        reply_markup = TO_ADMINS_MARKUP,
        disable_web_page_preview = True,
        parse_mode = 'MARKDOWN'
    )


@ben.callback_query_handler(
    func = lambda callback: callback.data == 'broadcast' and callback.from_user.id in (owners_ids + admins)
)
def broadcast(callback):
    user_id = callback.from_user.id
    if user_id not in owners_ids:
        if user_id not in admins: return ben.edit_message_text(
            message_id = callback.message.id,
            chat_id = user_id,
            text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
        )
        else:
            return ben.answer_callback_query(
                callback.id, '- لا يمكنك استخدام هذه الميزهّ!' , show_alert = True
            )
    settings['get_broadcast'].append(user_id)
    write(settings_db, settings)
    ben.edit_message_text(
        chat_id = user_id,
        message_id = callback. message.id,
        text = '- حسنا عزيزي قم بارسال رسالة الاذاعه الان.',
        reply_markup = TO_ADMINS_MARKUP
    )


@ben.message_handler(
    chat_types = ['private'],
    content_types = ['photo', 'text','audio', 'voice', 'video', 'sticker', 'document'],
    func = lambda message: message.from_user.id in settings['get_broadcast']
)
def get_broadcast(message):
    user_id = message.from_user.id
    settings['get_broadcast'].remove(user_id)
    write(settings_db, settings)
    ben.reply_to(
        message,
        '- جاري الاذاعه!',
        reply_markup = TO_ADMINS_MARKUP
    )
    banned_me = 0
    for user in users:
        try: ben.copy_message(
            chat_id = int(user),
            from_chat_id = user_id,
            message_id = message.id
        )
        except: banned_me += 1
    ben.reply_to(
        message,
        '- تمت الاذاعه بنجاح الى : %s\n\n- الاشخاص الذين قاموا بحظر البوت: %s' % (len(users) - banned_me, banned_me)
    )

@ben.callback_query_handler(
    func = lambda callback: callback.data == 'force_sub' and callback.from_user.id in owners_ids + admins
)
def force_sub(callback):
    user_id = callback.from_user.id
    if user_id not in owners_ids + admins: return ben.edit_message_text(
            message_id = callback.message.id,
            chat_id = user_id,
            text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
        )
    ben.edit_message_text(
        chat_id = user_id,
        message_id = callback.message.id,
        text = '- قناة الاشتراك الحاليه : @%s\n- يمكنك تغيير قناة الاشتراك من خلال الزر التالي: ' % (settings['channel']),
        reply_markup = Markup([
            [Button('- تغيير قناة الاشتراك -', callback_data = 'change_force')],
            [Button('- رجوع -', callback_data = 'admins')]
        ])
    )


@ben.callback_query_handler(
    func = lambda callback: callback.data == 'change_force' and callback.from_user.id in owners_ids + admins
)
def change_force(callback):
    user_id = callback.from_user.id
    if user_id not in owners_ids:
        if user_id not in admins: return ben.edit_message_text(
            message_id = callback.message.id,
            chat_id = user_id,
            text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات'
        )
        else:
            return ben.answer_callback_query(
                callback.id, '- لا يمكنك استخدام هذه الميزهّ!' , show_alert = True
            )
    settings['get_channel'].append(user_id)
    write(settings_db, settings)
    ben.edit_message_text(
        chat_id = user_id,
        message_id = callback.message.id,
        text = '- حسنا عزيزي قم بارسال قناة الاشتراك الجديده',
        reply_markup = TO_ADMINS_MARKUP
    )


@ben.message_handler(
    content_types =  ['text'],
    chat_types = ['private'],
    func = lambda message: message.from_user.id in settings['get_channel']
)
def get_channel(message):
    user_id = message.from_user.id
    settings['get_channel'].remove(user_id)
    write(settings_db, settings)
    nchannel = message.text.replace('http', '').replace('https', '').replace('t.me', '').replace('/', '').replace('@', '')
    try: ben.get_chat('@' + nchannel)
    except: return ben.reply_to(
        message,
        '- عذرا عزيزي لم استطع الوصول لهذه القناه',
        reply_markup = TO_ADMINS_MARKUP
    )
    settings['channel'] = nchannel
    write(settings_db, settings)
    ben.reply_to(
        message,
        '- تم تحديث قناة الاشتراك الاجباري!\n\n- تأكد من رفعي مشرف بالقناه الجديده!',
        reply_markup = TO_ADMINS_MARKUP
    )
    ben.send_message(
        MAIN_OWNER,
        '- تم تغيير قناة الاشتراك الاجباري بواسطة : [%s](t.me/%s)' % (message.from_user.first_name, message.from_user.username)
    )
    

@ben.callback_query_handler(
    func = lambda call: ((users.get(str(call.from_user.id)) is None and call.from_user.id not in owners_ids + admins and settings['mode'] == 'private')
                          or (users.get(str(call.from_user.id)) == False and call.from_user.id not in owners_ids + admins and settings['mode'] == 'private'))
)
def not_active(callback):
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = callback.from_user.id,
        text = '- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات!'
    )


@ben.callback_query_handler(
    func = lambda call: call.data.startswith('ct_')
)
def start_search(callback):
    user_id = callback.from_user.id
    settings['get_name'][str(user_id)] = callback.data.split('_')[1]
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = callback.from_user.id,
        text = '- حسنا عزيزي قم بارسال اسم الشخص ثلاثي أو ثنائي.',
        reply_markup = TO_USERS_MARKUP
    )


@ben.message_handler(
    content_types = ['text'],
    chat_types = ['private'],
    func = lambda msg: settings['get_name'].get(str(msg.from_user.id))
)
def get_name(message):
    full_name = message.text.split()
    user_id = message.from_user.id
    city = settings['get_name'][str(user_id)]
    del settings['get_name'][str(user_id)]
    write(settings_db, settings)
    if len(full_name) not in [2, 3]: return ben.reply_to(
        message,
        '- عذرا عزيزي الاسم المعطى غير صحيح!',
        reply_markup = TO_USERS_MARKUP
    )
    wait = ben.reply_to(message, '- جاري البحث...')
    if city == "baghdad":
        town = "rc_name"
        street = "f_street"
        work = "p_job"
    else:
        town = "ss_br_nm"
        street = "ss_lg_no"
        work = "p_work" 
    connection = sqlite3.connect(f'{city}.db')
    connection.text_factory = str
    cursor = connection.cursor()
    fname = full_name[0]
    sname = full_name[1]
    if len(full_name) == 3: lname = full_name[2]
    else: lname = None
    if lname: query = f"SELECT fam_no, p_first, p_father, p_grand, p_birth, {town}, rc_no, seq_no, {street}, {work} FROM person WHERE p_first LIKE '{fname}%' AND p_father LIKE '{sname}%' AND p_grand LIKE '{lname}%'"
    else: query = f"SELECT fam_no, p_first, p_father, p_grand, p_birth, {town}, rc_no, seq_no, {street}, {work} FROM person WHERE p_first LIKE '{fname}%' AND p_father LIKE '{sname}%'"
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows is None or rows == False: return ben.edit_message_text(
        message_id = wait.id,
        chat_id = user_id,
        text = '- عذرا عزيزي لم يتم ايجاد اي نتائج مطابقه!',
        reply_markup = TO_USERS_MARKUP
	)
    for row in rows:
        row = list(row)
        try: age = str(int(datetime.now().year) - int(str(row[4])[:4]))
        except: age = None
        text_template = '- رقم العائله : %s\n- الاسم الاول : %s\n- الاسم الثاني : %s\n- الاسم الثالث : %s\n- تاريخ الميلاد : %s\n- العمر : %s\n- الوضيفه : %s\n- المحافظه : %s\n- القضاء : %s\n- المحله : %s\n- الزقاق : %s\n- الدار : %s' % (
	        str(row[0]), str(row[1]).replace('\x84', ''), str(row[2]).replace('\x84', ''), row[3].replace('\x84', ''), 
            str(row[4])[:4], age,
	        str(row[9]), CITIES[city], str(row[5]), str(row[6]), str(row[8]), str(row[7])
	    )
        ben.send_message(
	        user_id,
	        text_template,
	        reply_markup = Markup([
	            [Button('- البحث عن العائله -', callback_data = f'family {str(row[0])} {city}')]
	        ])
	    )
    connection.close()
    ben.delete_message(
	    user_id,
	    wait.id
    )
    ben.send_message(
	    user_id,
	    '- انتهى البحث عن :  {}'.format(message.text),
	    reply_markup = TO_USERS_MARKUP
    )


@ben.callback_query_handler(
    func = lambda call: call.data.startswith('family')
)
def get_family(callback):
    user_id = callback.from_user.id
    data = callback.data.split()[1:]
    family = data[0]
    city = data[1]
    wait = ben.send_message(
        user_id,
        '- جاري البحث عن العائله...'
    )
    town = 'rc_name' if city == 'baghdad' else 'ss_br_nm'
    connection = sqlite3.connect(f'{city}.db')
    connection.text_factory = str
    cursor = connection.cursor()
    query = f"SELECT fam_no, p_first, p_father, p_grand, p_birth, {str(town)} FROM person WHERE fam_no LIKE '{family}%'"
    cursor.execute(query)
    rows = cursor.fetchall()
    members = ''
    if rows is None or not len(rows) or rows == False: return ben.edit_message_text(
        message_id = wait.id,
        chat_id = user_id,
        text = '- عذرا عزيزي لم يتم ايجاد اي نتائج مطابقه!',
        reply_markup = TO_USERS_MARKUP
    )
    for row in rows:
        row = list(row)
        try: age = str(int(datetime.now().year) - int(str(row[4])[:4]))
        except: age = None
        text_template = '- رقم العائله : %s\n- الاسم الاول : %s\n- الاسم الثاني : %s\n- الاسم الثالث : %s\n- تاريخ الميلاد : %s\n- العمر : %s\n- المحافظه : %s\n- القضاء : %s'  % (
            str(row[0]), str(row[1]).replace('\x84', ''), str(row[2]).replace('\x84', ''), row[3].replace('\x84', ''), 
            str(row[4])[:4], age, CITIES[city], str(row[5])
        )
        members += text_template
        members += '\n\n'
        ben.edit_message_text(
            message_id = wait.id,
            chat_id = user_id,
            text = members
        )
    connection.close()
    members += '- تم الانتهاء.'
    ben.edit_message_text(
        message_id = wait.id,
        chat_id = user_id,
        text = members
    )
    

@ben.callback_query_handler(
    func = lambda call: call.data == 'sh_phone'
)
def sh_phone(callback):
    user_id = callback.from_user.id
    settings['get_num'].append(user_id)
    write(settings_db, settings)
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = callback.from_user.id,
        text = '- حسنا عزيزي قم بإرسال الاسم الثلاثي للشخص.',
        reply_markup = TO_USERS_MARKUP
    )
    

@ben.message_handler(
    content_types = ['text'],
    chat_types = ['private'],
    func = lambda msg: msg.from_user.id in settings['get_num']
)
def get_num(message):
    user_id = message.from_user.id
    settings['get_num'].remove(user_id)
    write(settings_db, settings)
    full_name = message.text
    if len(full_name.split()) not in [2, 3]: return ben.reply_to(
        message,
        '- عذرا عزيزي الاسم المعطى غير صحيح!',
        reply_markup = TO_USERS_MARKUP
    )
    wait = ben.reply_to(message, '- جاري البحث')
    connection = sqlite3.connect('Asiacell.db')
    connection.text_factory = str
    cursor = connection.cursor()
    query = f'SELECT * FROM MAIN_DATA WHERE NAME LIKE "{full_name}%"'
    cursor.execute(query)
    rows = cursor.fetchall()
    if not len(rows) or rows is None or rows == False: return ben.edit_message_text(
        message_id = wait.id,
        chat_id = user_id,
        text = '- عذرا عزيزي لم يتم ايجاد اي نتائج مطابقه!',
        reply_markup = TO_USERS_MARKUP
    )
    for row in rows:
        row = list(row)
        try:ben.reply_to(
            message,
            '- الاسم : %s\n- المحافظه : %s\n- رقم البطاقه : %s\n- تاريخ الميلاد: %s\n- الرقم : %s' % (
                row[0], row[1], row[-1] if row[-1] != '' else 'غير معروف', row[3][:8], '0' + row[2].replace('.', '')[:10]
            )
        )
        except apihelper.ApiTelegramException as e:
            if 'A request to the Telegram API was unsuccessful. Error code: 429. Description: Too Many Requests: retry after' in str(e):
                time = int(str(e).rsplit(maxsplit = 1)[1])
                sleep(time)
                ben.reply_to(
                    message,
                    '- الاسم : %s\n- المحافظه : %s\n- رقم البطاقه : %s\n- تاريخ الميلاد: %s\n- الرقم : %s' % (
                        row[0], row[1], row[-1] if row[-1] != '' else 'غير معروف', row[3][:8], 
                        '0' + row[2].replace('.', '')[:10]
                    )
                )
                continue
            else:
                ben.reply_to(message, '- حدث خطأ ما..!')
                continue
    ben.delete_message(user_id, wait.id)
    ben.reply_to(
        message,
        '- انتهى البحث.',
        reply_markup = TO_USERS_MARKUP
    )
    
    

@ben.callback_query_handler(
    func = lambda call: call.data == 'users'
)
def to_users(callback):
    user_id = callback.from_user.id
    for setting in settings:
        if setting in ['mode', 'channel']: continue
        elif setting in ['get_num', 'get_broadcast', 'get_channel']:
            if user_id in settings[setting]: settings[setting].remove(user_id)
        elif settings[setting].get(str(user_id)): del settings[setting][str(user_id)]
    ben.edit_message_text(
        message_id = callback.message.id,
        chat_id = user_id,
        text = '- مرحبا بك عزيزي في بوت بيانات العراق يمكنك البحث من خلال الازرار التاليه :',
        reply_markup = CITIES_MARKUP
    )


read = lambda path: load(open(path))
write = lambda path, data: dump(data ,open(path, 'w'), indent = 4, ensure_ascii = False)


def subscription(user_id):
    try:member = ben.get_chat_member('@' + settings['channel'], user_id)
    except:return ben.send_message(MAIN_OWNER, '- هناك مشكله بالاشتراك الاجباري')
    if member.status in ["creator", "member", "administrator"]:
        return True
    return


def main():
    global users, settings, admins
    import os
    if not os.path.exists(users_db):
        write(users_db, {})
    if not os.path.exists(settings_db):
        write(settings_db, {
            'mode' : 'private',
            'get_id': {},
            'get_name': {},
            'get_broadcast': [],
            'channel': channel,
            'get_channel': [],
            'get_num': []
        })
    if not os.path.exists(admins_db):
        write(admins_db, [])
    settings = read(settings_db)
    users = read(users_db)
    admins = read(admins_db)
    print('[+] Started')
    ben.infinity_polling(skip_pending = True)


if __name__ == '__main__': main()
# 𝗪𝗥𝗜𝗧𝗧𝗘𝗡 𝗕𝗬 : @aSBSsSa
# 𝗦𝗢𝗨𝗥𝗖𝗘 : @mmaahg