import re


def filter_num(text):
    if text is None:
        return 0
    else:
        pattern = re.compile(r'(\d+)',re.S)
        result = re.search(pattern, text)
        if result is None:
            return 0
        else:
            return int(result[0])

def filter_date(text):
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2})', re.S)
    result = re.search(pattern, text)
    if result is None:
        return 0
    else:
        return result[0] + ' 00:00:00'


def filter_label(text):
    if text is not None:
        pattern = re.compile(r'(<.*?>)', re.S)
        return re.sub(pattern, '', text)


def filter_author_time(text):
    if text is not None:
        author_time = text.split()
        return author_time[0], author_time[1]
    else:
        return None,None

if __name__ == '__main__':
    a="编辑与 2180-11-11"
    res = filter_date(a)
    print(res)