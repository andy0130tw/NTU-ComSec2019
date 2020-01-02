import base64
import urllib
import requests

from padding_oracle import *
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

sess = requests.session()

SESSION_KEY = 'sna8a3f7nivkt63gvnggb3jos4'
BLOCK_SIZE = 16
NUM_THREADS = 8

cookiejar = requests.utils.cookiejar_from_dict({'PHPSESSID': SESSION_KEY})
sess.cookies = cookiejar

from_cookie = 'cPdUk0i7t%2BFOY2UdBHwtqoUCFDXp7nRGyQ4lbcacz7iGju%2FRgKwIYf%2BAWflR%2FNPGmuNKv3%2FEapARIMWlZ9NsyAYs5ZcSXwR6gz50d5L2haVDhnbR%2B%2FYn2EkB%2B0sMw1G5'
encoded = urllib.parse.unquote(from_cookie)
cipher = base64_decode(encoded)


def oracle(payload):
    flag = base64.b64encode(payload)

    r = sess.get('https://edu-ctf.csie.org:10190/party.php',
        proxies=dict(https='socks5://localhost:8888'),
        cookies={
            'FLAG': urllib.parse.quote(flag, safe=''),
        },
        verify=False,
        )

    if 'What the flag?! CHEATER!!!' in r.text:
        return False
    if '<h1>CAT PARTY!!!!!!</h1>' in r.text:
        return True

    print(r.text)
    raise Exception('Unknown response from server')


plaintext = padding_oracle(cipher, BLOCK_SIZE, oracle, NUM_THREADS)
print(remove_padding(plaintext).decode())
