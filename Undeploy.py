import time
import os
import boto.ec2
import paramiko
import commands
from boto.manage.cmdshell import sshclient_from_instance

def initializeConnection():
    """
    Establishing connection to EC2 using critical info provided in the credentials.csv
    :return: boto.ec2.connection
    """
    _aws_access_key_id = ''
    _aws_secret_access_key = ''
    try:
        with open(".aws/credentials.csv", 'r') as credentials:
            # Skip the first line
            credentials.readline()
            info = credentials.readline().split(',')
            _aws_access_key_id = info[2]
            _aws_secret_access_key = info[3]
        print "About to establish connection..."

    except IOError:
        print "Credentials not found. Exiting..."
        exit(-1)


    connection = boto.ec2.connect_to_region('us-east-1',
                                            aws_access_key_id=_aws_access_key_id,
                                            aws_secret_access_key=_aws_secret_access_key)

    print "Successfully connected to AWS"

    return connection

def terminate_all(conn):
    """
    Terminate instance on aws
    """
    reservations = conn.get_all_reservations()

    for reservation in reservations:
        instances = reservation.instances

        terminate_list = []

        for instance in instances:
            print "Running instance: %s" %  instance.id
            terminate_list.append(instance.id)

    print "Ready to terminate instances above"

    conn.terminate_instances(instance_ids = terminate_list)

    print "Finished termination"

    print "Exiting..."

if __name__ == "__main__":
    conn = initializeConnection()
    terminate_all(conn)
