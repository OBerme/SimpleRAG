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


# Pre: get_title_url es un delegado una funcion que va conseguir a traves de una url un titulo
def get_json_model_response(response, get_title_url):
    response_parsed = get_list_response(response)
    answer = response_parsed[0]
    new_chat_title = clean_response_str(response_parsed[1]) # El título que viene de la IA
    raw_links = get_list_links(clean_response_str(response_parsed[2].replace('@', '')))
    
    links = [ {"raw_link" : next_raw_link , "title" : get_title_url(next_raw_link)} for next_raw_link in raw_links]
    
    return {
        "answer": answer, 
        "chat_title": new_chat_title, 
        "links": links
    }
    