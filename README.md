# Playbook for Rolling Restart MongoDB

## Overview
This playbook has ability to rolling restart MongoDB cluster, starting from hidden replicas, secondary replicas, and lastly to primary replica.

## What this repository covers
- [x] Rolling restart of MongoDB cluster.
- [x] Restarting from `hidden` replicas, proceed to `secondary` replicas, and lastly to `primary` replicas after delegating `primary` role.
- [x] Delegate the `primary` role only to `secondary` replicas which are not hidden, and prevent the current `primary` to get the same role during the process.
- [x] Does not continue to the next step if the current task fail

## Tools Used During Development
- Ansible [2.10.5](https://docs.ansible.com/ansible/latest/roadmap/COLLECTIONS_2_10.html)

## Makefile
To get this playbook running:
- Update your hosts file with mongodb ip addresses
- Adjust private_key_file location in `ansible/ansible.cfg`
- Execute `make run` from this project root directory.