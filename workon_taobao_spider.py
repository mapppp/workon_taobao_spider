import requests
import re
import json
import time


class TaoSpider:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        self.cookies = "miid=1251581815637967137; t=781bf38a2cb7c1017ea65e968391e523; cna=+YcwFThx9EYCAXs1vywHDGJn; tg=0; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; UM_distinctid=169fac7a4d2135-08813818d9d75-39395704-12c000-169fac7a4d3194; _uab_collina=155512050097305009061934; enc=2id%2FTiaJkaPFwNn%2FlqKD7AcwagUggjsbtgAYRvyr8WlxgaGOVZW26wPj6EQYzuOqDUrVi54jQTQJaV83yehs7g%3D%3D; _m_h5_tk=17028522c9133f21828e193e5bb56646_1556009434965; _m_h5_tk_enc=eed07f4681c75336e4e311b5d0e1dcd1; _cc_=VT5L2FSpdA%3D%3D; mt=ci=0_0; JSESSIONID=6CACC2CE298301F5172CAA5154058809; isg=BDQ0Yvo61KNdGUAB38QTXHFlBfJmpVidiwb4vs6Rpr8dOdaD9R_YhvSwuRFEwZBP; l=bBMXRMcmvnXlmJTdBOfNZuI8at7tfCAbzsPzw4_GfICPOQfpDEZlWZOJnaT9C3GVa6U283rLI0XzBXYTWy4e0"
        self.referer = "https://s.taobao.com/search?q=%E8%80%B3%E9%92%89&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190427&ie=utf8&filter=reserve_price%5B%2C25%5D&sort=sale-desc"
        self.headers = {"User-Agent": self.user_agent, "Cookie": self.cookies, "referer": self.referer}
        self.page_num = 1
        self.root_url = "https://s.taobao.com/search?spm=a230r.1.14.17.7f3933a3qvnGgH&type=samestyle&app=i2i&rec_type=1&uniqpid=-1272557146&nid=589190196973"
        self.items = {}
        self.pass_id = []
        # self.rq = requests.request(headers=self.headers)

    def __req(self):
        pass

    def __set_cookies(self):
        pass

    def __set_user_agent(self):
        with open('user-agent.txt','r',encoding="utf-8")as fp:
            s = fp.read()
            uli = json.loads(s, strict=False)

    def __test(self, t):
        with open("test.txt", "w", encoding="utf-8") as wf:
            wf.write(t)

    def get_headers(self):
        with open("headers.js", "r", encoding="utf-8") as rf:
            self.headers = json.load(rf)

    def set_root_url(self):
        url = input("url:")
        if url == "":
            return
        else:
            self.root_url = url
        return

    def set_page_num(self):
        page_num = input("set_pageNum:")
        if page_num == "":
            try:
                r = requests.get(self.root_url, headers=self.headers)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                # self.__test(r.text)
                pat = re.compile(r'g_page_config = (\{.*\});')
                if pat.search(r.text) is not None:
                    root_rec_items = pat.search(r.text).group(1)
                    txt = json.loads(root_rec_items)
                    self.page_num = int(int(txt["mods"]["pager"]["data"]["totalCount"])/60+1)
            except:
                pass
            print(self.page_num)
        else:
            self.page_num = int(page_num)
        return

    def set_pass_id(self):
        pass_id = input("pass_id(separated by whitespace):")
        if pass_id == "":
            self.pass_id.append(self.root_url.split("=")[-1])
            print(self.pass_id)
            # print(self.pass_id)
        else:
            self.pass_id = pass_id.split()
            print(self.pass_id)

    def get_rec_items(self):
        try:
            pat = re.compile(r'g_page_config = (\{.*\});')
            for i in range(0, self.page_num):
                if i == 0:
                    p_url = self.root_url
                else:
                    p_url = self.root_url + "&s=" + str(i * 60)
                try:
                    r = requests.get(p_url, headers=self.headers)
                    r.raise_for_status()
                    r.encoding = r.apparent_encoding
                    self.__test(r.text)
                    if pat.search(r.text) is not None:
                        root_rec_items = pat.search(r.text).group(1)
                        txt = json.loads(root_rec_items)
                        ili = txt["mods"]["recitem"]["data"]["items"]
                        # print(ili)
                        for item in ili:
                            item_url = "https:" + item["detail_url"]
                            ww = item["nick"]
                            print(1)
                            print("ww", ww)
                            shoplink = item["shopLink"]
                            print("shopLink", shoplink)
                            self.items[ww] = [item_url, shoplink]
                except:
                    pass
                print("items:", len(self.items), "page:%d"%(i+1))
        except Exception as e:
            print("1:", e)
            print("fail")

    def get_pass(self):
        old_items = {}
        for i in self.items:
            old_items[i] = self.items[i]
        for ww in old_items:
            iurl = old_items[ww][0]
            try:
                # 请求商品url，获取异步url
                r = requests.get(iurl, headers=self.headers)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                # self.__test(r.text)
                # 异步url正则表达式
                match = re.search(r"'(//desc.alicdn.com/.*?)',", r.text)
                # 天猫不要
                if match is None:
                    self.items.pop(ww)
                else:
                    desc_url = "https:" + match.group(1)
                    # 请求异步url，获取隐藏链接
                    r1 = requests.get(desc_url, headers=self.headers)
                    r1.raise_for_status()
                    r1.encoding = r.apparent_encoding
                    # 隐藏链接正则表达式
                    match2 = re.search(r'href="(.*?id=(\d+).*?)"', r1.text)
                    # 没有隐藏链接的不要
                    if match2 is not None:
                        id = match2.group(2)
                        if id in self.pass_id:
                            print("id:", id, "pass")
                        # 隐藏链接不对的不要
                        else:
                            print("id:", id)
                            self.items.pop(ww)
                    else:
                        self.items.pop(ww)
            except Exception as e:
                print("2:", e)
                pass

    def data_output(self):
        if len(self.items) == 0:
            return
        else:
            loc_time = time.strftime("%m-%d-%H-%M", time.localtime(time.time()))
            with open("ww/ww%s.txt"%loc_time, "a", encoding="utf-8") as wf:
                for i in self.items:
                    wf.write(i+"\t"+self.items[i][0]+"\t"+self.items[i][1]+"\n")

    def craw(self):
        self.get_headers()
        self.set_root_url()
        self.set_pass_id()
        self.set_page_num()
        self.get_rec_items()
        self.get_pass()
        self.data_output()
        print("end_item:", len(self.items))

if __name__ == "__main__":
    spiderMan = TaoSpider()
    spiderMan.craw()
