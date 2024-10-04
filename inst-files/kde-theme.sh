#!/bin/bash

mkdir -p ~/.config/
cat <<EOL > ~/.config/kdeglobals
[General]
ColorScheme=Yellow
EOL

mkdir -p ~/.local/share/config/colors
cat <<EOL > ~/.local/share/config/colors/Yellow.colors
[ColorScheme]
Name=Yellow
ColorBackground=255,255,204
ColorForeground=0,0,0
ColorHighlight=255,255,0
ColorHighlightText=0,0,0
EOL

# Apply the theme
qdbus org.kde.plasmashell org.kde.plasmashell.reloadConfig
