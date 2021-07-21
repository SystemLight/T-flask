#!/bin/bash

uwsgi --stop ./uwsgi.pid
uwsgi --ini ./uwsgi.ini
