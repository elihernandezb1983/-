"""Конфигурация текстов, панелей и путей."""

from pathlib import Path

# Корень проекта
BASE_DIR = Path(__file__).resolve().parent
FOTO_PANEL_DIR = BASE_DIR / "foto_panel"
FOTO_VZP_DIR = BASE_DIR / "foro_vzp"

# Discord
BOT_TOKEN = ""  # или через .env: DISCORD_TOKEN

# ID сервера для быстрой синхронизации /панель (рекомендуется при разработке).
# В .env: GUILD_ID=123456789012345678
SYNC_GUILD_ID: int | None = None

# Глобальная синхронизация при каждом запуске — лимит Discord ~1 раз в час.
SYNC_GLOBAL_ON_START = False

# Роли/права для /панель и /тикет-настройка (нужно одно из: админ сервера или эта роль)
PANEL_ALLOWED_ROLE_IDS: list[int] = []

# --- Telegram (только войны → Discord) ---
TELEGRAM_API_ID: int | None = None
TELEGRAM_API_HASH: str = ""
TELEGRAM_PHONE: str = ""
TELEGRAM_CHATS: list[str] = []

# Канал Discord для embed статистики войн (или /война-канал)
WAR_CHANNEL_ID: int | None = None
# Канал для запроса скрина и приёма фото (или /война-канал-скрины)
WAR_REPORT_CHANNEL_ID: int | None = None
# Секунд ждать скрин после исхода (30 мин)
WAR_SCREENSHOT_TIMEOUT_SEC = 1800
# Роли для тега при запросе скрина (через запятую в .env)
WAR_PING_ROLE_IDS: list[int] = []
# Канал панели кулдаунов атаки/защиты (или /война-канал-кд)
WAR_CD_CHANNEL_ID: int | None = None
# Минуты кулдауна после забивки (атака 240 = 4 ч, защита 180 = 3 ч)
WAR_ATTACK_CD_MINUTES = 240
WAR_DEFENSE_CD_MINUTES = 180

# Карты VZP: название → файлы в foro_vzp/ (1–2 фото на карту)
VZP_MAPS: dict[str, list[str]] = {
    "Байкерка": ["1.png"],
    "Большой миррор": ["2.png"],
    "Веспуччи": ["3.png"],
    "Ветряки": ["4.png"],
    "Киностудия": ["5.png"],
    "Лесопилка": ["6.png"],
    "Маленький миррор": ["7.png"],
    "Муравейник": ["8.png"],
    "Мусорка": ["9.png"],
    "Мясо": ["10.png"],
    "Нефть": ["11.png", "11_2.png"],
    "Палетка": ["12.png"],
    "Порт Биз": ["13.png"],
    "Сендик": ["14.png"],
    "Стройка": ["15.png"],
    "Татушка": ["16.png"],
}

# --- Панели (ключ = значение в /панель) ---
PANELS: dict[str, dict] = {
    "semya": {
        "label": "Заявка в семью",
        "description": "Панель набора в семью с формой заявки",
        "image": "semya.png",
        "accent_color": 0xB9BBBE,
        "title": "### Оформление заявки в семью.",
        "body": (
            "Уведомление о приглашении на обзвон отправляется в личные сообщения.\n"
            "Заявки открыты только на **20 сервер Murrieta**\n\n"
            "> В среднем заявки обрабатываются в течение 1-2 дней\n\n"
            "Следите за статусом набора.\n"
            "**Если возможности заполнить заявку нет – набор закрыт.**\n"
            "**Каждое открытие набора сопровождается тегами в этом канале.**\n\n"
            "> В случае отказа можете подать заявку повторно через 7 дней"
        ),
        "select_section_label": "Подать заявку:",
        "select_placeholder": "Подать заявку в семью",
        "select_option_label": "Подать заявку",
        "select_option_description": "Открыть форму заявки",
        "select_custom_id": "panel:semya:apply",
    },
    "vzp": {
        "label": "VZP Maps",
        "description": "Панель карт VZP — выбор карты и 2 фото",
        "accent_color": 0xB9BBBE,
        "title": "### VZP MAPS",
        "body": " ",
        "select_section_label": "Выбери карту:",
        "select_placeholder": "Выбирай",
        "select_custom_id": "panel:vzp:map",
    },
}

# --- Модальная форма заявки в семью ---
APPLICATION_MODAL = {
    "title": "Форма заявки",
    "custom_id": "modal:semya:apply",
    "fields": [
        {
            "id": "identity",
            "label": "Ваше имя, возраст, ник в игре статик на 18",
            "placeholder": "Алексей, 19, Alexis, 344",
            "style": "paragraph",
            "max_length": 1000,
            "required": True,
        },
        {
            "id": "online",
            "label": "Ваш средний онлайн + часовой пояс",
            "placeholder": "5ч, мск",
            "style": "short",
            "max_length": 100,
            "required": True,
        },
        {
            "id": "rollbacks",
            "label": "Откаты МП (мкл, капт) и ГГ (сайга и спеш)",
            "placeholder": "https://youtu.be/...",
            "style": "paragraph",
            "max_length": 1000,
            "required": True,
        },
        {
            "id": "experience",
            "label": "Ваш игровой опыт, история семей и причина поч",
            "placeholder": "Играю с открытия 4 сервера; Ag. Blade; недопонимания с Ромарито",
            "style": "paragraph",
            "max_length": 1000,
            "required": True,
        },
    ],
}

