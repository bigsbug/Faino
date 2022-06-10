import re

extractor_ip_re = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"


def get_client_ip(response: dict) -> str:
    x_forwarded_for = response.META.get('HTTP_X_FORWARDED_FOR')
    x_real_real_ip = response.META.get('HTTP_X_REAL_IP')
    if x_real_real_ip:

        ip = x_real_real_ip
    elif x_forwarded_for:
        print(x_forwarded_for)
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = response.META.get('REMOTE_ADDR')
    x = re.search(extractor_ip_re, ip)
    if x:
        return x.group()
    return None
