#coding: utf-8

#This is a small program enabling to transfer the rating and the playcount of different iTunes to another one
#This Software is published under the GPL3 License and comes "as it is" without any warranty
#Copyright by Birk Bremer, 2013



import sys
import os
import shutil       #for copy
import xml.etree.ElementTree as ET

 
class MusicDBclass(dict):
    def __init__(self):
        dict.__init__(self)
        
    def __normalize(self, string):
        '''
        Removes special characters, spaces and decapitalizes everything
        @param string: string to work on
        '''
        string = string.replace(u"ä","ae").replace(u"ö","oe").replace(u"ü","ue").replace(u"ß","ss").replace("_","").replace(" ","_").replace("-","").replace("/","").replace("\\","").lower()
        return string
        
    def __CalcHash(self, sArtist, sSongName):
        '''
        Creates the pseudo Hash
        @param sArtist: Artist as a string
        @param sSongName: Song Name as a string
        '''
        
        sArtist_normalized = self.__normalize(sArtist)
        sSongName_normalized = self.__normalize(sSongName)
        
        return "%s%s"%(sArtist_normalized,sSongName_normalized)
    
    def GetValue(self, sArtist, sSongName):
        sHash = self.__CalcHash(sArtist, sSongName)
        
        if not self.has_key(sHash):
            return None, None
        else:
            return self[sHash]["iCount"], self[sHash]["iRating"] 
        
    
    def add(self, sArtist, sSongName, iCount, iRating):
        '''
        Create a new element in the DB class
        @param sArtist: Artist as a string
        @param sSongName: Song Name as a string
        @param iCount: count as a integer
        @param iRating: Rating as a integer (Itunes only 0 - 100)
        '''
    
        #nothing to do        
        if (iCount == None) and (iRating == None):
            return
        
        sHash = self.__CalcHash(sArtist, sSongName)

        if not self.has_key(sHash):
            self[sHash] = { "iCount": 0,
                           "iRating": 0}
        
        if iCount != None:
            self[sHash]["iCount"] = self[sHash]["iCount"] + iCount
        
        #take always the best rating
        if iRating != None:
            if self[sHash]["iRating"] < iRating:
                self[sHash]["iRating"] = iRating
   
MusicDB = MusicDBclass()         
        

def GetItunesTracks(tree):
    '''
    Extracts all the iTunes Tracks elements and returns a list with them (wired xml usage!)
    @param tree: the xml tree element
    '''
    root = tree.getroot()
    
    tracks = []
    #lets find the tracks root
    for idx, child in enumerate(root[0]):
        if child.text == "Tracks":
            #print child.text, child.tag, child.attrib, "\n"
            #print "Found Tracks root"
            tracks_root = root[0][idx+1]
            
            #extract all track elements
            for track in tracks_root:
                if track.tag == "dict":
                    tracks.append(track)
                #print track.tag, track.text
            break
    return tracks

def ParseTunesXML(sLibraryFile):
    global MusicDB
    #this function does the actual XML Parsing and creates the LibraryObjects"
    print "Reading Library File %s"%(sLibraryFile)
    #fh_LibraryFile = open(sLibraryFile,'r')
    #xml_data = fh_LibraryFile.read()
    #fh_LibraryFile.close()
    
    
    tree = ET.parse(sLibraryFile)
    tracks = GetItunesTracks(tree)
    
    for track in tracks:
        #parse all the tracks element and transfer the information to the  summary
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
        #print "Song: %s by %s was played %s and rated %s"%(sSongName, sArtist, iCount, iRating)
        MusicDB.add(sArtist, sSongName, iCount, iRating)
    #print MusicDB
    
def WriteItunesXML(XMLobj, FilePathName):
    '''
    Writes the given XML object to a iTunes compatible file
    @param XMLobj: The xml object in form of a element tree (root object)
    '''
    out = '<?xml version="1.0" encoding="UTF-8"?>\n'
    out += '<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
    out += ET.tostring(XMLobj)
    
    FilePathName = os.path.abspath(FilePathName)
    
    fh = open(FilePathName,"w")
    print "Writing file %s"%(FilePathName)
    fh.write(out)
    fh.close()
        
