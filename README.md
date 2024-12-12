# HDHomeRun EPG converter to XMLTV file

## Features

Program to download the current EPG from an HDHomeRun Quattro box for the next 7 days into an XMLTV formatted file.

I developed this so I could easily update the EPG on a Jellyfin media server that was linked to an HDHomeRun Quattro.  The HDHomeRun Quattro hardware automatically maintains the EPG for the channels it has tuned in, so it made sense to use this.

The HDHomeRun Quattro does have a limitation of 7 days EPG, so trying to go beyond that is pointless.

## Usage

```
python HDHomeRunEPG_To_XmlTv.py [--help] [--host <HOST>] [--filename <FILENAME>] [--days <DAYS>] [--hours <HOURS>] [--debug <DEBUG>]
```

|      Paramater | Description     |
| -------------: | :-------------- |
| `--help`  | Show the command parameters available. |
| `--host <HOST>`  | The host name or IP address of the HDHomeRun server if different from "hdhomerun.local". |
| `--filename <FILENAME>` | The file path and name of the EPG to be generated. Defaults to epg.xml in the current directory. |
| `--days <DAYS>` | The number of days in the future from now to obtain an EPG for. Defaults to 7 but will be restricted to a max of about 14 by the HDHomeRun device. |
| `--hours <HOURS>` | The number of hours of guide interation to obtain. Defaults to 3 hours. |
| `--debug <DEBUG>` | Switch debug log message on, options in "on", "full" or "off". Defaults to "on" |
