from django_cron import CronJobBase, Schedule
from datetime import timedelta
from django.utils import timezone
from .models import OTPStore

class DeleteExpiredOTPJob(CronJobBase):
    RUN_EVERY_MINS = 1  # You can keep it 5 in production

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'data.delete_expired_otp'

    def do(self):
        try:
            expiration_time = timezone.now() - timedelta(minutes=5)
            expired_otps = OTPStore.objects.filter(timestamp__lt=expiration_time)
            count = expired_otps.count()
            deleted, _ = expired_otps.delete()

            print(f"[CRON] Found {count} expired OTP(s). Deleted {deleted}. Timestamp: {timezone.now()}")

            # Optional: Write to a log file to debug cron failures
            with open("cron_debug.log", "a") as f:
                f.write(f"[{timezone.now()}] Deleted {deleted} out of {count} expired OTPs.\n")

        except Exception as e:
            print(f"[CRON ERROR] Failed to delete expired OTPs: {str(e)}")
            with open("cron_debug.log", "a") as f:
                f.write(f"[{timezone.now()}] ERROR: {str(e)}\n")
