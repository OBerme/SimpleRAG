



# 1. Función de extracción de índices (basada en la respuesta anterior)
def find_end_index_of_word(content_string: str, word_to_find: str = "ACTUALIZADO") -> int:
    """Busca la última ocurrencia de la palabra y devuelve el índice de su ÚLTIMO carácter."""
    start_index = content_string.rfind(word_to_find)
    
    if start_index != -1:
        return start_index + len(word_to_find) - 1
    else:
        raise Error("Not founded the word: " + word_to_find)
    
    
def find_end_index_of_word_reverse(content_string: str, word_to_find: str = "ACTUALIZADO") -> int:
    """Busca la última ocurrencia de la palabra y devuelve el índice de su ÚLTIMO carácter."""
    start_index = content_string.rfind(word_to_find)
    
    if start_index != -1:
        return len(content_string) - (start_index + len(word_to_find) - 1)
    else:
        raise Error("Not founded the word: " + word_to_find)
