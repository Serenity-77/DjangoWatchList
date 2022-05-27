from django.conf import settings

def error_message_from_form(form):
    err_content = []
    for field, errors in form.errors.as_data().items():
        for error in errors:
            err_content.append("%s: %s" % (form.fields[field].label, error.messages[0]))
            break
    content = "\n".join(err_content)
    return content


def get_tmdb_configuration_url():
    conf_url = settings.TMDB_API_CONFIGURATION_URL
    api_key = settings.TMDB_API_KEY
    url = "%s?api_key=%s" % (conf_url.rstrip("/"), api_key, )
    return url
