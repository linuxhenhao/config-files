## notifications for new installation

### 1. packages

```
apt-get install 
awesome
awesome-extra
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



### 3. Network configuration

For some reason, Network proxy is a *Must have* feature. Wireguard is a very good and secure virtual private network service provider. 

By default, wg-quick using fwmark and ip rule to configure policy based route database, if any route was matched in main route table (except default route), the packets will be sent out using default device. otherwise the wireguard network would be used. To avoid long travel of `local` network packets, a chnroute.txt which contains nearly all IPs in China was used to produce lots of rows in main route table.

But there is still a problem, As is known to all, to provide better service to people all over the world, Lots of companies are using CDN, which means the server IP got from DNS query is varied according to the request's source. If all of the DNS requests were sent out by remote wireguard server, Even there are some servers located very close to our original computer, we finally established a connection to a remote CDN server. That's unacceptable! To avoid such a problem, a service named chinadns should be enabled.

In repo `config-files`, the deb package of chinadns can be found.

```
dpkg -i packages/chinadns.deb
systemctl enable chinadns.service
systemctl start chinadns.service
rm /etc/resolv.conf
echo "nameserver 127.0.0.1" > /etc/resolv.conf
```

When configuring wireguard, a PostUp script should be run, it was located in repo `config-files`, too.

```
[Interface]
xxx
xxx
PostUp = /path/to/chinadns_routes.py up
PreDown = /path/to/chinadns_routes.py down
```

enable virtual network as a auto startup service

```
systemctl enable wg-quick@wg0  # wg0 means using /etc/wireguard/wg0.conf
```
