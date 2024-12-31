# HDHomeRun EPG converter to XMLTV file

## Features

A Python program to download the current EPG from an HDHomeRun Quattro box for the next 7 days and convert this into an XMLTV formatted file.

I developed this so I could easily update the EPG on a Jellyfin media server that was linked to an HDHomeRun Quattro.  The HDHomeRun Quattro hardware automatically maintains the EPG for the channels it has tuned in, so it made sense to use this as it is a perfect match for the channels used by Jellyfin.  I personally schedule it to run on a nightly basis at 1am shortly after which Jellyfin is scheduled to update its EPG from the newly generated XMLTV file.

<i><b>NOTE 1:</b> The HDHomeRun Quattro does have a limitation of 7 days EPG, so trying to go beyond that is pointless.</i>

<i><b>NOTE 2:</b> The Binaries I have generated are purely for those that are not comfortable running the Python application.  All of the binaries run on my local hardware and virtual machines, but if you have any problems please send me a message and I will try my best to help out.</i>

## Usage

```
python HDHomeRunEPG_To_XmlTv.py [--help] [--host <HOST>] [--filename <FILENAME>] [--days <DAYS>] [--hours <HOURS>] [--debug <DEBUG>]
```

|      Paramater | Description     |
| -------------: | :-------------- |
| `--help`  | Show the command parameters available. |
| `--host <HOST>`  | The host name or IP address of the HDHomeRun server if different from "hdhomerun.local". |
| `--filename <FILENAME>` | The file path and name of the EPG to be generated. Defaults to epg.xml in the current directory. |
| `--days <DAYS>` | The number of days in the future from now to obtain an EPG for. Defaults to 7 but will be restricted to the maximum number of days the HDHomeRun device will return. |
| `--hours <HOURS>` | The number of hours of guide interation to obtain. Defaults to 3 hours. This is an adavanced option which basically tells the app how many hours to increment for each query to the HDHomeRun device.  Making this too large will mean gaps can appear int he guide, equally making it too small will make the app run longer. Note any duplicate programmes retrieved are ignored anyway. |
| `--debug <DEBUG>` | Switch debug log message on, options are "on", "full" or "off". Defaults to "on". This is usefuly to see the detail of all the programmes being retrieved, but will mak the app take longer to run. |

## Binaries

Please find a <b>binaries</b> directory in the repository root that contains a PyInstaller built distibution that can be run independently on the platform it is built for.  Extract the relevant binary platform zip files onto your machine and run according to the instructions below:

### Linux (Tested)

To run the Mac OS binary from a terminal window, put yourself in the binaries directory and run the following command with any parameters (as described above), e.g:

```
.\HDHomeRunEPG_To_XmlTv --host 192.168.1.100
```

If this fails and you need to make the HDHomeRunEPG_To_XmlTv runnable, type in the followwing before running it again:

```
chmod 755 HDHomeRunEPG_To_XmlTv
```

### Mac OS (Tested)

<i><b>IMPORTANT: The Mac OS binary is not reliable yet due to an SSL library issue I need to resolve.</b></i>

To run the Mac OS binary from a terminal window, put yourself in the binaries directory and run the following command with any parameters (as described above), e.g:

```
.\HDHomeRunEPG_To_XmlTv --host 192.168.1.100
```

If this fails and you need to make the HDHomeRunEPG_To_XmlTv runnable, type in the followwing before running it again:

```
chmod 755 HDHomeRunEPG_To_XmlTv
```

### Windows (Tested)

To run the Mac OS binary from a terminal window, put yourself in the binaries directory and run the following command with any parameters (as described above), e.g:

```
.\HDHomeRunEPG_To_XmlTv --host 192.168.1.100
```
