from typing import List, Any


def split_list_into_chunks(elements: List[Any], chunk_size: int) -> List[List[Any]]:
    return [elements[i:i + chunk_size] for i in range(0, len(elements), chunk_size)]
