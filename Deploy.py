import time
import os
import boto.ec2
import paramiko
import commands
from boto.manage.cmdshell import sshclient_from_instance


GIT_CLONE = "https://github.com/moGrans/Team-noob-Web-Project.git"

SELECTED_AMI_IMAGE = 'ami-8caa1ce4'
SELECTED_INSTANCE_TYPE = 't1.micro'
KEY_NAME = 'ATESTINSTANCE666'

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


    connection = boto.ec2.connect_to_region('us-east-1',
                                            aws_access_key_id=_aws_access_key_id,
                                            aws_secret_access_key=_aws_secret_access_key)

    print "Successfully connected to AWS"

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

    if not os.path.exists(os.getcwd() + '/KeyPairs'):
        commands.getstatusoutput('mkdir ' + os.getcwd()+ '/KeyPairs')

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
<<<<<<< HEAD
    KEY_DIR = os.getcwd() + '/KeyPairs/' + KEY_NAME + '.pem'
=======
    KEY_DIR = os.getcwd() + '\\KeyPairs\\' + KEY_NAME + '.pem'
>>>>>>> 68cc0e156654fe02fd90992965aa87ae53280b60

    print "Waiting for instance ready check"

    print "Connecting..."


    for eachInst, order in zip(instList, range(len(instList))):
        print "Instance %d booted at IP: %s" % (order, eachInst.ip_address)


    print "Proceed to system setup"

    global SSH_CLIENT
    SSH_CLIENT = paramiko.SSHClient()
    SSH_CLIENT.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    time.sleep(20)

    while True:
        try:
            SSH_CLIENT.connect(instList[0].ip_address, username="ubuntu", key_filename=KEY_DIR)
            break
        except Exception as error:
            print error
            print "...Attempting to reconnect"
            time.sleep(3)

    print "Terminal connection established"

    print "--- No need to allocate elastic IP, skip..."

    print "Installing git components for repository transfer"

    client_exec("sudo apt-get install git -y", "Git")
    
    print "Downloading from Git repository..."

    clone_command = "git clone " + GIT_CLONE
    
    client_exec(clone_command, "Git clone")
    
    print "Executing deployment wizard..."

    client_exec("sudo python ~/Team-noob-Web-Project/setup.py", "Deployment wizard")

    print "Ready to boot up the website..."

    print "Not there yet, so far so good"


def client_exec(command, progName):
    stdin, stdout, stderr = SSH_CLIENT.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()

    if exit_status == 0:
        print "%s ---> Successful" % progName
    else:
        print "%s **** Failed" % progName
        print stderr
        print "Deployment encounters an unsolvable problem and has to quit"
        raw_input("Press any key to exit...")
        exit(-1)

if __name__ == "__main__":
    processAWS()
    # aws_componentInstall()
    # aws_moduleInstall()
    # aws_gitClone()
    # aws_mongodbDeployment()
    exit(0)