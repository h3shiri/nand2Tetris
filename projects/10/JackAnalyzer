#!/usr/bin/env python3

# out driver file
import JackParser
import os
import sys

sysInput = sys.argv[1]

def isDirectory():
    global sysInput
    isDir = os.path.isdir(sysInput)
    if isDir:
        if not sysInput.endswith('/'):
            sysInput = (sysInput + '/')
    return isDir


def listJackInDir():
    """
    function that get the list of Jack files(if its a directory)
    :param dir:
    :return:
    """
    global  sysInput
    files = []
    for file in os.listdir(sysInput):
        if file.endswith(".jack"):
            files.append(file)
    return files



def main():
    if isDirectory():
        #directoryName = sysInput.split("/")[-2]
        filesToParse = listJackInDir()
        for file in filesToParse:
            if not sysInput.endswith("/"):
                fileWithRelativePath = (sysInput + "/" + file)
            else:
                fileWithRelativePath = (sysInput + file)
            JackParser.parseOneFile(fileWithRelativePath)

    else:
        JackParser.parseOneFile(sysInput)

if __name__ == "__main__":
    main()