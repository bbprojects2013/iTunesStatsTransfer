iTunesStatsTransfer
===================

A small Script in Python to transfer ratings and playcounts to another iTunes Library (Merge this information from
one or several libraries to one destination library)

Usage:<br>
1) Make a Backup of all your iTunes stuff - this software comes without any guaranty and you might loose everything!<br>
2) Export the Media XML in the different Itunes libraries using Storage -> Mediatek -> Export Mediatek<br>
3) Merge the different XML using: python mergeLibraries.py mediatek1.xml <mediatek2.xml> <mediatek_n.xml> destination_mediatek.xml<br>
4) In the destination Library remove all Music from the library but DON'T DELETE the music from the hard disk<br>
5) Go to Storage -> Mediatek -> import Mediatek and select the file destination_mediatek.xml<br>
6) All your Music including the updated ratings and play counts should be back<br>
7) Remove the duplicated play lists<br>
