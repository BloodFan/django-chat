from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class ChatPagination(PageNumberPagination):
    '''Пока нигде не используется'''
    page_size = 2
    page_size_query_param = 'page_size'  # ?page=1&page_size=3(вручную задаем кол-во объектов на стр)
    max_page_size = 10


class ChatLimitOffsetPagination(LimitOffsetPagination):
    '''Пока нигде не используется'''
    max_limit = 10  # ?limit=5&offset=0 кол-во и смещение
    limit_query_param = 'limit' # значения по умолчанию
    offset_query_param = 'offset' # значения по умолчанию
