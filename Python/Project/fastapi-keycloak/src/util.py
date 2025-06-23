from typing import List
from regex import regex

def parse_list(query: str) -> List[str]:
    pattern = r'\[([^,]+,)*([^,]+)\]'
    extract = r'[^\[\],]+'
    
    if regex.match(pattern, query):
        return regex.findall(extract, query)
    else:
        raise TypeError('Expected a list')