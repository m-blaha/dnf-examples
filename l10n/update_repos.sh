#!/bin/bash
set -ex

BASE_PATH="git@github.com:rpm-software-management"
REPOS=(
    'dnf:master'
    'libdnf:master'
    'libdnf:dnf-4-master'
    'dnf-plugins-core:master'
    'dnf-plugins-extras:master'
)

GIT_COMMITER_NAME="DNF github localization bot"
GIT_COMMITER_EMAIL="mblaha+l10n@redhat.com"

PROG_PATH=$(dirname $(readlink -f -- $0))

error() {
    printf >&2 "Error: %s\n" "$*"
    exit 1
}

pushd () {
    command pushd "$@" > /dev/null
}

popd () {
    command popd "$@" > /dev/null
}

for repobranch in ${REPOS[@]}; do
    old_IFS=$IFS
    IFS=: read -a repo <<< "$repobranch"
    IFS=${old_IFS}
    L10N_REPO="${repo[0]}-l10n"
    POT_FILE="${repo[0]}.pot"
    TMP_DIR=$(mktemp -d --tmpdir= "l10n-tmp.${L10N_REPO}.XXXXXXXX")
    if [[ ! -e "$TMP_DIR" ]]; then
        error "Error creating temp directory for repo ${L10N_REPO}."
    fi
    git clone --depth=1 -b master ${BASE_PATH}/${L10N_REPO}.git ${TMP_DIR}
    pushd ${TMP_DIR}
        ./script/update_source_pot.sh ${repo[1]}
        git config user.email "${GIT_COMMITER_EMAIL}"
        git config user.name "${GIT_COMMITER_NAME}"
        git add ${POT_FILE}
        git commit -m 'Update source file'
        git push origin master
    popd
    rm -rf $TMP_DIR
done;


