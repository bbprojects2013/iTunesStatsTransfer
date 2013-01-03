

import sys

import xml.etree.ElementTree as ET

#This is a small program enabling to transfer the rating and the playcount of different iTunes to another one
#This Software is published under the GPL3 License. 
#Copyright 2013 Birk Bremer
 
 



def ParseTunesXML(sLibraryFile):
    #this function does the actual XML Parsing and creates the LibraryObjects
    print "Parsing Library File %s"%(sLibraryFile)
    #fh_LibraryFile = open(sLibraryFile,'r')
    #xml_data = fh_LibraryFile.read()
    #fh_LibraryFile.close()
    
    
    tree = ET.parse(sLibraryFile)
    root = tree.getroot()
    
    tracks = []
    #lets find the tracks root
    for idx, child in enumerate(root[0]):
        if child.text == "Tracks":
            #print child.text, child.tag, child.attrib, "\n"
            print "Found Tracks root"
            tracks_root = root[0][idx+1]
            
            #extract all track elements
            for track in tracks_root:
                if track.tag == "dict":
                    tracks.append(track)
                #print track.tag, track.text
            break
    
    for track in tracks:
        sArtist= ""
        sSongName= ""
        iCount = None
        iRating = None 
        for idx, sTrackinfo in enumerate(track):
            #print sTrackinfo.tag, sTrackinfo.text
            
            if sTrackinfo.text == "Name":
                #print "found %s"%track[idx+1].text
                sSongName = track[idx+1].text
                
            if sTrackinfo.text == "Artist":
                #print "found %s"%track[idx+1].text
                sArtist = track[idx+1].text
                
            if sTrackinfo.text == "Rating":
                #print "found %s"%track[idx+1].text
                iRating = int(track[idx+1].text)
            
            if sTrackinfo.text == "Play Count":
                #print "found %s"%track[idx+1].text
                iCount = int(track[idx+1].text)
        print "Song: %s by %s was played %s and rated %s"%(sSongName, sArtist, iCount, iRating)
        
    #print tracks
    
    #print tracks.text, tracks.tag, tracks.attrib, "\n"
        #print child.text, child.tag, child.attrib, "\n"
        
    #print root.find("key").text(9)
    #for elem in root[0][0]:
    #    print elem
    #print root.attrib
   
    
    #dom = parseString(xml_data)
    #tracks = dom.getElementsByTagName("key")
    #for elem in tracks:
    #    if elem.toxml() == "<key>Tracks</key>" :
    #        tracks = elem
    #        break
   # 
    #print tracks
    #print tracks.childNodes    







def main():
    #just the main function
    if len(sys.argv) == 1: 
        sSourceFiles = [r"./sample/Mediathek.xml"]
        sDestinFile = r"./sample/Mediathek_dst.xml"
        
        print "Testmode: Using as Input: %s and output: %s"%(sSourceFiles, sDestinFile)
        
    for sSourcefile in sSourceFiles:
        #parse all the input Mediatheks
        ParseTunesXML(sSourcefile)
        
        
    

if __name__ == "__main__":
    main()

#test