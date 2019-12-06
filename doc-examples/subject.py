#!/usr/bin/python3
import dnf
import hawkey

nevra_string = "dnf-0:4.2.2-2.fc30.noarch"
subject = dnf.subject.Subject(nevra_string)
possible_nevra = subject.get_nevra_possibilities(
    forms=[hawkey.FORM_NEVRA, hawkey.FORM_NEVR])

for i,nevra in enumerate(possible_nevra):
    print("Possibility {} for \"{}\":".format(i+1, nevra_string))
    print("name: {}".format(nevra.name))
    print("epoch: {}".format(nevra.epoch))
    print("version: {}".format(nevra.version))
    print("release: {}".format(nevra.release))
    print("architecture: {}".format(nevra.arch))
    print()

