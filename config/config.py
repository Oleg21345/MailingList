from datetime import datetime
from pytz import timezone, UTC


BOT_TOKEN = '7803036489:AAFcRaV9uDw57KQ8AnuWEUSYnmVXoNqZSgE'


kyiv_tz = timezone("Europe/Kyiv")
WEBINAR_TIME_KYIV = kyiv_tz.localize(datetime(2025, 4, 24, 11, 15, 0))

WEBINAR_TIME = WEBINAR_TIME_KYIV.astimezone(UTC)





















