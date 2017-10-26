# UTILS
import hashlib, re, time
from datetime import date
from dateutil.relativedelta import relativedelta
from pytz import timezone

from django.core.urlresolvers import reverse_lazy
from pushbullet import Pushbullet
from django.core.mail import send_mail
from django.conf import settings


def send_data_to_user(user, subject, body, is_link=False):
    if user.pb_token is not None and user.pb_token is not u"" and user.pb_token is not "":
        try:
            pb = Pushbullet(user.pb_token)
            if is_link:
                push = pb.push_link(title=subject, url=body)
            else:
                push = pb.push_note(subject, body)
            return push
        except:
            return send_mail_m(user, subject, body, is_link, True)
    else:
        return send_mail_m(user, subject, body, is_link, False)


def generate_md5_id(char, id):
    hash = hashlib.md5(str(time.time()) + str(id) + char + str(time.time())).hexdigest()
    hash_numbers = re.sub("[^0-9]", "", hash)
    return char + hash_numbers[:6]


def send_mail_m(user, subject, body, is_link=False, fallback=False):
    ex_body = ""
    if fallback:
        ex_body = "MENSAJE ENVIADO POR SISTEMA DE RECUPERACION - PUSHBULLET HA FALLADO\n\n"
    if is_link:
        ex_body += "Consulta el siguiente enlace: "

    return send_mail(subject=subject, message=ex_body + body,
                     from_email="intranet@mundiaguabalear.com", recipient_list=[user.email])


def get_return_from_id(search_text):
    intervention_r = re.compile('[v|V][0-9]+')
    idegis_r = re.compile('[x|X][0-9]+')
    ath_r = re.compile('[a|A][0-9]+')
    client_r = re.compile('[c|C][0-9]+')
    engine_r = re.compile('[e|E][0-9]+')
    budget_r = re.compile('[p|P][0-9]+')

    intervention_m = intervention_r.match(search_text)
    if intervention_m is not None:
        idstr = intervention_m.group()
        id = int(re.sub("[^0-9]", "", idstr))
        return {"found": True, "url": reverse_lazy('intervention:intervention-view', kwargs={"pk": id})}

    budget_m = budget_r.match(search_text)
    if budget_m is not None:
        idstr = budget_m.group()
        id = int(re.sub("[^0-9]", "", idstr))
        return {"found": True, "url": reverse_lazy('budget:budget-view', kwargs={"pk": id})}

    idegis_m = idegis_r.match(search_text)
    if idegis_m is not None:
        idstr = idegis_m.group()
        id = int(re.sub("[^0-9]", "", idstr))
        return {"found": True, "url": reverse_lazy('repair:repair-idegis-view', kwargs={"pk": id})}

    ath_m = ath_r.match(search_text)
    if ath_m is not None:
        idstr = ath_m.group()
        id = int(re.sub("[^0-9]", "", idstr))
        return {"found": True, "url": reverse_lazy('repair:repair-ath-view', kwargs={"pk": id})}

    client_m = client_r.match(search_text)
    if client_m is not None:
        idstr = client_m.group()
        id = int(re.sub("[^0-9]", "", idstr))
        return {"found": True, "url": reverse_lazy('client:client-view', kwargs={"pk": id})}

    engine_m = engine_r.match(search_text)
    if engine_m is not None:
        idstr = engine_m.group()
        id = int(re.sub("[^0-9]", "", idstr))
        return {"found": True, "url": reverse_lazy('engine:engine-view', kwargs={"pk": id})}

    return {"found": False, "url": None}


def get_time_zone():
    return timezone(settings.TIME_ZONE)


def has_to_change_password(d):
    return date.today() > (d + relativedelta(years=1, days=1))


def create_amazon_client(service):
    import boto3
    try:
        client = boto3.client(service,
                              aws_access_key_id=settings.AWS_ACCESS_KEY,
                              aws_secret_access_key=settings.AWS_SECRET_KEY,
                              region_name=settings.AWS_REGION
                              )
        return client
    except:
        return None
