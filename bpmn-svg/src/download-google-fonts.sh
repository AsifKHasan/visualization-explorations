#!/usr/bin/env bash
sudo apt-get install fonts-cantarell ttf-ubuntu-font-family git
srcdir="/tmp/google-fonts"
pkgdir="/usr/share/fonts/truetype/google-fonts"
giturl="git://github.com/google/fonts.git"

mkdir $srcdir
cd $srcdir
echo "Cloning Git repository..."
git clone $giturl

echo "Installing fonts..."
sudo mkdir -p $pkgdir
sudo find $srcdir -type f -name "*.ttf" -exec install -Dm644 {} $pkgdir \;

echo "Cleaning up..."
sudo find $pkgdir -type f -name "Cantarell-*.ttf" -delete \;
sudo find $pkgdir -type f -name "Ubuntu-*.ttf" -delete \;

# provides roboto
sudo apt-get --purge remove fonts-roboto

echo "Updating font-cache..."
sudo fc-cache -f > /dev/null

echo "Done!"
