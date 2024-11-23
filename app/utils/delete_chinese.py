import re


def remove_chinese_translation(text):
    # 正则表达式匹配包含中文字符的行
    cleaned_text = re.sub(r'[^\n]*[\u4e00-\u9fff]+[^\n]*', '', text)
    # 清除可能的多余空行
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)
    return cleaned_text.strip()
