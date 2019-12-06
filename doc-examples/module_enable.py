#!/usr/bin/python3
import dnf

base = dnf.Base()
base.read_all_repos() 
base.fill_sack()

module_base = dnf.module.module_base.ModuleBase(base)
module_base.enable(['nodejs:11'])

#base.do_transaction()
