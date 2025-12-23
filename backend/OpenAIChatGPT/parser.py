SPLIT_KEY_STR = '---------------'
SPLIT_LINKS_STR = '@@@@@@@@@@@@@@@'
SPLIT_LINKS_SEPARATOR = ','
DEBUG_MODE = True


def clean_response_str(response):
    response = response.replace('\n', '')
    return response.strip()
    
def get_list_response(response):
    split_sum_up = response.split(SPLIT_KEY_STR, 2)
    sum_up = split_sum_up[1]
    split_links = sum_up.split(SPLIT_LINKS_STR,2)
    
    return [ split_sum_up[0], split_links[0], split_links[1]]
    # return [ split_sum_up[0]]


def get_list_links(links):
    final_links = None
    try:
        final_links = links.split(SPLIT_LINKS_SEPARATOR)
    except:
        print("Ocurrio un error interno a la hora de separar los links")
        final_links = links
    return final_links



def get_json_model_response(response):
    response_parsed = get_list_response(response)
    
    answer = response_parsed[0]
    new_chat_title = clean_response_str(response_parsed[1]) # El título que viene de la IA
    links = get_list_links(clean_response_str(response_parsed[2]))
    
    return {
        "answer": answer, 
        "chat_title": new_chat_title, 
        "links": links
    }