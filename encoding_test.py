import re
import json

# s = "//detail.tmall.com/item.htm?id\u003d588287086969\u0026ns\u003d1".encode('utf-8').decode('utf-8')
# print(s)

def get_items_url(file):
    items = {}
    pat = re.compile(r'g_page_config = (\{.*\});')
    with open(file, "r", encoding="utf-8") as rf:
        s = rf.read()
        rt = pat.search(s).group(1)
        txt = json.loads(rt)
    ili = txt["mods"]["recitem"]["data"]["items"]
    print(len(ili))
    for i in ili:
        item = "https:"+i["detail_url"]
        ww = i["nick"]
        items[ww] = item
    return items
# for i in range(1, len(ili)+1):

if __name__ == "__main__":
    print(get_items_url(r"text.txt"))