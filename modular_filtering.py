#!/usr/bin/python3

import dnf
import hawkey

def get_set_of_name_artifacts(versions):
    name_set = set()
    for module in versions:
        req_list = []
        for nevra in module.getArtifacts():
            subject = dnf.subject.Subject(nevra)
            nevras = subject.get_nevra_possibilities(forms=[hawkey.FORM_NEVRA])
            for nevra_obj in nevras:
                if nevra_obj.name.endswith("-debuginfo") or nevra_obj.name.endswith("-debugsource"):
                    continue
                name_set.add(nevra_obj.name)
    return name_set

class TestModules():

    def __init__(self, releasever=None):
        self.base = dnf.base.Base()
        if releasever:
            self.base.conf.releasever = releasever
        self.base.read_all_repos()
        self.base.fill_sack(load_system_repo=False)
        self.modules = self.base._moduleContainer.getModulePackages()

    def parse_artifact(self, artifact):
        '''return [names] corresponding to artifact'''
        subject = dnf.subject.Subject(artifact)
        nevras = subject.get_nevra_possibilities(forms=[hawkey.FORM_NEVRA])
        return [nevra for nevra in nevras]

    def artifacts_names(self, artifacts):
        names = []
        for artifact in artifacts:
            for nevra in self.parse_artifact(artifact):
                names.append(nevra.name)
        return names

    def filter_name_provide(self, module):
        names = self.artifacts_names(module.getArtifacts())
        artifacts_q = self.base.sack.query(flags=hawkey.IGNORE_EXCLUDES).filterm(
            nevra_strict=module.getArtifacts())
        # filter packages by name
        names_q = self.base.sack.query(flags=hawkey.IGNORE_EXCLUDES).filterm(name=names)
        names_q = names_q.difference(artifacts_q)
        # filter packages by provide
        provides_q = self.base.sack.query(flags=hawkey.IGNORE_EXCLUDES).filterm(provides=names)
        provides_q = provides_q.difference(artifacts_q)
        return names, names_q, provides_q

    def reldep_iter(self, reldeps):
        for reldep in reldeps:
            rd = str(reldep)
            yield rd.split(' ')[0], rd

    def compare_filtering(self):
        '''compares modular filtering base on names and provides and names only'''
        modules_count = packages_count = 0
        for module in self.modules:
            names, names_q, provides_q = self.filter_name_provide(module)
            dif = provides_q.difference(names_q).run()
            if dif:
                modules_count += 1
                print("Module: {}".format(module.getFullIdentifier()))
                for pkg in dif:
                    packages_count += 1
                    print("  {}".format(pkg))
                    provides = set([
                        provide
                        for p_name, provide in self.reldep_iter(pkg.provides)
                        if p_name in names])
                    print("    provides:", ', '.join(provides))
                    if pkg.obsoletes:
                        print("    obsoletes:", ', '.join(
                            [obsolete
                             for o_name, obsolete in self.reldep_iter(pkg.obsoletes)]))
                print()
        print("Number of modules affected:", modules_count)
        print("Number of packages affected:", packages_count)


if __name__ == '__main__':
    tm = TestModules(releasever='31')
    tm.compare_filtering()
