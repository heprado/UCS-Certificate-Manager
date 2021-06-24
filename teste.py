from datetime import datetime
import pytz

ucs_time = "May 30 23:59:12 2026 GMT"

ucs_obj = datetime.strptime(ucs_time,"%a %d ")

timezone = pytz.timezone("America/Sao_Paulo")


hm = timezone.localize(ucs_time)

print(hm)