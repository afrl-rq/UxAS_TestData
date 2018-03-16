import sqlite3

class UxASDbHelper():

    def getDescriptorAndCounts(dbPath):
        """Returns the descriptor and counts for each type of message sent with UxAS.
        :param dbPath: A string representation of the fully qualified path to the sqlite database
        """""
        query = "SELECT descriptor, count(*) AS count FROM msg GROUP BY descriptor"
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()

        # query for count of distinct message types
        c.execute(query)

        descriptorsAndCounts = dict(c.fetchall())
        conn.close()
        return descriptorsAndCounts

    def compareDescriptorAndCountsOneWay(descriptorAndCounts1, descriptorAndCounts2 ,blacklistItems=[]):

        unmatchedMessageKeys = []
        skippedMessageKeys = []
        for key in descriptorAndCounts1.keys():
            # Check all messages in the blacklist here:
            continueCheck = False

            # Loop to get all messages that are skipped
            for item in blacklistItems:
                if (item.lower() in key.lower()):
                    continueCheck = True  # the message will not be compared in databases
                    skippedMessageKeys.append(key)

            if (continueCheck):  # if the message type is skipped, then continue and do not compare the counts
                continue

            if (descriptorAndCounts1[key] != descriptorAndCounts2.get(key, 0)):  # Check if truth and test message counts match
                unmatchedMessageKeys.append(key)

        skippedAndUnmatchedMessageKeyTuple = (skippedMessageKeys, unmatchedMessageKeys)
        return skippedAndUnmatchedMessageKeyTuple



    def compareDescriptorAndCounts(truthDescriptorAndCounts, testDescriptorAndCounts, testName="", blacklistItems = []):
        """Compares the counts of each type of message in the test database to the truth database.
        :param truthDescriptorAndCounts: A dictionary of the messages sent where the key is the message descriptor and the value is the number of that type of message sent. This is the dbFile that the output from the most recent run is compared to.
        :param testDescriptorAndCounts:  A dictionary of the messages sent where the key is the message descriptor and the value is the number of that type of message sent. This is the dbFile that was output from the most recent run.
        """""
        doMessageCountsMatch = True
        warningMessageString = str()
        (skippedMessageKeys1, unmatchedMessageKeys1) = UxASDbHelper.compareDescriptorAndCountsOneWay(truthDescriptorAndCounts, testDescriptorAndCounts, blacklistItems)
        (skippedMessageKeys2, unmatchedMessageKeys2) = UxASDbHelper.compareDescriptorAndCountsOneWay(testDescriptorAndCounts, truthDescriptorAndCounts, blacklistItems)
        skippedMessageKeys = set(skippedMessageKeys1 + skippedMessageKeys2)
        unmatchedMessageKeys = set(unmatchedMessageKeys1 + unmatchedMessageKeys2)

        if(skippedMessageKeys):
            skippedMessages = ["Not comparing the \"%s\" messages" % key for key in skippedMessageKeys]
            warningMessageString = "\tWARNING:\n\t\t" + "\n\t\t".join(skippedMessages)
        if(unmatchedMessageKeys):
            doMessageCountsMatch = False
            unmatchedMessages= ["\n\tThe count for the message \"%s\" does not match in the log files.\n\tExpected Count: %s\n\tActual Count: %s" % (key, truthDescriptorAndCounts.get(key, 0), testDescriptorAndCounts.get(key, 0)) for key in unmatchedMessageKeys]
            print("%s\nFAILED\n\tThe message counts do not match in the log files" % testName)
            [print("\tWARNING: %s messages" % message) for message in skippedMessages]
            [print("\tERROR: " + message) for message in unmatchedMessages]
            errorMessageString = "\n\tERROR:\n\t" + "\n\t\t".join(unmatchedMessages)
            descriptionMessage = warningMessageString + errorMessageString
        else:
            print("%s\nPASSED:\n\tAll message counts match in the log files\n" % testName)
            descriptionMessage = warningMessageString
            print(descriptionMessage)
            descriptionMessage = warningMessageString

        return (doMessageCountsMatch, descriptionMessage)