# Сообщения
MESSAGES = {
    "panel_sent": "Панель **{panel}** отправлена в {channel}.",
    "panel_no_image": "Файл `{image}` не найден в `foto_panel/`. Панель отправлена без картинки.",
    "application_sent": "Заявка отправлена. Канал: {channel}. Ожидайте ответа.",
    "ticket_embed_title": "Заявка в семью #{number}",
    "ticket_welcome": "ваша заявка. Ожидайте ответа в этом канале.",
    "ticket_review_prompt": "**Решение по заявке:**",
    "ticket_setup_need_category": "Для этого действия укажите параметр **категория**.",
    "ticket_setup_need_role": "Для этого действия укажите параметр **роль**.",
    "ticket_category_set": "Категория для тикетов: {category}",
    "ticket_role_added": "Роль {role} добавлена — видит каналы заявок.",
    "ticket_role_removed": "Роль {role} убрана из списка просмотра тикетов.",
    "ticket_role_exists": "Роль {role} уже в списке.",
    "ticket_role_missing": "Роли {role} нет в списке.",
    "ticket_settings_summary": (
        "**Настройки тикетов**\n"
        "Категория: {category}\n"
        "Роли просмотра:\n{roles}\n"
        "Роль при принятии: {accepted_role}\n"
        "Следующий номер: `ticket-{next_number:04d}`"
    ),
    "ticket_accepted_role_set": "При принятии выдаётся роль {role}.",
    "ticket_accepted": "Заявка **принята**. {user} получил(а) {role}. Канал закрыт.",
    "ticket_accepted_left_server": (
        "Заявка **принята**. Пользователь вышел с сервера — "
        "роль {role} не выдана. Канал закрыт."
    ),
    "ticket_rejected": "Заявка **отклонена** ({user}). Канал закрыт.",
    "ticket_review_no_permission": "Принимать и отклонять могут только настроенные роли персонала.",
    "ticket_review_no_applicant": "Не удалось определить заявителя из сообщения.",
    "ticket_review_wrong_channel": "Кнопки работают только в канале тикета.",
    "ticket_no_accepted_role": (
        "Роль при принятии не задана. Настройте `/тикет-настройка` → «Роль при принятии»."
    ),
    "ticket_accepted_role_missing": "Настроенная роль при принятии удалена с сервера.",
    "ticket_role_grant_failed": (
        "Не удалось выдать роль: проверьте, что роль бота выше роли заявителя."
    ),
    "ticket_close_failed": "Не удалось удалить канал тикета (права бота).",
    "ticket_no_category": (
        "Тикеты не настроены: администратор должен указать категорию "
        "через `/тикет-настройка` → «Категория для тикетов»."
    ),
    "ticket_no_roles": (
        "Тикеты не настроены: добавьте хотя бы одну роль "
        "через `/тикет-настройка` → «Роль просмотра — добавить»."
    ),
    "ticket_create_failed": "Не удалось создать канал заявки. Попробуйте позже.",
    "ticket_bot_permissions": (
        "У бота нет прав создавать каналы в категории. "
        "Выдайте **Управление каналами** и доступ к категории."
    ),
    "no_permission": "У вас нет прав на использование этой команды.",
    "vzp_map_no_images": (
        "Фото для **{map}** не найдены в `{folder}/`.\n"
        "Нужны файлы: {files}"
    ),
    "war_channel_set": "Статистика войн (embed) → {channel}.",
    "war_report_channel_set": "Запрос скрина и фото → {channel}.",
    "war_report_channel_missing": (
        "Канал для скринов не настроен. `/война-настройка` → «Канал скринов» "
        "или **WAR_REPORT_CHANNEL_ID** в .env."
    ),
    "war_setup_need_channel": "Укажите параметр **канал**.",
    "war_setup_need_role": "Укажите параметр **роль**.",
    "war_setup_need_minutes": "Укажите параметр **минут** (от 1 до 1440).",
    "war_cd_minutes_set": "КД **{kind}** — **{minutes} мин**. Панель обновлена.",
    "war_settings_summary": (
        "**Настройки войн**\n"
        "• Статистика (embed): {stats}\n"
        "• Скрины: {screenshots}\n"
        "• Кулдауны: {cooldowns}\n"
        "• КД атаки: **{attack_cd} мин** · защиты: **{defense_cd} мин**\n"
        "• Роль для тега: {ping_role}"
    ),
    "war_parse_failed": "Не удалось разобрать текст. Скопируйте сообщение из TG целиком.",
    "war_test_sent": "Отправлено в канал войн (как из Telegram).",
    "war_ping_screenshot": (
        "{mentions} — скиньте **скрин боя** "
        "(ответом на это сообщение или фото в этот канал, **30 мин**).\n"
        "**{location}** · бой **#{battle_id}** · **{outcome}**"
    ),
    "war_screenshot_done": "✅ Скрин добавлен в embed.",
    "war_ping_role_set": "Для тега при исходе будет использоваться {role}.",
    "war_cd_channel_set": (
        "Панель кулдаунов отправлена в {channel}. "
        "При забивке из TG таймеры обновятся автоматически."
    ),
    "log_setup_need_channel": "Укажите параметр **канал**.",
    "log_actions_channel_set": "Канал **логов** (мут, move и т.д.) → {channel}.",
    "log_usage_channel_set": "Канал **логов бота** (кто какие команды использует) → {channel}.",
    "log_enabled": "Логирование на этом сервере **включено**.",
    "log_disabled": "Логирование на этом сервере **выключено**.",
    "log_settings_summary": (
        "**Настройки логов**\n"
        "• Статус: {status}\n"
        "• Логи (модерация): {actions}\n"
        "• Логи бота (команды): {usage}"
    ),
}
