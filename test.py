from datetime import datetime, timezone

now = datetime.now(timezone.utc)
month_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
print(now)
print(month_start)