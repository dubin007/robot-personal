# from snownlp import SnowNLP


def __preprocessing(text):
    # 去除空格
    text = text.replace(" ", "")
    # 去除换行符
    text = text.replace("\n", "")
    # 去除引号
    text = text.replace("\"", "").replace("\'", "").replace("“", "").replace("”", "")
    return text

def get_text_summary(text, topK=5):
    text = __preprocessing(text)
    return [text[:20]]
    # s = SnowNLP(text)
    # topK_titles = s.summary(topK)
    # return topK_titles

if __name__ =='__main__':
    test_str = '日本读卖电视台报道“中国7省市共派遣约1000名医务人员赴武汉疫区”，由于日语表达习惯性省略主语，有网友根据报道画面显示的字错误解读为“日本派遣1000人医疗队前往武汉”。'
    print(get_text_summary(text=test_str, topK=1))