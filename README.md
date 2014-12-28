MonkeyShifter
=============

The app is designed to sort media files into categories automatically (it will search movie databases for name matches etc)

i.e The app will have a configured directory/ies that it will pick up files that need to be sorted. For a file name like:

Absolutely.Fabulous.S01E00.Pilot.Mirrorball.DVDRip.DivX-CthragSardius.[sharethefiles.com].avi 

1) Files with the correctly configured type will be matched to configured category (.avi/.mkv = media, .iso/.exe = app)
2) The name will broken into words usings a list of common word seprators ([space],.-)
3) Duplicate files will be matched via word distance algorthim. Duplicates will be removed/moved (will be configured)
4) Common technical words will be matched via stored hash list (filled via tunning) be removed list (of words) (i.e DVDRip,DivX,[sharethefiles.com],CthragSardius)
5) Words that may indicated media type/category will be matched via stored hash list (fille via tunning), i.e S01E00 = tv show
6) Any left over words will be matched with previously sorted record stored in hash list
