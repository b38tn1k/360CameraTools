# Multi GoPro SD Importer
For use with 360 GoPro camera rigs of any size! Card names must be in convention C## eg C01, C02, etc

##How to Run
Running ./imp 28 34 23 43 2 33 44 65 will grab all footage of SD cards named C28, C34, C23, C43, C02, etc and drop them all in a chosen directory. Running ./imp 1 2 3 followed by ./imp 4 5 6 -m will import footage from all 6 SDs into the same take/dump directory

##What it does:
* imports all footage of the SD cards with prepended camera numbers
* creates a take-specific CSV receipt detailing notes, location, time, camera rig used, fps, bitrate, duration, etc
* creates a master location CSV
* stores some information between uses for easy repeated use on set
