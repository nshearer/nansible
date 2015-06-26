Nansible README
===============

Nate's Ansible deployment script with additional source compilation tools.

Projects
--------

Project folders are in the roles folder, but end in .proj
and have a project.yml file.  Projects contain groups of
role folders that are related, and specical tasks files:

 - my.proj/role/tasks/enabled.yml
 - my.proj/role/tasks/disabled.yml
 - my.proj/role/tasks/purged.yml

Each of which is translated to my__role/tasks/main.yml
depending on if the project is designated as enabled,
disabled, or purged.