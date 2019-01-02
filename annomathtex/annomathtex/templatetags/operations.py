from django import template

register = template.Library()

@register.filter
def create_popup_id(iteration):
    """

    :param iteration:
    :return:
    """
    return 'popup' + iteration


@register.filter
def create_popup_id_query_selector(iteration):
    """

    :param iteration:
    :return:
    """
    return '#' + 'popup' + iteration


@register.filter
def create_token_content_id(iteration):
    """

    :param iteration:
    :return:
    """
    return 'tokenContent' + iteration


@register.filter
def current_iteration(parent_iteration, child_iteration):
    """

    :param parent_iteration:
    :param child_iteration:
    :return:
    """
    return str(parent_iteration) + '-' + str(child_iteration)
