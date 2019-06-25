#!/usr/bin/python
# -*- coding: utf-8 -*-

# Job Céspedes <jobcespedes@gmail.com> idea from
# https://github.com/ansible/ansible/issues/35665#issuecomment-375859256
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
author: Job Céspedes (@jobcespedes)
module: create_ks_iso
short_description: Create OEMDRV ISO with kickstart file
description:
- This module creates an OEMDRV ISO with a kickstart file to boot from it
version_added: "2.7"
options:
  src:
    description:
    - The kickstart file source to include in the iso.
    required: true
  dest:
    description:
    - The destination directory for the iso.
    required: true
'''

EXAMPLES = r'''
- name: Create OEMDRV ISO with kickstart file
  create_ks_iso:
    src: /tmp/ks.cfg
    dest: /tmp/ks-iso.img
'''

RETURN = r'''
#
'''

import os

HAS_PYCDLIB = False
try:
    import pycdlib
    HAS_PYCDLIB = True
except ImportError:
    pass

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        src=dict(type='str', required=True),
        dest=dict(type='str', required=True)
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
    )

    # AnsibleModule object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    src = module.params['src']
    dest = module.params['dest']

    # checks
    if not os.path.exists(os.path.dirname(dest)):
        module.fail_json(msg='Directory "%s" does not exist' % os.path.dirname(dest), **result)

    if not os.path.exists(src):
        module.fail_json(msg='Kickstart file "%s" does not exist' % src, **result)

    # if check mode
    if module.check_mode:
        module.exit_json(**result)

    # iso creation
    iso = pycdlib.PyCdlib()
    iso.new(vol_ident="OEMDRV", rock_ridge="1.09")
    iso.add_file(src, "/KS.CFG;1", rr_name="ks.cfg")
    iso.write(dest)
    iso.close()
    result['changed'] = True

    # successful module execution
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
