# JIRA integration pack

This pack consists of a sample JIRA sensor and a JIRA action.

## Installation

You will need to have `gcc` installed on your system. For Ubuntu systems, run `sudo apt-get install gcc`. For Redhat/CentOS
systems, run `sudo yum install gcc libffi-devel python-devel openssl-devel`. To build the python cryptography dependency (part of the following `st2 pack install` command) 2GB of RAM is recommended. In some cases adding a swap file may eliminate strange gcc compiler errors.

Then install this pack with: `st2 pack install jira-basic`

## Configuration

Copy the example configuration in [jira-basic.yaml.example](./jira-basic.yaml.example)
to `/opt/stackstorm/configs/jira-basic.yaml` and edit as required.

* ``url`` - URL of the JIRA instance (e.g. ``https://myproject.atlassian.net``)
* ``username`` - Username.
* ``password`` - Password.
* ``poll_interval`` - Polling interval - default 30s
* ``project`` - Key of the project which will be used as a default with some of the actions which
  don't require or allow you to specify a project (e.g. ``STORM``).

To get these OAuth credentials, take a look at OAuth section below.

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.


## Sensors

### JiraSensor

The sensor monitors for new tickets and sends a trigger into the system whenever there is a new ticket.

## Actions

* ``create_issue`` - Action which creates a new JIRA issue.
* ``get_issue`` - Action which retrieves details for a particular issue.
