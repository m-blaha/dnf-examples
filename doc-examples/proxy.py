import dnf

base = dnf.Base()

conf = base.conf
conf.proxy = "http://the.proxy.url:3128"
conf.proxy = "http://192.168.1.45:3128"
conf.proxy_username = "username"
conf.proxy_password = "secret"

base.read_all_repos()
base.fill_sack()

q = base.sack.query()
a = q.available()
for p in a:
    print('{} in repo {}'.format(p, p.reponame))
