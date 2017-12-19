import sqlite3

class UxASDbHelper():

    def getDescriptorAndCounts(dbPath):
        """Returns the descriptor and counts for each type of message sent with UxAS.
        :param dbPath: A string representation of the fully qualified path to the sqlite database
        """
        query = "SELECT descriptor, count(*) AS count FROM msg GROUP BY descriptor"
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()

        # query for count of distinct message types
        c.execute(query)

        descriptorsAndCounts = dict(c.fetchall())
        conn.close()
        return descriptorsAndCounts


    def compareDescriptorAndCounts(truthDescriptorAndCounts, testDescriptorAndCounts, testName=""):
        """Compares the counts of each type of message in the test database to the truth database.
        :param truthDescriptorAndCounts: A dictionary of the messages sent where the key is the message descriptor and the value is the number of that type of message sent. This is the dbFile that the output from the most recent run is compared to.
        :param testDescriptorAndCounts:  A dictionary of the messages sent where the key is the message descriptor and the value is the number of that type of message sent. This is the dbFile that was output from the most recent run.
        """""
        #SHOULD THIS RETURN (BOOL - Whether or not the test passed, String - Description of the tests (failed message descripion and passed) )

        doMessageCountsMatch = True
        failedMessages = []
        for key in truthDescriptorAndCounts.keys():
            if (truthDescriptorAndCounts[key] != testDescriptorAndCounts.get(key, 0)):  # testDescriptorAndCounts.get used in case key doesnt exist in dict
                doMessageCountsMatch = False
                failedMessages.append("ERROR:\n\tThe count for the message \"%s\" does not match in the log files.\n\tExpected Count: %s\n\tActual Count: %s" % (
                    key, truthDescriptorAndCounts[key], testDescriptorAndCounts.get(key, 0)))

        if (doMessageCountsMatch):
            print(testName + "\nPASSED:\n\tAll message counts match in the log files\n")
            return (doMessageCountsMatch, "All message counts matched in the expected and actual message databases")
        else:
            print(testName + "\nFAILED:\n\tThe message counts do not match in the log files")
            failedMessagesString = str()

            # add messages to a failed messages string that will be passed as the test description
            for message in failedMessages:
                failedMessagesString = failedMessagesString + message + "\n"
            #can uncomment the following line for debugging, will be used in UI
            [ print(message) for message in failedMessages ] # print all the messages that failed
            return (doMessageCountsMatch, failedMessagesString)