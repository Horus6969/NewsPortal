from django import template

register = template.Library()


@register.filter()
def censor(text):
    censored_text = text
    bad_words = ['выходные', 'Выходные', 'синоптик', 'Синоптик',]
    if type(text) is str:
        for bad_word in bad_words:
            censored_text = censored_text.replace(bad_word, bad_word[0] + '*' * (len(bad_word)-1) + bad_word[-1])
    else:
        raise TypeError
    return censored_text
