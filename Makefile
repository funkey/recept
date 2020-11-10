default: compile

	scp libintercept.so remarkable:
	ssh remarkable "LD_PRELOAD=/home/root/libintercept.so ls"

compile:
	. /usr/local/oecore-x86_64/environment-setup-cortexa9hf-neon-oe-linux-gnueabi; arm-oe-linux-gnueabi-g++ -march=armv7-a -mfpu=neon -mfloat-abi=hard -mcpu=cortex-a9 --sysroot=/usr/local/oecore-x86_64/sysroots/cortexa9hf-neon-oe-linux-gnueabi -Wall -shared -ldl -fPIC -O3 intercept.cpp -o libintercept.so
