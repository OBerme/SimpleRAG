class 
SPLIT_KEY_STR = '---------------'
def get_list_response(response):
    return response.split(SPLIT_KEY_STR, 2)