#!/usr/bin/python3
import dnf

base = dnf.Base()
base.read_all_repos() 
base.fill_sack()

module_base = dnf.module.module_base.ModuleBase(base)
module_packages, nsvcap = module_base.get_modules('nodejs:11/minimal')

print("Parsed NSVCAP:")
print("name:", nsvcap.name)
print("stream:", nsvcap.stream)
print("version:", nsvcap.version)
print("context:", nsvcap.context)
print("arch:", nsvcap.arch)
print("profile:", nsvcap.profile)

print("Matching modules:")
for mpkg in module_packages:
    print(mpkg.getFullIdentifier())
    print(mpkg.getDescription())
