Nansible README
===============

Nate's Ansible deployment script with additional source compilation tools.

USAGE: nan action (other-flags)

Where action is one of:

  - compile:      Compile source tree (but don't call ansible)
                  Use --keep_compiled to see compiled tree
  - test_remote:  Run deployment in test mode to remote host
  - test_local:   Run deployment in test mode on local host
  - remote:       Compile, then deploy configuration to remote host
  - local:        Compile, then deploy configuration to local host
  - debug_parse:  Print listing of source files and how they are typed

This tool provides the following features on top of ansible:

  - The collection of roles into folders.
    See Nansible README

  - Automatic file renaming:
      role/handlers.yml -> role/handlers/main.yml
      role/tasks.yml -> role/tasks/main.yml
      role/vars.yml -> role/vars/main.yml
      role/meta.yml -> role/meta/main.yml

  - Execution of autogen scripts

nansible is expected to run from a folder with the structure of:

    source/                    -->   compiled/
     |--roles/                        |--roles/
     |   `--standard_roles/...        |   |--standard_roles/...
     |--projects/                     |   |--project_a__proj_role_a/
     |   `--project_a/                |   `--project_a__proj_role_v/
     |       |--proj_role_a/...       `--main.yml
     |       |--proj_role_b/
     |       |   `--tasks/
     |       |       |--enabled.yml
     |       |       |--disabled.yml
     |       |       `--purged.yml
     |       `--project.yml
     |--main.yml
     `--hosts

*projects is still under review.  Not sure if I need this feature*