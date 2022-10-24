#scripts to run and stuff

.PHONY: install

install: 
	sudo apt-get install rpi.gpio\
	sudo apt-get install python3-rpi.gpio\
	sudo pip3 install gpiozero\
