#scripts to run and stuff

.PHONY: install startup


# installs not needed anymore \
	#sudo apt-get install rpi.gpio\
	#sudo apt-get install python3-rpi.gpio
install: 
	sudo apt install pigpio\
	sudo pip3 install gpiozero

