import requests
import re
import json
import time


class TaoSpider:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        self.cookies = "miid=1251581815637967137; t=781bf38a2cb7c1017ea65e968391e523; cna=+YcwFThx9EYCAXs1vywHDGJn; tg=0; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; UM_distinctid=169fac7a4d2135-08813818d9d75-39395704-12c000-169fac7a4d3194; swfstore=145103; cookie2=1578a4478b571e9eae7b1da9c0e2ae56; _tb_token_=5d1dee854465e; _uab_collina=155512050097305009061934; _m_h5_tk=f0f07c29543cd80a647911aed1465e51_1555217117907; _m_h5_tk_enc=b24e36d02e775e07cfa8643cce581e47; alitrackid=www.taobao.com; v=0; skt=0f520f451217c3bb; csg=13c81ff4; uc3=vt3=F8dByEiYDwC3UEivgM4%3D&id2=UoH7LXu2CGXQiA%3D%3D&nk2=DgVepHGh%2B3rAvw%3D%3D&lg2=W5iHLLyFOGW7aA%3D%3D; existShop=MTU1NTIyMDk2OA%3D%3D; tracknick=m543260832; lgc=m543260832; _cc_=VFC%2FuZ9ajQ%3D%3D; dnk=m543260832; enc=4pitEtpYVhFzXv2S4x8YqdqfY9LoyrsQev2moL5VT0fv9T0fVVkZjlhHzFLGJ0jRRRf%2FPQmawyr01fT0HwrWbA%3D%3D; lastalitrackid=login.taobao.com; mt=ci=18_1; whl=-1%260%260%261555223509874; JSESSIONID=143F561E7B90EF5696762C4B6F07682C; l=bBMXRMcmvnXlm03tBOCiquI8at7tMIRAguPRwN2Xi_5Il18s84_OlZrF4eJ6Vj5R_aYB4keiqTJ9-etkq; isg=BKOjkRDk-zi9d7cUZHGMQeoIMueNMDewYBtvi9UAioJ5FMM2XWn6KqFGDqS_tI_S; uc1=cookie14=UoTZ4Sf%2FlUG6dg%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=U%2BGCWk%2F7p4sj&tag=8&cookie15=W5iHLLyFOGW7aA%3D%3D&pas=0"
        self.headers = {"User-Agent": self.user_agent, "Cookie": self.cookies}
        self.page_num = 1
        self.root_url = "https://s.taobao.com/search?spm=a230r.1.14.180.59161f5dWI3JfC&type=samestyle&app=i2i&rec_type=1&uniqpid=-1693057917&nid=589419870826"
        self.items = {}
        self.pass_id = []
        # self.rq = requests.request(headers=self.headers)

    def __set_cookies():
        pass
        
    def __set_user_agent():
        with open('user-agent.txt','r',encoding="utf-8")as fp:
            s = fp.read()
            uli = json.loads(s, strict=False)

    def __test(self, t):
        with open("test.txt", "w", encoding="utf-8") as wf:
            wf.write(t)

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
                    if pat.search(r.text) is not None:
                        root_rec_items = pat.search(r.text).group(1)
                        txt = json.loads(root_rec_items)
                        ili = txt["mods"]["recitem"]["data"]["items"]
                        for item in ili:
                            item_url = "https:" + item["detail_url"]
                            ww = item["nick"]
                            self.items[ww] = item_url
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
            iurl = old_items[ww]
            try:
                # 获取异步加载商品描述的url
                r = requests.get(iurl, headers=self.headers)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                # self.__test(r.text)
                match = re.search(r"'(//desc.alicdn.com/.*?)',", r.text)
                # 天猫不要
                if match is None:
                    self.items.pop(ww)
                else:
                    desc_url = "https:" + match.group(1)
                    # 获取隐藏链接id字段
                    r1 = requests.get(desc_url, headers=self.headers)
                    r1.raise_for_status()
                    r1.encoding = r.apparent_encoding
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
        loc_time = time.strftime("%m-%d-%H-%M", time.localtime(time.time()))
        with open("ww/ww%s.txt"%loc_time, "a") as wf:
            for i in self.items:
                wf.write(i+"\t"+self.items[i]+"\n")


if __name__ == "__main__":
    spiderMan = TaoSpider()
    spiderMan.set_root_url()
    spiderMan.set_pass_id()
    spiderMan.set_page_num()
    spiderMan.get_rec_items()
    spiderMan.get_pass()
    spiderMan.data_output()
    print("end_item:", len(spiderMan.items))
