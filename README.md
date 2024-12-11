# HDHomeRun EPG converter to XMLTV file

## Features

Program to download the current EPG from an HDHomeRun Quattro box for the next 7 days into an XMLTV formatted file.

I developed this so I could easily update the EPG on a Jellyfin media server that was linked to an HDHomeRun Quattro.  The HDHomeRun Quattro hardware automatically maintains the EPG for the channels it has tuned in, so it made sense to use this.

The HDHomeRun Quattro does have a limitation of 7 days EPG, so trying to go beyond that is pointless.

## Usage

```
python HDHomeRunEPG_To_XmlTv.py [--help] [--host <HOST>] [--filename <FILENAME>] [--days <DAYS>] [--hours <HOURS>] [--debug <DEBUG>]
```
