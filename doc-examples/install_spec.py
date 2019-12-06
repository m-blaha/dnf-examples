#!/usr/bin/python3
import dnf
import dnf.cli.progress

base = dnf.Base()
conf = base.conf
conf.basearch = 'aarch64'
conf.installroot = '/tmp/installroot'
base.read_all_repos()
base.fill_sack(load_system_repo=False)

base.install_specs(['acpi']) #, '@Web Server', '@core'])
print("Resolving transaction...",)
base.resolve()
print("Downloading packages...")
progress = dnf.cli.progress.MultiFileProgressMeter()
pkgs_to_download = base.transaction.install_set
base.download_packages(pkgs_to_download, progress)
print("Installing...")
base.do_transaction()