def UpdateTunesDB(sDestinFile):
    global MusicDB
    #this function Modifies the iTunes Library
    
    print "Create a backup of %s (is now %s.backup)"%(sDestinFile,sDestinFile)
    shutil.copyfile(sDestinFile, "%s.backup"%(sDestinFile))
    
    print "Parsing File %s for updates"%(sDestinFile)
    
    tree = ET.parse(sDestinFile)
    root = tree.getroot()
    tracks = GetItunesTracks(tree)    
    
    for track in tracks:
        #Search for the reqired Elements
        for idx, sTrackinfo in enumerate(track):
            #print sTrackinfo.tag, sTrackinfo.text
            
            if sTrackinfo.text == "Name":
                #print "found %s"%track[idx+1].text
                sSongName = track[idx+1].text
                
            if sTrackinfo.text == "Artist":
                #print "found %s"%track[idx+1].text
                sArtist = track[idx+1].text
                
            #remove a existing Rating
            if sTrackinfo.text == "Rating":
#                print "Del tag: %s, Text: %s"%(sTrackinfo.tag, sTrackinfo.text)
                track.remove(sTrackinfo)
                track.remove(track[idx])
                #bDelnext = True
                
            #remove a existing Playcount    
            if sTrackinfo.text == "Play Count":
 #               print "Del tag: %s, Text: %s"%(sTrackinfo.tag, sTrackinfo.text)
                track.remove(sTrackinfo)
                track.remove(track[idx])
    
        #if we have a updated rating put it to the x,l structure
        if MusicDB.GetValue(sArtist, sSongName) != (None, None):
            iCount, iRating = MusicDB.GetValue(sArtist, sSongName)
            print "Updating: %s / %s with Count: %s, Raing: %s"%(sArtist, sSongName, iCount, iRating)
            
            if iCount > 0:
                key_count = ET.SubElement(track, "key")
                key_count.text = "Play Count"
                num_count = ET.SubElement(track, "integer")
                num_count.text = "%s"%(iCount)
                
            if iRating > 0:
                key_rating = ET.SubElement(track, "key")
                key_rating.text = "Rating"
                num_rating = ET.SubElement(track, "integer")
                num_rating.text = "%s"%(iRating)
                
    WriteItunesXML(root, sDestinFile)


def main(sSourceFiles, sDestinFile):
    
    for sSourcefile in sSourceFiles:
        #parse all the input Mediatheks
        sSourcefile = os.path.abspath(sSourcefile)
        if not os.path.exists(sSourcefile):
            print "File %s doesn't exist --> Exit"
            sys.exit(1)
        ParseTunesXML(sSourcefile)
    
    sDestinFile = os.path.abspath(sDestinFile)
    UpdateTunesDB(sDestinFile)
    sys.exit(0)


if __name__ == "__main__":
    #called in case this file is called directly
    
    #test if we need to print the help
    if (len(sys.argv) == 1) or (sys.argv[1] == "-h") or (sys.argv[1] == "--help"): 
        print "Usage: python %s mediatek1.xml <mediatek2.xml> <mediatek_n.xml> destination_mediatek.xml"%(os.path.split(sys.argv[0])[1])
        print "\n\nLong explanation"
        print "1) Make a Backup of all your iTunes stuff - this software comes without any guaranty and you might loose everything!"
        print "2) Export the Media XML in the different Itunes libraries using Storage -> Mediatek -> Export Mediatek"
        print "3) Merge the different XML using: python %s mediatek1.xml <mediatek2.xml> <mediatek_n.xml> destination_mediatek.xml"%(os.path.split(sys.argv[0])[1])
        print "4) In the destination Library remove all Music from the library but DON'T DELETE the music from the hard disk"
        print "5) Go to Storage -> Mediatek -> import Mediatek and select the file destination_mediatek.xml"
        print "6) All your Music including the updated ratings and play counts should be back"
        print "7) Remove the duplicated play lists"
        sys.exit(0)
        
    if sys.argv[1] == "-t":
        sSourceFiles = [r"./sample/Mediathek.xml", r"./sample/Mediathek_dst.xml"]
        sDestinFile = r"./sample/testfile.xml"
        print "Testmode: Using as Input: %s and output: %s"%(sSourceFiles, sDestinFile)
        main(sSourceFiles, sDestinFile)
        sys.exit(0)
        
    
    sSourceFiles = (sys.argv[1:])
    sDestinFile = sys.argv[-1] 
    
    main(sSourceFiles, sDestinFile)