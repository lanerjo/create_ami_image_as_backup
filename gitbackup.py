#!/usr/bin/python
# -*- coding: utf-8 -*-
#import our dependencies
import boto
from boto import ec2
from boto.ec2 import connection, connect_to_region
import sys
import os
import uuid


class AMICreation(object):

    def __init__(self):

        #os.environ['AWS_ACCESS_KEY_ID']
        #os.environ['AWS_SECRET_ACCESS_KEY']
        #os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

        self.connection = connect_to_region('us-west-2')

        self.instances = [i for r in
                          self.connection.get_all_instances() for i in
                          r.instances]
        self.action = 'failure'
        self.has_error = 'no'
        self.instance = None

    def create_image_id(
        self,
        instance=None,
        description=None,
        no_reboot=None,
        ami_name=None,
        ):

        image_id = instance.create_image(ami_name,
                description=description, no_reboot=no_reboot)

        if 'ami' in image_id:
            print image_id

            return 'success'
        else:

            return 'failure'

    def find_instance_id_and_create(
        self,
        servername,
        descritption,
        no_reboot,
        ):

        for i in self.instances:

            if 'Name' in i.tags:

                state = i.state

                name = i.tags['Name']

                instance_id = str(i.id)

                print name, state, instance_id

            if name.lower() == servername.lower():

                ami_name = servername.lower() + '-' \
                    + str(uuid.uuid4().fields[-1])[:5]

                status = self.create_image_id(i, str(descritption),
                        str(no_reboot), str(ami_name))

                if status == 'success':

                    self.has_error = 'no'

                    return self
                else:

                    self.has_error = 'yes'

                    return self
            else:

                self.has_error = 'no instances named %s' \
                    % servername.lower()


AMICreator = AMICreation()

AMICreator.find_instance_id_and_create('gitserver',
        'this is a git server backup base image', 'False')

if str(AMICreator.has_error) == 'no':
    print 'success'
else:
    print AMICreator.has_error
