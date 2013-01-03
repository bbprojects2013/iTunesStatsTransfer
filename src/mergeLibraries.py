#coding: latin-1

import sys
import shutil       #for copy
import xml.etree.ElementTree as ET

#This is a small program enabling to transfer the rating and the playcount of different iTunes to another one
#This Software is published under the GPL3 License. 
#Copyright 2013 Birk Bremer



 
class MusicDBclass(dict):
    def __init__(self):
        dict.__init__(self)
        
    def __normalize(self, string):
        '''
        Removes special characters, spaces and decapitalizes everything
        @param string: string to work on
        '''
        string = string.replace("Š","ae").replace("š","oe").replace("Ÿ","ue").replace("§","ss").replace("Ÿ","ue").replace("_","").replace(" ","_").replace("-","").replace("/","").replace("\\","").lower()
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
        
def UpdateTunesDB(sLibraryFile):
    global MusicDB
    #this function Modifies the iTunes Library
    
    print "Create a backup of %s (is now %s_backup)"%(sLibraryFile,sLibraryFile)
    shutil.copyfile(sLibraryFile, "%s_backup"%(sLibraryFile))
    
    print "Writing Library File %s"%(sLibraryFile)
    
    tree = ET.parse(sLibraryFile)
    root = tree.getroot()
    tracks = GetItunesTracks(tree)    
    
    for track in tracks:
        for idx, sTrackinfo in enumerate(track):
            #print sTrackinfo.tag, sTrackinfo.text
            
            if sTrackinfo.text == "Name":
                #print "found %s"%track[idx+1].text
                sSongName = track[idx+1].text
                
            if sTrackinfo.text == "Artist":
                #print "found %s"%track[idx+1].text
                sArtist = track[idx+1].text
                
            if sTrackinfo.text == "Rating":
#                print "Del tag: %s, Text: %s"%(sTrackinfo.tag, sTrackinfo.text)
                track.remove(sTrackinfo)
                track.remove(track[idx])
                #bDelnext = True
                
            
            if sTrackinfo.text == "Play Count":
 #               print "Del tag: %s, Text: %s"%(sTrackinfo.tag, sTrackinfo.text)
                track.remove(sTrackinfo)
                track.remove(track[idx])
    
        if MusicDB.GetValue(sArtist, sSongName) != (None, None):
            iCount, iRating = MusicDB.GetValue(sArtist, sSongName)
            print "Updating: %s / %s with Count: %s, Raing: %s"%(sArtist, sSongName, iCount, iRating)
            
                

                
                
    tree.write(r"./sample/testfile.xml")
                








def main():
    #just the main function
    if len(sys.argv) == 1: 
        sSourceFiles = [r"./sample/Mediathek.xml", r"./sample/Mediathek_dst.xml"]
        sDestinFile = r"./sample/Mediathek_dst.xml"
        
        print "Testmode: Using as Input: %s and output: %s"%(sSourceFiles, sDestinFile)
        
    for sSourcefile in sSourceFiles:
        #parse all the input Mediatheks
        ParseTunesXML(sSourcefile)
        
    UpdateTunesDB(sDestinFile)
        
        
    

if __name__ == "__main__":
    main()

#test