# Inkscape colour label extension

An extension to [Inkscape](https://inkscape.org) to label features with their fill colour value.

![label-colours_650x480](/uploads/07ee96d63a9615a7c1f35d2bb8077f79/label-colours_650x480.png)

## Installation
Download [labelColour.inx](./labelColour.inx) and [labelColour.py](./labelColour.py), and save them into your Inkscape installation’s extension folder (see *Edit*→*Preferences*→*System*→*User extensions*). Restart Inkscape.

## Usage
Select one of more features, choose *Colour*→*Label features with fill colour* from the *Extension* menu.

*Note:* As of this writing, this plugin does not handle SVG `transform` parameters. To work around missplaced labels, select the features, then choose *Options*→*Transform* and apply a 0-transformation (e.g. rotate or move), check the *Apply to each object separately* box.
