default: rm2 rm1

rm2:
	mkdir -p build/rm2
	for rs in `seq 2 32`; \
	do \
	  $(CXX) \
	      $(CXXFLAGS)\
	      -DRING_SIZE=$$rs \
	      -DINPUT_DEVICE=/dev/input/event1 \
	      -Wall \
	      -shared \
	      -ldl \
	      -fPIC \
	      recept.cpp \
	      -o build/rm2/librecept_rs$$rs.so; \
	done

rm1:
	mkdir -p build/rm1
	for rs in `seq 2 32`; \
	do \
	  $(CXX) \
	      $(CXXFLAGS)\
	      -DRING_SIZE=$$rs \
	      -DINPUT_DEVICE=/dev/input/event0 \
	      -Wall \
	      -shared \
	      -ldl \
	      -fPIC \
	      recept.cpp \
	      -o build/rm1/librecept_rs$$rs.so; \
	done

test-rm1:
	scp build/rm1/librecept_rs32.so root@remarkable:librecept.so
	ssh remarkable "LD_PRELOAD=/home/root/librecept.so ls"

test-rm2:
	scp build/rm2/librecept_rs16.so root@remarkable:librecept.so
	ssh remarkable "LD_PRELOAD=/home/root/librecept.so ls"
