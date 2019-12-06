#!/usr/bin/python3
import dnf

base = dnf.Base()
base.read_all_repos()
base.fill_sack()
q = base.sack.query()

a = q.available()
a = a.filter(name='acpi')
print("Available acpi packages:")
for p in a:  # a only gets evaluated here
    print('{} in repo {}'.format(p, p.reponame))


#i = i.filter(name__glob='*dnf*')
