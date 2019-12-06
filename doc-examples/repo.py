#!/usr/bin/python3
import dnf

base = dnf.Base()
base.read_all_repos()
base.fill_sack()

repos = base.repos.get_matching('*-debuginfo')
repos.disable()
