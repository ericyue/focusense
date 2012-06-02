from django import template
import random
register = template.Library()

@register.filter
def cut_str(str,length):
    is_encode = False
    try:
        str_encode = str.encode('gb18030')
        is_encode = True
    except:
        pass
    if is_encode:
        l = length*2
        if l < len(str_encode):
            l = l - 3
            str_encode = str_encode[:l]
            try:
                str = str_encode.decode('gb18030') + '...'
            except:
                str_encode = str_encode[:-1]
                try:
                    str = str_encode.decode('gb18030') + '...'
                except:
                    is_encode = False
    if not is_encode:
        if length < len(str):
            length = length - 2
            return str[:length] + '...'
    return str


@register.filter
def random_label(str,length):
    rnd=[
    "label",
    "label label-success",
    "label label-warning",
    "label label-important",
    "label label-info",
    "label label-inverse"]
    val=random.uniform(1,1000)
    return rnd[int(val)%6]
@register.filter
def shrink_price(str):
    str=str.split('-')[0].strip()
    return str

