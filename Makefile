default: compile

	scp libintercept.so remarkable:
	ssh remarkable "LD_PRELOAD=/home/root/libintercept.so ls"

compile:
	@echo
	@echo "Make sure to"
	@echo "  source /usr/local/oecore-x86_64/environment-setup-cortexa9hf-neon-oe-linux-gnueabi"
	@echo
	arm-oe-linux-gnueabi-gcc -march=armv7-a -mfpu=neon -mfloat-abi=hard -mcpu=cortex-a9 --sysroot=/usr/local/oecore-x86_64/sysroots/cortexa9hf-neon-oe-linux-gnueabi -Wall -shared -ldl -fPIC intercept.c -o libintercept.so
