#!/usr/bin/python3
import dnf

base = dnf.Base()
base.fill_sack()
q = base.sack.query()

i = q.installed()
i = i.filter(name='dnf')
packages = list(i) # i only gets evaluated here
print("Installed dnf package:")
for p in packages:
    print(p, p.reponame)


#i = i.filter(name__glob='*dnf*')
