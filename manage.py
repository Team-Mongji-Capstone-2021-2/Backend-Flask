# -*- coding: utf-8 -*-
import os
import sys
import boto3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import Config

try:
    activate_this = '{0}/venv/bin/activate_this.py'.format(Config.ROOT_DIR)
    with open(activate_this) as f:
        exec(f.read(), dict(__file__=activate_this))
except FileNotFoundError:
    activate_this = '{0}/venv/Scripts/activate_this.py'.format(Config.ROOT_DIR)
    with open(activate_this) as f:
        exec(f.read(), dict(__file__=activate_this))

from apps.controllers.router import app as application
from apps.common.commands.manager import manager

if __name__ == '__main__':

    os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-2' # 서울 리전
    os.environ['AWS_PROFILE'] = "Profile1"

    ec2 = boto3.resource('ec2')
    instance = ec2.Instance('i-021aecbd394c86f54')

    manager.run()
