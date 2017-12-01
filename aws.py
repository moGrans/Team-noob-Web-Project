import boto.ec2
from boto.manage.cmdshell import sshclient_from_instance
import os
import time

GIT_CLONE = "https://github.com/moGrans/Team-noob-Web-Project.git"

SELECTED_AMI_IMAGE = 'ami-8caa1ce4'
SELECTED_INSTANCE_TYPE = 't1.micro'
KEY_NAME = 'ATESTINSTANCE'

# Connection for accessing AWS terminal
SSH_CLIENT = None
KEY_DIR = None


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
    else:
        print "Unknown error. Exiting..."
        exit(-1)

    connection = boto.ec2.connect_to_region('us-east-1',
                                            aws_access_key_id=_aws_access_key_id,
                                            aws_secret_access_key=_aws_secret_access_key)

    return connection


def processAWS():
    connection = initializeConnection()

    # Creating a key pair on the connection
    try:
        print "Creating Key Pair: " + KEY_NAME
        newKeyPair = connection.create_key_pair(KEY_NAME)

    except Exception as error:
        print "Possibly due to the KeyPair exists already\n" \
              "deleting the Exists KeyPair.. "
        connection.delete_key_pair(key_name=KEY_NAME)
        newKeyPair = connection.create_key_pair(KEY_NAME)

    if os.path.exists(os.getcwd() + '/KeyPairs/' + KEY_NAME + '.pem'):
        os.remove(os.getcwd() + '/KeyPairs/' + KEY_NAME + '.pem')
    newKeyPair.save(os.getcwd() + '/KeyPairs')

    try:
        # Creating a security group
        webSec = connection.create_security_group('csc326-group28', 'Our local server group')
        # Authorizing server ping
        webSec.authorize('ICMP', -1, -1, '0.0.0.0/0')
        # Authorizing SSH
        webSec.authorize('TCP', 22, 22, '0.0.0.0/0')
        # Authorizing HTTP
        webSec.authorize('TCP', 80, 80, '0.0.0.0/0')

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

    while instanceBooted < len(instList):
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

    print "Connecting to instance terminal..."

    global SSH_CLIENT, KEY_DIR
    KEY_DIR = os.getcwd() + '/KeyPairs' + KEY_NAME + '.pem'

    print "Waiting for instance ready check"

    time.sleep(30)

    print "Connecting..."

    try:
        SSH_CLIENT = sshclient_from_instance(instList[0], KEY_DIR, user_name='ubuntu')
    except Exception as error:
        print error
        print "Setup encounters a unsolvable problem and must be closed..."
        exit(-1)

    print "Terminal connection established"

    print "--- No need to allocate elastic IP, skip..."

    # Assuming create only one instance
    # Binding static IP
    # staticIP = None

    # if not connection.get_all_addresses():
    #     staticIP = connection.get_all_addresses()[0]
    # else:
    # staticIP = connection.allocate_address()

    for eachInst, order in zip(instList, range(len(instList))):
        print "Instance %d booted at IP: %s, DNS: %s" % (order, eachInst.ip_address, eachInst.dns)

        # Binding a static IP address to instances
        # staticIP.associate(instance_id=eachInst.id, allow_reassociation=True)

        # print "Instance %d at static IP: %s" % (order + 1, staticIP.public_ip)

    print "Proceed to system setup"


def aws_moduleInstall():
    """ Installing essential module for website operating """
    module_to_be_install = []

    print "Prepare to install essential modules"

    moduleInstall = ["sudo pip install beaker",
                     "sudo pip install bottle",
                     "sudo pip install oauth2client",
                     "sudo pip install autocorrect",
                     "sudo pip install --upgrade google-api-python-client",
                     "sudo pip install requests",
                     "sudo pip install httplib2"]

    for eachModule in moduleInstall:

        print "...Installing " + eachModule.split()[-1]

        status, stdout, stderr = SSH_CLIENT.run(eachModule)

        if status == 0:
            print "\nSuccessfully installed %s" % eachModule.split()[-1]
        else:
            print "\nFailed installing %s" % eachModule.split()[-1]
            print stderr
            print "Terminating..."
            raw_input("Press key to exit.......")
            exit(-1)

    print "Finished installing modules"


def aws_componentInstall(connection):
    print "Prepare to install system component on aws"

    componentsInstall = ["apt-get update", "apt-get -y install python-pip"]

    _run_command_set(componentsInstall, "Python-setup")

    print "Installing mongoDB..."

    mongoDBInstall = ["sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6",
                      'echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list',
                      "sudo apt-get update",
                      "sudo apt-get install -y mongodb-org"]

    result = _run_command_set(mongoDBInstall, "Mongo")

    if not result:
        print "Terminating..."
        raw_input("Press key to exit.......")
        exit(-1)

    print "Finished system component"


def aws_gitClone():
    print "Prepare to clone from Git"

    gitInstall = ["sudo apt-get install git -y",
                  "git clone " + GIT_CLONE,]

    result = _run_command_set(gitInstall, "Git")

    if not result:
        print "Terminating..."
        raw_input("Press key to exit.......")
        exit(-1)

def aws_mongodbDeployment():
    print "Prepre to deploy mongoDB"
    print "\nMongoDB: Starting up"

    mongoDeploy = ["sudo service mongod start",
                   "mongorestore /home/ubuntu/Team-noob-Web-Project/dump"]

    result = _run_command_set(mongoDeploy,'MongoDB')

    if not result:
        print "Terminating..."
        raw_input("Press key to exit.......")
        exit(-1)

def _run_command_set(commandSet, procName):
    for eachCommand in commandSet:
        status, stdout, stderr = SSH_CLIENT.run(eachCommand)

        if status == 0:
            print "%s: In progress..." % procName
        else:
            print "%s: Encounters a unsolvable problem:" % procName
            print stderr
            return -1

    return 0
if __name__ == "__main__":
    processAWS()
    aws_componentInstall()
    aws_moduleInstall()
    aws_gitClone()
    aws_mongodbDeployment()
    exit(0)