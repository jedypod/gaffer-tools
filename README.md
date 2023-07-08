# Gaffer Tools
A collection of tools for [Gaffer](https://www.gafferhq.org) primarily focusing on image, color, and plotting.

# Installation
First, clone this repo to some location on disk, let's call it `/path/to/gaffer-tools`.
Second, we'll need to set up a couple of environment variables so that the nodes are loaded
into the node menu. I'll use Bash in this example but you can adapt it to your needs. We use
the `GAFFER_STARTUP_PATHS` to execute `loadNodes.py` on startup. This script adds all `.grf` 
Gaffer Reference Files and `.gfr` Gaffer Script Files into the node menu, re-creating the 
directory structure of the folders on disk in the node menu.

```
# Add startup directory to GAFFER_STARTUP_PATHS so `loadNodes.py` is executed on startup.
export GAFFER_STARTUP_PATHS=/path/to/gaffer-tools/startup:${GAFFER_STARTUP_PATHS}

# Add GAFFER_TOOLS_ROOT so gfr and grf files under tools are auto-loaded in the node menu.
export GAFFER_TOOLS_ROOT=/path/to/gaffer-tools/tools
```

If environment variables are inconvenient, you can also copy the `loadNodes.py` file into your
`~/gaffer/startup/gui` folder, and hard-code the filepath in that python file by setting the
GAFFER_TOOLS_ROOT variable to `/path/to/gaffer-tools`.

# Tools
Nodes are provided as `.grf` Gaffer Reference files.
## Gaffer Color Tools
### ColorMatrix
Applies a 3x3 matrix to the RGB channels of an incoming image. Supports inverse direction.

### GamutConvert
Converts an image from `inGamut` to `outGamut`.
