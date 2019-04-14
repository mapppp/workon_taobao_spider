import requests
import re


user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
cookies = "uab_collina=155489016275312094498979; miid=1251581815637967137; t=781bf38a2cb7c1017ea65e968391e523; cna=+YcwFThx9EYCAXs1vywHDGJn; _cc_=VFC%2FuZ9ajQ%3D%3D; tg=0; enc=W%2BxP%2Be3HSWapjVgmldTU5HII1CtTMqspJoTdkxNG%2FOvmBWvOSlrUJHB1CnQ%2FskDXEVblJgtKF37N80L2K6f4uQ%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; UM_distinctid=169fac7a4d2135-08813818d9d75-39395704-12c000-169fac7a4d3194; cookie2=18f75e71419a5963b908a0432c882a36; _tb_token_=d4bee175e557; _m_h5_tk=af672610426f2563bfcd705a019f71a8_1554890877852; _m_h5_tk_enc=38be8dd4ca3e748951c0b9b6f87b8fe1; mt=ci=0_0; XSRF-TOKEN=bc50fdf4-8ed8-4664-92fb-40e6602c2ae0; cookieCheck=6041; v=0; l=bBMXRMcmvnXlmVPzBOfiVuI8at7O5IRfGsPzw4_GfICPOgf9S1GcWZsIHR8pC3GVa6AkA3rLI0XzBvLZeyUIh; isg=BNnZ8Zyy4eWa3b12yn-mw2z-6MVzzs1ypm3lKfuOuoBvAv2UU7U-6LVQBIbRumVQ"
headers = {"User-Agent": user_agent, "Cookie": cookies}
url = "https://item.taobao.com/item.htm?id=589988332199&ns=1#detail"

# for i in self.items:
try:
	# 获取异步加载商品描述的url
	r = requests.get(url, headers=headers)
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	#with open("hiden.txt", "w", encoding="utf-8") as wf:
	#	wf.write(r.text)
	match = re.search(r"'(//desc.alicdn.com/.*?)',", r.text)
	# 天猫不要
	if match == None:
		pass  # self.items.remove(i)
	desc_url = "https:" + match.group(1)
	# 获取隐藏链接id字段
	r1 = requests.get(desc_url, headers=headers)
	r1.raise_for_status()
	r1.encoding = r.apparent_encoding
	print(r1.text)
	match2 = re.search(r'href="(.*?id=(\d+).*?)"', r1.text)
	# 没有隐藏链接的不要
	if match2 is not None:
		id = match2.group(2)
		print(id)
	else:
		print("hiden url match none")
		pass  # self.items.remove(i)
	# 隐藏链接不对的不要
	if id not in []:  #[] = self.pass_id
		pass  # self.items.remove(i)
except Exception as e:
	print(e)
	pass
