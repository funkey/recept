#include <cstdint>
#include <array>
#include <limits>

#ifndef RING_SIZE
#define RING_SIZE 16
#endif
#ifndef INPUT_DEVICE
#define _INPUT_DEVICE "/dev/input/event1"
#else
#define toString(_arg) #_arg
#define _INPUT_DEVICE toString(INPUT_DEVICE)
#endif

template<typename T, int Size>
class ring {

public:

	inline void add(const T& value) {

		if (empty()) {

			fill(value);
			return;
		}

		_index = (_index + 1) % Size;
		const T& oldest = _values[_index];
		_sum = _sum + value - oldest;
		_values[_index] = value;
	}

	inline void clear() {

		_sum = std::numeric_limits<T>::max();
	}

	inline bool empty() const {

		return _sum == std::numeric_limits<T>::max();
	}

	/**
	 * Return the last (i.e., newest) item added to the ring.
	 */
	inline const T& front() const {

		return _values[_index];
	}

	inline void fill(const T& value) {

		_values.fill(value);
		_sum = value*Size;
	}

	inline T sum() const {

		return _sum;
	}

	inline T average() const {

		return _sum/Size;
	}

private:

	std::array<T, Size> _values;
	uint8_t _index;
	T _sum;
};

static ring<uint32_t, RING_SIZE> ring_x;
static ring<uint32_t, RING_SIZE> ring_y;

template<typename Ring>
inline uint32_t update_pos(Ring& ring, uint32_t value) {

	ring.add(value);
	return ring.average();
}

void filter(char* buf) {

	const uint8_t type = (uint8_t)buf[8];
	const uint16_t code = (
		(uint16_t)buf[10]      |
		(uint16_t)buf[11] << 8);
	uint32_t value = (
		(uint32_t)buf[12]       |
		(uint32_t)buf[13] << 8  |
		(uint32_t)buf[14] << 16 |
		(uint32_t)buf[15] << 24);

	// type == 1 && code == 320 && value == 1 -> pen in
	// type == 1 && code == 320 && value == 0 -> pen out
	// type == 1 && code == 321 && value == 1 -> eraser in
	// type == 1 && code == 321 && value == 0 -> eraser out
	//
	// type == 1 && code == 330 && value == 1 -> pen/eraser down
	// type == 1 && code == 330 && value == 0 -> pen/eraser up
	//
	// type == 3 && code == 0 -> value == x
	// type == 3 && code == 1 -> value == y
	// type == 3 && code == 24 -> value == pressure
	// type == 3 && code == 25 -> value == distance
	// type == 3 && code == 26 -> value == tilt x
	// type == 3 && code == 27 -> value == tilt y

	// pen/eraser in
	if (type == 1 && ((code == 320 && value == 1) || (code == 321 && value == 1))) {

		ring_x.clear();
		ring_y.clear();
	}

	if (type == 3) {

		if (code == 0) {

			value = update_pos(ring_x, value);

		} else if (code == 1) {

			value = update_pos(ring_y, value);
		}

		// copy value back to buffer
		buf[12] = (uint8_t)value;
		buf[13] = (uint8_t)(value >> 8);
		buf[14] = (uint8_t)(value >> 16);
		buf[15] = (uint8_t)(value >> 24);
	}
}

extern "C" {

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdio.h>
#include <string.h>
#include <dlfcn.h>

typedef int (*t_open)(const char*, int);
typedef ssize_t (*t_read)(int, void*, size_t);

static int event_fd = 0;

int open(const char* filename, int flags) {

	static t_open real_open = NULL;
	if (!real_open)
		real_open = (t_open)dlsym(RTLD_NEXT, "open");

	int fd = real_open(filename, flags);

	if (strcmp(filename, _INPUT_DEVICE) == 0) {

		printf(">| someone is trying to open event1, let's remember the fd!\n");
		printf(">| (psssst: it is %d)\n", fd);
		event_fd = fd;
	}

	return fd;
}

ssize_t read(int fd, void* buf, size_t count) {

	static t_read real_read = NULL;
	if (!real_read)
		real_read = (t_read)dlsym(RTLD_NEXT, "read");

	ssize_t ret = real_read(fd, buf, count);

	if (fd != 0 && fd == event_fd && ret == 16)
		filter((char*)buf);

	return ret;
}

}
