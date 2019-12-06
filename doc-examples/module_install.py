#!/usr/bin/python3
import dnf

base = dnf.Base()
base.read_all_repos() 
base.fill_sack()

module_base = dnf.module.module_base.ModuleBase(base)
module_base.install(['nodejs:11/minimal'])

base.download_packages(base.transaction.install_set)
base.do_transaction()
