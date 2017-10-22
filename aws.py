import boto.ec2
import os
import time

SELECTED_AMI_IMAGE = 'ami-8caa1ce4'
SELECTED_INSTANCE_TYPE = 't1.micro'
KEY_NAME = 'NewInstance'


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

    except IOError:
        assert "Credentials not found. Exiting..."

    connection = boto.ec2.connect_to_region('us-east-1',
                                            aws_access_key_id=_aws_access_key_id,
                                            aws_secret_access_key=_aws_secret_access_key)

    return connection


def processAWS():
    connection = initializeConnection()

    # Creating a key pair on the connection
    try:
        newKeyPair = connection.create_key_pair(KEY_NAME)

    except Exception as error:
        print "Possibly due to the KeyPair exists already\n" \
              "Using the Exists KeyPair.. "

    else:
        if os.path.exists(os.getcwd()+'/KeyPairs/'+KEY_NAME+'.pem'):
            os.remove(os.getcwd()+'/KeyPairs/'+KEY_NAME+'.pem')
        newKeyPair.save(os.getcwd()+'/KeyPairs')

    try:
        # Creating a security group
        webSec = connection.create_security_group('csc326-group28', 'Our local server group')
        # Authorizing server ping
        webSec.authorize('ICMP', -1, -1, '0.0.0.0/0')
        # Authorizing SSH
        webSec.authorize('TCP' , 22, 22, '0.0.0.0/0')
        # Authorizing HTTP
        webSec.authorize('TCP' , 80, 80, '0.0.0.0/0')

    except:
        print "Security group 'csc326-group28' exists\n" \
              "Using the exists security group 'csc326-group28'"
        SecGroups = connection.get_all_security_groups(groupnames=['csc326-group28'])
        webSec = SecGroups[0]

    reservation = connection.run_instances(
        SELECTED_AMI_IMAGE,
        key_name=KEY_NAME,
        instance_type=SELECTED_INSTANCE_TYPE,
        security_groups=[webSec]
    )

    instList = reservation.instances

    print "Booting up instance..."

    associatedInstIds = [inst.id for inst in instList]

    instanceBooted = 0

    while instanceBooted < len(instList) :
        # Update instance status
        instList = connection.get_all_instances(instance_ids=associatedInstIds)[0].instances

        # Terminal informing
        for eachInst, order in zip(instList, range(len(instList))):
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print "\tInstance %d status: %s" % (order, eachInst.state)

            # If one instance is running, record
            if eachInst.state == 'running':
                instanceBooted += 1

        # Refreshing rate is at 5 seconds
        time.sleep(5)

    print "Instance finished booting up"

    # Assuming create only one instance
    # Binding static IP
    staticIP = None

    if not connection.get_all_addresses():
        staticIP = connection.get_all_addresses()[0]
    else:
        staticIP = connection.allocate_address()

    for eachInst, order in zip(instList, range(len(instList))):
        print "Instance %d at IP: %s" % (order+1, eachInst.ip_address)

        # Binding a static IP address to instances
        staticIP.associate(instance_id=eachInst.id,allow_reassociation=True)

        print "Instance %d at static IP: %s" % (order+1, staticIP.public_ip)

if __name__ == "__main__":
    processAWS()