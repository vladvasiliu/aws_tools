# AWS Tools

This is a package of tools intended to help managing AWS resources.
This is intended for use with instances that are stateful, for example running legacy applications.

## Main goals:
* Manage automatic backups for long-running EC2 instances
* Manage a schedule to turn on/off long-running instances


## Running

### API Backend
`docker run aws-tools /venv/bin/daphne aws_backup_proj.asgi:application`

### Celery beat
`docker run aws-tools /venv/bin/celery -A aws_backup_proj beat`

### Celery worker
`docker run aws-tools /venv/bin/celery -A aws_backup_proj worker -l info`
