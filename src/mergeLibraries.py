

import sys

#This is a small program enabling to transfer the rating and the playcount of different iTunes to another one
#This Software is published under the GPL3 License. 
#Copyright 2013 Birk Bremer
 










def main():
    #just the main function
    if len(sys.argv) == 1: 
        sSourceFiles = [r"./sample/Mediathek.xml"]
        sDestinFile = r"./sample/Mediathek_dst.xml"
        
        print "Testmode: Using as Input: %s and output: %s"%(sSourceFiles, sDestinFile)
        
    for sSourcefile in sSourceFiles:
        pass
        #parse all the input Mediatheks and transfer the read data in our librarya
        
    








if __name__ == "__main__":
    main()

#test