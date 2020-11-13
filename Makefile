default: compile

compile:
	! mkdir precompiled
	. /usr/local/oecore-x86_64/environment-setup-cortexa9hf-neon-oe-linux-gnueabi; \
	arm-oe-linux-gnueabi-g++ \
		-DRING_SIZE=16 \
		-I./armadillo-10.1.2/include \
		-march=armv7-a \
		-mfpu=neon \
		-mfloat-abi=hard \
		-mcpu=cortex-a9 \
		--sysroot=/usr/local/oecore-x86_64/sysroots/cortexa9hf-neon-oe-linux-gnueabi \
		-Wall \
		-shared \
		-ldl \
		-fPIC \
		-faligned-new \
		-std=c++11 \
		-O3 \
		recept.cpp \
		-o precompiled/librecept.so;
