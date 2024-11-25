import re


def remove_chinese_translation(text):
    # 正则表达式匹配包含中文字符的行
    cleaned_text = re.sub(r'[^\n]*[\u4e00-\u9fff]+[^\n]*', '', text)
    # 清除可能的多余空行
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)
    return cleaned_text.strip()


if __name__ == '__main__':
    text = """Bithumb Listing: [마켓 추가] 바이코노미(BICO), 퍼퍼(PUFFER) 원화 마켓 추가
Bithumb上新: [市场追加] BICO、PUFFER赢得市场追加


$BICO
————————————
2024-11-25 09:56:20
source: https://feed.bithumb.com/notice/1645252"""

    result = remove_chinese_translation(text)
    print(result)