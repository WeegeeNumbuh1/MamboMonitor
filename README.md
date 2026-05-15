<!-- Title -->
<a id="readme-top"></a>
<div align="center">
    <a href="https://github.com/WeegeeNumbuh1/MamboMonitor">
    <img src="mambo.jpg" alt="Matikanetannhauser" height="240">
    </a>
    <h1 align="center">MamboMonitor</h1>
    Umamusume gif player for rgbmatrix displays.
</div>
<!-- end title section -->

# What this is

A gif viewer that selects a random gif to play from a folder of gifs, renders it to an rgbmatrix display, and continues selecting random gifs until all are played, then starts all over again. Designed to run without a network connection.

> [!NOTE]
> This setup can be used for other kinds of gif collections. This just happens to be Umamusume themed.

> [!IMPORTANT]
> Most of this code was rushed, but works. Expect more refinements at some point if I ever get around to it.<br>
> (No LLMs were involved in this project.)

# How to use

This project assumes you're familiar with [rgbmatrix displays](https://github.com/hzeller/rpi-rgb-led-matrix) and have a Raspberry Pi on hand.<br>
These scripts are not designed for any other setups (Arduino, ESP32, etc.)

- Clone this repo:
```
git clone --depth=1 https://github.com/WeegeeNumbuh1/MamboMonitor
```
- Add URLs to [`links.txt`](/links.txt).
- Run the install script [`install.sh`](/install.sh) to install the required python packages and install the service.
- Run [`main_downloader.py`](./tools/main_downloader.py) in [`tools`](/tools/) to download Umamusume gifs from Tenor if you don't have any already.
- Edit [`config.yaml`](/config.yaml) to match your existing rgbmatrix setup.
  - The defaults are based on my personal config (2x 64x32 displays in V-Mapper:Z orientation)
- Run the main script, [`MatikanetannhauserMain.py`](./MatikanetannhauserMain.py)

If you wish to uninstall, use the `uninstall.sh` script (coming soon).

# Other stuff

Most of the code was adapted from my other project, [FlightGazer](https://github.com/WeegeeNumbuh1/FlightGazer).

### As Implemented

<div align="center"><img src="media/MamboMonitor_irl.jpg" alt="lmao wtf" height="420">
</div>

### License

(to be decided)