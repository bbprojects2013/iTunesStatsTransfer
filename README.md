iTunesStatsTransfer
===================

Some small Scripts in Python to for transferring rating and playcount to another iTunes Library

Usage: 
1) Make a Backup of all your iTunes stuff - this software comes without any guaranty and you might loose everything!
2) Export the Media XML in the different Itunes libraries using Storage -> Mediatek -> Export Mediatek
3) Merge the different XML using: python mergeLibraries.py mediatek1.xml <mediatek2.xml> <mediatek_n.xml> destination_mediatek.xml
4) In the destination Library remove all Music from the library but DON'T DELETE the music from the hard disk
5) Go to Storage -> Mediatek -> import Mediatek and select the file destination_mediatek.xml
6) All your Music including the updated ratings and play counts should be back
7) Remove the duplicated play lists