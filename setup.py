import commands
import os

def aws_componentInstall():
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

def aws_moduleInstall():
    """ Installing essential module for website operating """
    module_to_be_install = []

    print "Prepare to install essential modules"

    moduleInstall = ["sudo pip install boto",
                     "sudo pip install beaker",
                     "sudo pip install bottle",
                     "sudo pip install oauth2client",
                     "sudo pip install autocorrect",
                     "sudo pip install --upgrade google-api-python-client",
                     "sudo pip install requests",
                     "sudo pip install httplib2"]

    for eachModule in moduleInstall:

        print "...Installing " + eachModule.split()[-1]

        result = commands.getstatusoutput(eachModule)

        if result[0] == 0:
            print "\nSuccessfully installed %s" % eachModule.split()[-1]
        else:
            print "\nFailed installing %s" % eachModule.split()[-1]
            print result[1]
            print "Terminating..."
            raw_input("Press key to exit.......")
            exit(-1)

    print "Finished installing modules"

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
        result = commands.getstatusoutput(eachCommand)

    if result[0] == 0:
        print "%s: In progress..." % procName
    else:
        print "%s: Encounters a unsolvable problem:" % procName
        print result[1]
        return -1

    return 0

if __name__ == "__main__" :
    aws_componentInstall()
    aws_moduleInstall()
    aws_mongodbDeployment()    