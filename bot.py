from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import requests
import io
from PIL import Image

BOT_TOKEN = "7443794380:AAHpr7rEM5qkVxVRhOzrfPfES2UU2UU6omg"
OWNER_ID = 6217275870  # Replace with the actual owner ID
allowed_groups = [-1002211559198]

def fetch_player_info(uid: str, region: str):
    url = f'https://www.public.freefireinfo.site/api/info/{region}/{uid}?key=Ryz'
    try:
        response = requests.get(url)
        if response.status_code in [200, 500]:
            return response.json()
        else:
            print(f"Failed to fetch player information. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def format_section(title: str, content: dict) -> str:
    section = f"\n┌ {title}\n"
    for key, value in content.items():
        section += f"├─ {key}: {value}\n"
    return section[:-1]

def get_player_info(data: dict, language: str) -> str:
    if language == "ar":
        return format_section_ar(data)
    elif language == "ru":
        return format_section_ru(data)
    else:
        return format_section_en(data)

def format_section_ar(data: dict) -> str:
    return f"""
👤 **معلومات الحساب**
- **الاسم**: {data.get("Account Name", "N/A")}
- **المعرف**: {data.get("Account UID", "N/A")}
- **المستوى**: {data.get("Account Level", "N/A")} (Exp: {data.get("Account XP", "N/A")})
- **المنطقة**: {data.get("Account Region", "N/A")}
- **الإعجابات**: {data.get("Account Likes", "N/A")}
- **تقييم الشرف**: {data.get("Account Honor Score", "N/A")}
- **شعار إيفو**: {data.get("Account Evo Access Badge", "N/A")}
- **اللقب**: {data.get("Equipped Title", "N/A")}
- **السيرة الذاتية**: {data.get("Account Signature", "N/A")}

🎮 **نشاط الحساب**
- **المرور**: {data.get("Account Booyah Pass", "N/A")}
- **مستوى Booyah pass**: {data.get("Account Booyah Pass Badges", "N/A")}
- **تقييم الباتل رويال**: {data.get("BR Rank", "N/A")} ({data.get("BR Rank Points", "N/A")})
- **تقييم كلاش سكواد**: {data.get("CS Rank Points", "N/A")}
- **تاريخ إنشاء الحساب**: {data.get("Account Create Time (GMT 0530)", "N/A")}
- **آخر دخول**: {data.get("Account Last Login (GMT 0530)", "N/A")}

👕 **معلومات الزي**
- **معرف الصورة الرمزية**: {data.get("Account Avatar Image", "N/A").split("/")[-1]}
- **معرف الشعار**: {data.get("Account Banner Image", "N/A").split("/")[-1]}
- **المهارات المجهزة**: {", ".join(map(str, data.get("Equipped Items", {}).get("Equipped Skills", [])))}
- **معرف سلاح المختار**: {data.get("Equipped Items", {}).get("External Items", [{}])[0].get("Item ID", "Not Found")}

🐾 **معلومات الحيوان الأليف**
- **مجهز؟**: {"نعم" if data.get("Equipped Pet Information", {}).get("Equipped?", True) else "لا"}
- **اسم الحيوان الأليف**: {data.get("Equipped Pet Information", {}).get("Pet Name", "N/A")}
- **نوع الحيوان الأليف**: {data.get("Equipped Pet Information", {}).get("Pet Type", "N/A")}
- **خبرة الحيوان الأليف**: {data.get("Equipped Pet Information", {}).get("Pet XP", "N/A")}
- **مستوى الحيوان الأليف**: {data.get("Equipped Pet Information", {}).get("Pet Level", "N/A")}

🛡️ **معلومات النقابة**
- **اسم النقابة**: {data.get("Guild Information", {}).get("Guild Name", "N/A")}
- **معرف النقابة**: {data.get("Guild Information", {}).get("Guild ID", "N/A")}
- **مستوى النقابة**: {data.get("Guild Information", {}).get("Guild Level", "N/A")}
- **عدد الأعضاء**: {data.get("Guild Information", {}).get("Guild Current Members", "N/A")}
- **معلومات القائد**:
  - **اسم القائد**: {data.get("Guild Leader Information", {}).get("Leader Name", "N/A")}
  - **معرف القائد**: {data.get("Guild Leader Information", {}).get("Leader UID", "N/A")}
  - **مستوى القائد**: {data.get("Guild Leader Information", {}).get("Leader Level", "N/A")} (Exp: {data.get("Guild Leader Information", {}).get("Leader XP", "N/A")})
  - **تاريخ إنشاء حساب القائد**: {data.get("Guild Leader Information", {}).get("Leader Ac Created Time (GMT 0530)", "N/A")}
  - **آخر دخول للقائد**: {data.get("Guild Leader Information", {}).get("Leader Last Login Time (GMT 0530)", "N/A")}
  - **لقب القائد**: {data.get("Guild Leader Information", {}).get("Leader Title", "N/A")}
  - **شارات BP القائد**: {data.get("Guild Leader Information", {}).get("Leader BP Badges", "N/A")}
  - **تقييم الباتل رويال للقائد**: {data.get("Guild Leader Information", {}).get("Leader BR Points", "N/A")}
  - **تقييم كلاش سكواد للقائد**: {data.get("Guild Leader Information", {}).get("Leader CS Points", "N/A")}

🗺️ **معلومات كرافتلاند**
- **رمز الخريطة**: {data.get("Public Craftland Maps", {}).get("Map Codes", "Not Found")}
"""

def format_section_ru(data: dict) -> str:
    return f"""
👤 **Информация об аккаунте**
- **Имя**: {data.get("Account Name", "N/A")}
- **UID**: {data.get("Account UID", "N/A")}
- **Уровень**: {data.get("Account Level", "N/A")} (Exp: {data.get("Account XP", "N/A")})
- **Регион**: {data.get("Account Region", "N/A")}
- **Лайки**: {data.get("Account Likes", "N/A")}
- **Рейтинг доверия**: {data.get("Account Honor Score", "N/A")}
- **Значок Эво**: {data.get("Account Evo Access Badge", "N/A")}
- **Титул**: {data.get("Equipped Title", "N/A")}
- **Биография**: {data.get("Account Signature", "N/A")}

🎮 **Активность аккаунта**
- **Боевой пропуск**: {data.get("Account Booyah Pass", "N/A")}
- **Уровень боевого пропуска**: {data.get("Account Booyah Pass Badges", "N/A")}
- **Ранг BR**: {data.get("BR Rank", "N/A")} ({data.get("BR Rank Points", "N/A")})
- **Рейтинг CS**: {data.get("CS Rank Points", "N/A")}
- **Аккаунт создан**: {data.get("Account Create Time (GMT 0530)", "N/A")}
- **Последний вход**: {data.get("Account Last Login (GMT 0530)", "N/A")}

👕 **Информация о наряде**
- **ID аватара**: {data.get("Account Avatar Image", "N/A").split("/")[-1]}
- **ID баннера**: {data.get("Account Banner Image", "N/A").split("/")[-1]}
- **Оснащенные навыки**: {", ".join(map(str, data.get("Equipped Items", {}).get("Equipped Skills", [])))}
- **ID выбранного оружия**: {data.get("Equipped Items", {}).get("External Items", [{}])[0].get("Item ID", "Not Found")}

🐾 **Информация о питомце**
- **Оснащен?**: {"Да" if data.get("Equipped Pet Information", {}).get("Equipped?", True) else "Нет"}
- **Имя питомца**: {data.get("Equipped Pet Information", {}).get("Pet Name", "N/A")}
- **Тип питомца**: {data.get("Equipped Pet Information", {}).get("Pet Type", "N/A")}
- **Опыт питомца**: {data.get("Equipped Pet Information", {}).get("Pet XP", "N/A")}
- **Уровень питомца**: {data.get("Equipped Pet Information", {}).get("Pet Level", "N/A")}

🛡️ **Информация о гильдии**
- **Название гильдии**: {data.get("Guild Information", {}).get("Guild Name", "N/A")}
- **ID гильдии**: {data.get("Guild Information", {}).get("Guild ID", "N/A")}
- **Уровень гильдии**: {data.get("Guild Information", {}).get("Guild Level", "N/A")}
- **Члены гильдии**: {data.get("Guild Information", {}).get("Guild Current Members", "N/A")}
- **Информация о лидере**:
  - **Имя лидера**: {data.get("Guild Leader Information", {}).get("Leader Name", "N/A")}
  - **UID лидера**: {data.get("Guild Leader Information", {}).get("Leader UID", "N/A")}
  - **Уровень лидера**: {data.get("Guild Leader Information", {}).get("Leader Level", "N/A")} (Exp: {data.get("Guild Leader Information", {}).get("Leader XP", "N/A")})
  - **Аккаунт лидера создан**: {data.get("Guild Leader Information", {}).get("Leader Ac Created Time (GMT 0530)", "N/A")}
  - **Последний вход лидера**: {data.get("Guild Leader Information", {}).get("Leader Last Login Time (GMT 0530)", "N/A")}
  - **Титул лидера**: {data.get("Guild Leader Information", {}).get("Leader Title", "N/A")}
  - **Значки BP лидера**: {data.get("Guild Leader Information", {}).get("Leader BP Badges", "N/A")}
  - **Ранг BR лидера**: {data.get("Guild Leader Information", {}).get("Leader BR Points", "N/A")}
  - **Рейтинг CS лидера**: {data.get("Guild Leader Information", {}).get("Leader CS Points", "N/A")}

🗺️ **Информация о Крафтланде**
- **Код карты**: {data.get("Public Craftland Maps", {}).get("Map Codes", "Not Found")}
"""

def format_section_en(data: dict) -> str:
    return f"""
👤 **Account Info**
- **Name**: {data.get("Account Name", "N/A")}
- **UID**: {data.get("Account UID", "N/A")}
- **Level**: {data.get("Account Level", "N/A")} (Exp: {data.get("Account XP", "N/A")})
- **Region**: {data.get("Account Region", "N/A")}
- **Likes**: {data.get("Account Likes", "N/A")}
- **Honor Score**: {data.get("Account Honor Score", "N/A")}
- **Evo Access Badge**: {data.get("Account Evo Access Badge", "N/A")}
- **Title**: {data.get("Equipped Title", "N/A")}
- **Signature**: {data.get("Account Signature", "N/A")}

🎮 **Account Activity**
- **Booyah Pass**: {data.get("Account Booyah Pass", "N/A")}
- **Booyah Pass Level**: {data.get("Account Booyah Pass Badges", "N/A")}
- **BR Rank**: {data.get("BR Rank", "N/A")} ({data.get("BR Rank Points", "N/A")})
- **CS Rank Points**: {data.get("CS Rank Points", "N/A")}
- **Account Created**: {data.get("Account Create Time (GMT 0530)", "N/A")}
- **Last Login**: {data.get("Account Last Login (GMT 0530)", "N/A")}

👕 **Outfit Info**
- **Avatar ID**: {data.get("Account Avatar Image", "N/A").split("/")[-1]}
- **Banner ID**: {data.get("Account Banner Image", "N/A").split("/")[-1]}
- **Equipped Skills**: {", ".join(map(str, data.get("Equipped Items", {}).get("Equipped Skills", [])))}
- **Equipped Weapon Skin ID**: {data.get("Equipped Items", {}).get("External Items", [{}])[0].get("Item ID", "Not Found")}

🐾 **Pet Info**
- **Equipped?**: {"Yes" if data.get("Equipped Pet Information", {}).get("Equipped?", True) else "No"}
- **Pet Name**: {data.get("Equipped Pet Information", {}).get("Pet Name", "N/A")}
- **Pet Type**: {data.get("Equipped Pet Information", {}).get("Pet Type", "N/A")}
- **Pet XP**: {data.get("Equipped Pet Information", {}).get("Pet XP", "N/A")}
- **Pet Level**: {data.get("Equipped Pet Information", {}).get("Pet Level", "N/A")}

🛡️ **Guild Info**
- **Guild Name**: {data.get("Guild Information", {}).get("Guild Name", "N/A")}
- **Guild ID**: {data.get("Guild Information", {}).get("Guild ID", "N/A")}
- **Guild Level**: {data.get("Guild Information", {}).get("Guild Level", "N/A")}
- **Guild Members**: {data.get("Guild Information", {}).get("Guild Current Members", "N/A")}
- **Leader Info**:
  - **Leader Name**: {data.get("Guild Leader Information", {}).get("Leader Name", "N/A")}
  - **Leader UID**: {data.get("Guild Leader Information", {}).get("Leader UID", "N/A")}
  - **Leader Level**: {data.get("Guild Leader Information", {}).get("Leader Level", "N/A")} (Exp: {data.get("Guild Leader Information", {}).get("Leader XP", "N/A")})
  - **Leader Account Created**: {data.get("Guild Leader Information", {}).get("Leader Ac Created Time (GMT 0530)", "N/A")}
  - **Leader Last Login**: {data.get("Guild Leader Information", {}).get("Leader Last Login Time (GMT 0530)", "N/A")}
  - **Leader Title**: {data.get("Guild Leader Information", {}).get("Leader Title", "N/A")}
  - **Leader BP Badges**: {data.get("Guild Leader Information", {}).get("Leader BP Badges", "N/A")}
  - **Leader BR Points**: {data.get("Guild Leader Information", {}).get("Leader BR Points", "N/A")}
  - **Leader CS Points**: {data.get("Guild Leader Information", {}).get("Leader CS Points", "N/A")}

🗺️ **Craftland Info**
- **Map Code**: {data.get("Public Craftland Maps", {}).get("Map Codes", "Not Found")}
"""

def create_combined_image(avatar_url: str, banner_url: str) -> Image.Image:
    try:
        response_banner = requests.get(banner_url)
        response_avatar = requests.get(avatar_url)
        banner_image = Image.open(io.BytesIO(response_banner.content))
        avatar_image = Image.open(io.BytesIO(response_avatar.content))

        avatar_image = avatar_image.resize((57, 57))
        position = (banner_image.height - avatar_image.height, 2)
        combined_image = banner_image.copy()
        combined_image.paste(avatar_image, position, avatar_image.convert("RGBA"))

        return combined_image

    except Exception as e:
        print(f"Failed to create combined image: {e}")
        return None

def create_clothes_image(clothes_urls: list) -> Image.Image:
    try:
        max_width = 57
        max_height = 57
        num_clothes = len(clothes_urls)
        max_cols = 4
        num_rows = (num_clothes + max_cols - 1) // max_cols
        combined_clothes_image = Image.new('RGBA', (max_width * max_cols, max_height * num_rows))

        for idx, url in enumerate(clothes_urls):
            response_clothes = requests.get(url)
            clothes_image = Image.open(io.BytesIO(response_clothes.content))
            clothes_image = clothes_image.resize((max_width, max_height))
            col = idx % max_cols
            row = idx // max_cols
            x = col * max_width
            y = row * max_height
            combined_clothes_image.paste(clothes_image, (x, y))

        return combined_clothes_image

    except Exception as e:
        print(f"Failed to create combined clothes image: {e}")
        return None

def handle_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if chat_id not in allowed_groups:
        update.message.reply_text("This bot is not allowed to operate in this group.")
        return
    
    message_text = update.message.text.split()
    if len(message_text) != 2:
        return
    region, uid = message_text
    if region not in ['sg', 'ind', 'br']:
        return
    
    context.user_data['region'] = region
    context.user_data['uid'] = uid

    keyboard = [
        [
            InlineKeyboardButton("English", callback_data='en'),
            InlineKeyboardButton("العربية", callback_data='ar'),
            InlineKeyboardButton("Русский", callback_data='ru')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose a language / يرجى اختيار اللغة / Пожалуйста, выберите язык:', reply_markup=reply_markup)

def choose_language(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    language = query.data

    region = context.user_data.get('region')
    uid = context.user_data.get('uid')
    data = fetch_player_info(uid, region)

    if data:
        avatar_url = data.get("Account Avatar Image")
        banner_url = data.get("Account Banner Image")
        clothes_urls = data.get("Equipped Items", {}).get("profile", {}).get("Clothes", [])
        player_info = get_player_info(data, language)

        if avatar_url and banner_url:
            combined_image = create_combined_image(avatar_url, banner_url)
            if combined_image:
                combined_webp_io = io.BytesIO()
                combined_image.save(combined_webp_io, format='webp')
                combined_webp_io.seek(0)
                query.message.reply_sticker(combined_webp_io)

        if clothes_urls:
            combined_clothes_image = create_clothes_image(clothes_urls)
            if combined_clothes_image:
                clothes_io = io.BytesIO()
                combined_clothes_image.save(clothes_io, format='PNG')
                clothes_io.seek(0)
                query.message.reply_photo(clothes_io)

        query.message.reply_text(player_info, parse_mode=ParseMode.MARKDOWN)
        query.message.edit_reply_markup(reply_markup=None)
    else:
        query.message.reply_text("Failed to fetch player information. Please check the UID and region.")
        query.message.edit_reply_markup(reply_markup=None)

def add_group(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != OWNER_ID:
        update.message.reply_text("You are not authorized to use this command.")
        return

    if len(context.args) != 1:
        update.message.reply_text("Usage: /add <group_id>")
        return
    
    group_id = int(context.args[0])
    if group_id not in allowed_groups:
        allowed_groups.append(group_id)
        update.message.reply_text(f"Group {group_id} has been added to the allowed list.")
    else:
        update.message.reply_text(f"Group {group_id} is already in the allowed list.")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('HI ON BOT INFO PY FOX & STURNE  INFO PLYER IN FREE FIRE TAKE PLEASE SEND (regoin and uid)')
    update.message.reply_text('بوت فري فاير لجلب معلومات لاعب ')
def main() -> None:
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add_group))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(choose_language))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
