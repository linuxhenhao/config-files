## notifications for new installation

### 1. packages

```
apt-get install 
awesomewm
xinit
xserver-xorg-video-XXX(intel/or others)
xcompmgr (window transparency)
fcitx fcitx-libpinyin (input)
firefox (web browser)
volumeicon-alsa (volume control)
neovim (command line editor)
privoxy (proxy/filter/ad blocker)
proxychains (proxy in terminal)
git (VCS)
```

mannual install, their readmes have details about installation process.
```
[alacritty](https://github.com/jwilm/alacritty)  (fast terminal emulator)
[mcfly](https://github.com/cantino/mcfly) (fast command line history)
[rustup](rust program language env manager)
vscode
```


### 2. sound problems

After install debian testing on my newly constructed amd ryzen 3600,
with an ALC 892 sound card on board, the system has no sound.

First install `pulseaudio-utils`, then you'll have a `pacmd` command.
using the following command to check output device

```
pacmd list-sinks
```
The result shows that system only has a sink device which has a description "Dummy output".
This means that for the kernel dosen't know a real device to put audio signal to.

using the following command, finnally the system got a right way to make sound.

```
pacmd set-card-profile 1 output:analog-stereo+input:analog-stereo
```
The `1` in the above command representing the card index, which can be get from `pacmd list-cards`
command, in my results, index 0 is the nvidia hdmi audio output card, index 1 is the onboard
`ALC892` card. the profile name can also be retrieved from the `list-cards` results.
`output:analog-stereo+input:analog-stereoo` was choosed.

To make this change take effect after reboot, add the following line in the file: `/etc/pulse/default.pa`

```
set-card-profile 1 output:analog-stereo+input:analog-stereo
```


