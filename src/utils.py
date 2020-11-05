from typing import List

def load_keywords(path: str) -> List[str]:
    with open(path, 'r') as f:
        data = f.read().split('\n')

    return data