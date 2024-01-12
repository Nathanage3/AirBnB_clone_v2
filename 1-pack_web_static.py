#!/usr/bin/python3
from fabric.api import *
import os
from datetime import datetime

env.hosts = ['localhost']

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder.

    All files in the folder web_static must be added to the final archive.
    All archives must be stored in the folder versions (your function should
    create this folder if it doesn’t exist).
    The name of the archive created must be web_static_<year><month><day>
    <hour><minute><second>.tgz.
    The function do_pack must return the archive path if the archive has been
    correctly generated. Otherwise, it should return None.
    """
    try:
        # Create a unique filename with a timestamp
        filepath = "versions/web_static_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".tgz"

        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Create the archive with the proper filename
        local("tar -zcvf {} web_static".format(filepath))

        # Print information about the created archive
        print("web_static packed: {} -> {}".format(filepath, os.path.getsize(filepath)))

        # Return the archive path
        return filepath
    except Exception as e:
        # Print any exception that occurs during the process
        print("Error during archive creation:", str(e))
        return None
