# Hovercraft systemd unitfiles

Here lies template systemd unit files for starting various services upon
Raspbery Pi boot.

# Usage

Copy the file to `/etc/systemd/system/`. Change values depending on the system
(follow the comments in the files).

Enable the service:

```
sudo systemctl enable servicename@username
```

Where `servicename` is the service and `username` is the username of the
primary user on the Raspberry Pi (say, frank).
