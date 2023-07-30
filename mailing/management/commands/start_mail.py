from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.core.management import BaseCommand
from client.models import MailingClient
from config import settings
from mailing.models import Mail, MailingSettings, MailingTry


class Command(BaseCommand):
    '''команда для запуска рассылки периодических задач'''

    def handle(self, *args, **options):
        for mail in Mail.objects.values():
            mail_to = Mail.objects.filter(id=mail["id"]).values()
            set_of_mails = Mail.objects.get(id=mail_to[0]['id'])
            client_to_message = set_of_mails.client_to_message.all()
            list_mail_to = []
            for i in client_to_message.values_list():
                list_mail_to.append(i[2])
            setting = MailingSettings.objects.get(id=mail["settings_id"])
            if len(mail_to) > 1:
                for i in mail_to:
                    client = MailingClient.objects.get(id=i)
                    if (setting.mailing_status == "AC") and (
                            setting.mailing_periods == "DL" and setting.mailing_time_start - datetime.now() >= timedelta(
                        days=1)) or (
                            setting.mailing_periods == "WL" and setting.mailing_time_start - datetime.now() >= timedelta(
                        days=6)) or (
                            setting.mailing_periods == "ML" and setting.mailing_time_start - datetime.now() >= timedelta(
                        days=30)):
                        setting.mailing_time_start = datetime.now()
                        sending = send_mail(mail["mailing_subject"], mail["mailing_body"], settings.DEFAULT_FROM_EMAIL,
                                            recipient_list=list_mail_to,
                                            fail_silently=False)
                        if sending == 1:
                            setting.mail_status = 'OK'
                        else:
                            setting.mail_status = 'Не отправлено'

                        if (setting.mailing_periods == "DL") and ((
                                                                          setting.mailing_time_end - setting.mailing_time_start) <= timedelta(
                            days=1)):
                            setting.mailing_status = 'FI'
                            setting.save()
                        elif (setting.mailing_periods == "WL") and ((
                                                                            setting.mailing_time_end - setting.mailing_time_start) <= timedelta(
                            days=6)):
                            setting.mailing_status = 'FI'
                            setting.save()
                        elif (setting.mailing_periods == "ML") and ((
                                                                            setting.mailing_time_end - setting.mailing_time_start) <= timedelta(
                            days=30)):
                            setting.mailing_status = 'FI'
                            setting.save()

                        MailingTry.objects.create(mailing=setting, mailing_try=datetime.now(),
                                                  mailing_try_status=setting.mailing_status,
                                                  mailing_response=setting.mail_status)
            else:
                setting = MailingSettings.objects.get(id=mail["settings_id"])
                if (setting.mailing_status == "AC") and (
                        setting.mailing_periods == "DL" and setting.mailing_time_start - datetime.now() >= timedelta(
                    days=1)) or (
                        setting.mailing_periods == "WL" and setting.mailing_time_start - datetime.now() >= timedelta(
                    days=6)) or (
                        setting.mailing_periods == "ML" and setting.mailing_time_start - datetime.now() >= timedelta(
                    days=30)):
                    setting.mailing_time_start = datetime.now()
                    sending = send_mail(mail["mailing_subject"], mail["mailing_body"], settings.DEFAULT_FROM_EMAIL,
                                        recipient_list=list_mail_to,
                                        fail_silently=False)
                    if sending == 1:
                        setting.mail_status = 'OK'
                    else:
                        setting.mail_status = 'Не отправлено'

                    if (setting.mailing_periods == "DL") and ((
                                                                      setting.mailing_time_end - setting.mailing_time_start) <= timedelta(
                        days=1)):
                        setting.mailing_status = 'FI'
                        setting.save()
                    elif (setting.mailing_periods == "WL") and ((
                                                                        setting.mailing_time_end - setting.mailing_time_start) <= timedelta(
                        days=6)):
                        setting.mailing_status = 'FI'
                        setting.save()
                    elif (setting.mailing_periods == "ML") and ((
                                                                        setting.mailing_time_end - setting.mailing_time_start) <= timedelta(
                        days=30)):
                        setting.mailing_status = 'FI'
                        setting.save()

                    MailingTry.objects.create(mailing=setting, mailing_try=datetime.now(),
                                              mailing_try_status=setting.mailing_status,
                                              mailing_response=setting.mail_status)
