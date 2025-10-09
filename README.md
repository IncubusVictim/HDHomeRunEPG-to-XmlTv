# HDHomeRun EPG converter to XMLTV file
<div align="right">
<a href="https://buymeacoffee.com/incubusvictim" target="_blank"><img align="top" src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a> <img align="top" src="https://github.com/IncubusVictim/HDHomeRunEPG-to-XmlTv/blob/main/bmc_qr.png" width="100" />
</div>

## Acknowledgments

Thanks to the following contributors for their support:

- [@supitsmike](https://github.com/supitsmike) – Fixed issue [#5](https://github.com/IncubusVictim/HDHomeRunEPG-to-XmlTv/issues/5): EPG - All programs listed as "New"
- [@AcSlayter](https://github.com/acslayter) – Added docker support

## Features

A Python program to download the current EPG from an HDHomeRun Quattro box for the next 7 days and convert this into an XMLTV formatted file.

I developed this so I could easily update the EPG on a Jellyfin media server that was linked to an HDHomeRun Quattro.  The HDHomeRun Quattro hardware can automatically provide the EPG for HDHomeRun application, so it made sense to use this as it is a perfect match for the channels used by Jellyfin.  I personally schedule it to run on a nightly basis at 1am shortly after which Jellyfin is scheduled to update its EPG from the newly generated XMLTV file.

<i><b>NOTE 1:</b> The Binaries I have generated are purely for those that are not comfortable running the Python application.  All of the binaries run on my local hardware and virtual machines, but if you have any problems please send me a message and I will try my best to help out.</i>

## Usage

```
python HDHomeRunEPG_To_XmlTv.py [--help] [--host <HOST>] [--filename <FILENAME>] [--days <DAYS>] [--hours <HOURS>] [--debug <DEBUG>]
```

|      Parameter | Description     |
| -------------: | :-------------- |
| `--help`  | Show the command parameters available. |
| `--host <HOST>`  | The host name or IP address of the HDHomeRun server if different from "hdhomerun.local". |
| `--filename <FILENAME>` | The file path and name of the EPG to be generated. Defaults to epg.xml in the current directory. |
| `--days <DAYS>` | The number of days in the future from now to obtain an EPG for. Defaults to 7 but will be restricted to the maximum number of days the HDHomeRun device will return. |
| `--hours <HOURS>` | The number of hours of guide interation to obtain. Defaults to 3 hours. This is an adavanced option which basically tells the app how many hours to increment for each query to the HDHomeRun device.  Making this too large will mean gaps can appear int he guide, equally making it too small will make the app run longer. Note any duplicate programmes retrieved are ignored anyway. |
| `--debug <DEBUG>` | Switch debug log message on, options are "on", "full" or "off". Defaults to "on". This is usefuly to see the detail of all the programmes being retrieved, but will mak the app take longer to run. |

## Python Pre-requisites

To run the Python application as described in the [Usage](#usage) section above, you will need the following elements set up:

### Install Python

Install Python onto your platform if it is not already available and ensure you can execute the following from you terminal/command/Powershell window:

```
python --version
```

If this return the Python version you have it installed correctly.

### Install PIP

With Python installed you should have the PIP utility to install Python packages. If not check instructions for your platform.

```
pip --version
```

OR 

```
pip3 --version
```

### Install HDHomeRunEPG_To_XmlTv Python packages

Install any packages that you do not have already installed. When you run the Python program it will complain about a missing package.

The following are obvious packages I needed to install to get this running:

```
pip3 install argparse
pip3 install requests
```

### Running the HDHomeRunEPG_To_XmlTv Python app

Simply run the HDHomeRunEPG_To_XmlTv app on your platform, e.g.

```
python HDHomeRunEPG_to_XmlTv.py --host 192.168.68.102
```

## Binaries

Please find a <b>binaries</b> directory in the repository root that contains a PyInstaller built distibution that can be run independently on the platform it is built for.  Extract the relevant binary platform zip files onto your machine and run according to the instructions below:

### Debian Linux (#7 Tested)

To run the Mac OS binary from a terminal window, put yourself in the binaries directory and run the following command with any parameters (as described above), e.g:

```
.\HDHomeRunEPG_To_XmlTv --host 192.168.1.100
```

If this fails and you need to make the HDHomeRunEPG_To_XmlTv runnable, type in the followwing before running it again:

```
chmod 755 HDHomeRunEPG_To_XmlTv
```

### Mac OS (#7 Tested)

To run the Mac OS binary from a terminal window, put yourself in the binaries directory and run the following command with any parameters (as described above), e.g:

```
.\HDHomeRunEPG_To_XmlTv --host 192.168.1.100
```

If this fails and you need to make the HDHomeRunEPG_To_XmlTv runnable, type in the followwing before running it again:

```
chmod 755 HDHomeRunEPG_To_XmlTv
```

### Windows (#7 Tested)

To run the Mac OS binary from a terminal window, put yourself in the binaries directory and run the following command with any parameters (as described above), e.g:

```
.\HDHomeRunEPG_To_XmlTv --host 192.168.1.100
```
# Docker Usage

You can run this project using Docker. Here are the steps:

1. **Update the HDHomeRun host:**
	Edit the `HOST` environment variable in your `docker-compose.yml` file or set it directly in your Docker command. Example:
	```yaml
	environment:
	  - HOST=192.168.1.100
	```
	Or set it in your run command:
	```sh
	docker run --rm -e HOST=192.168.1.100 hdhomerun-epg
	```

2. **Build the Docker image:**
	```sh
	docker compose build
	```

3. **Start the container:**
	```sh
	docker compose up
	```

4. **Cron schedule:**
	The script is scheduled to run every day at 1am using cron inside the container:
	```cron
	0 1 * * *
	```
	This will automatically update the EPG file as specified by the `FILENAME` environment variable.

---
