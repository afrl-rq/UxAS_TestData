import os
import platform

class FileHelper():


    def getMostRecentFileInPathWithExtension(directory, extension):
        """Returns the most recently created file in a directory with the specified extension
         :param directory: The string representation of a directory to be searched.
         :param extension: The string representation of a file extension searched for in the directory
         """
        files = [file for file in os.listdir(directory) if file.endswith(extension)]
        if (files == []):
            return (False, "No such file exists")
        fileDict = {}
        for file in files:
            filePath = "%s\\%s" % (directory, file)
            fileDict[FileHelper.getCreationDate(filePath)] = filePath

        return (True, fileDict[max(fileDict.keys())])

    def getCreationDate(pathToFile):
        """Returns the date a file was created
        :param pathToFile: A string representation of the fully qualified path to a file
        """
        if platform.system() == 'Windows':
            return os.path.getctime(pathToFile)
        else:
            stat = os.stat(pathToFile)
            try:
                return stat.st_birthtime
            except AttributeError:
                return stat.st_mtime

    def searchForSubFolderInDir(directory, subFolder, isSubFolderHint = False):
        """Searches a directory for a sub folder. Returns a tuple ([BOOL, TRUE IF FOLDER IS FOUND, OTHERWISE FALSE],[STRING, REPRESENTING SUBFOLDER'S PATH])
        :param directory: The string representation of the directory to be searched.
        :param subFolder: The string representation of the sub folder of interest. This can either be the full name of the subfolder the beginning of the subfolder name
        :param isSubFolderHint: A boolean that identifies whether the subFolder represents the beginning of the folder name or not. If true, then the subFolder parameter is a hint that represents the beginning of the folder name. If false, then it represents the full subFolder name
        """
        # check if subfolder exists in specified directory
        if (isSubFolderHint == False and os.path.isdir(directory + subFolder)):
            return (True, directory + subFolder)
        # if isSubFolderHint is true then the subfolder has to begin with subFolder name

        if (isSubFolderHint == True):
            for root, dirs, files in os.walk(directory):
                for folder in dirs:
                    if folder.startswith(subFolder):
                        return (True, directory + "\\" + folder)

        return (False, "SubFolder does not exist")

    def searchForFileInDir(directory, fileHint, isFileHint = False):
        """Searches a directory for a file. Returns a tuple ([BOOL, TRUE IF FILE IS FOUND, OTHERWISE FALSE],[STRING, REPRESENTING FILES'S PATH])
        :param directory: The string representation of the directory to be searched.
        :param subFolder: The string representation of the file of interest. This can either be the full name of the file the beginning of the file's name
        :param isFileHint: A boolean that identifies whether the file represents the beginning of the file's name or not. If true, then the file parameter is a hint that represents the beginning of the file's name. If false, then it represents the full file's name
        """
        # check if file exists in the specified directory
        if (isFileHint == False and os.path.isdir(directory + file)):
            return (True, directory + file)
        # if isSubFolderHint is true then the subfolder has to begin with subFolder name

        if (isFileHint == True):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.startswith(fileHint):
                        return (True, directory + "\\" + file)

        return (False, "File does not exist")
