#!/usr/bin/python3
import dnf

base = dnf.Base()
conf = base.conf
conf.cachedir = '/tmp/my_cache_dir'
conf.substitutions['releasever'] = '30'
conf.substitutions['basearch'] = 'x86_64'

base.repos.add_new_repo('my-repo', conf,
    baseurl=["http://download.fedoraproject.org/pub/fedora/linux/releases/$releasever/Everything/$basearch/os/"])
base.fill_sack()

print("Enabled repositories:")
for repo in base.repos.iter_enabled():
    print("id: {}".format(repo.id))
    print("baseurl: {}".format(repo.baseurl))
