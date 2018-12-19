from django import template

register = template.Library()

@register.filter
def create_popup_id(iteration):
    """

    :param iteration:
    :return:
    """
    return 'popup' + str(iteration)


@register.filter
def create_popup_id_query_selector(iteration):
    """

    :param iteration:
    :return:
    """
    return '#' + 'popup' + str(iteration)


@register.filter
def create_token_content_id(iteration):
    """

    :param iteration:
    :return:
    """
    return 'tokenContent' + str(iteration)
