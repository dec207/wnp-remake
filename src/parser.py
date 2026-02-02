from typing import Tuple, Optional

# 무시할 단어들 (전치사, 관사 등)
IGNORE_WORDS = {"THE", "A", "AN", "AT", "TO", "WITH", "IN", "ON"}

def parse_input(user_input: str) -> Tuple[Optional[str], Optional[str]]:
    """
    사용자 입력을 받아 (동사, 명사) 형태의 튜플로 반환합니다.
    예: "Throw the pod" -> ("THROW", "POD")
    """
    if not user_input:
        return None, None

    # 1. 대문자 변환 및 공백 분리
    tokens = user_input.strip().upper().split()
    
    # 2. 불용어 제거
    tokens = [t for t in tokens if t not in IGNORE_WORDS]

    if not tokens:
        return None, None

    verb = tokens[0]
    noun = None
    
    # 3. 명사 추출 (동사 이후의 단어들을 합침)
    if len(tokens) > 1:
        noun = " ".join(tokens[1:])
    
    return verb, noun
