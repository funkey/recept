#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <dlfcn.h>

static int event_fd = 0;

// size of the ring buffer
#define N 16

struct ring {

	uint32_t values[N];
	uint8_t index;
	uint32_t sum;
};

static struct ring ring_x = { {0}, 0, 0 };
static struct ring ring_y = { {0}, 0, 0 };

void ring_add(struct ring* ring, const uint32_t value) {

	ring->index = (ring->index + 1) % N;
	const uint32_t oldest = ring->values[ring->index];
	ring->sum = ring->sum + value - oldest;
	ring->values[ring->index] = value;
}

uint32_t ring_average(const struct ring* ring) {

	return ring->sum/N;
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
	// type == 1 && code == 330 && value == 0 -> pen down(?)
	// type == 3 && code == 0 -> value == x
	// type == 3 && code == 1 -> value == y
	// type == 3 && code == 24 -> value == pressure
	// type == 3 && code == 25 -> value == distance
	// type == 3 && code == 26 -> value == tilt x
	// type == 3 && code == 27 -> value == tilt y

	if (type == 3) {

		if (code == 0) {

			ring_add(&ring_x, value);
			value = ring_average(&ring_x);

		} else if (code == 1) {

			ring_add(&ring_y, value);
			value = ring_average(&ring_y);
		}

		// copy value back to buffer
		buf[12] = (uint8_t)value;
		buf[13] = (uint8_t)(value >> 8);
		buf[14] = (uint8_t)(value >> 16);
		buf[15] = (uint8_t)(value >> 24);
	}
}

int open(const char* filename, int flags) {

	static int (*real_open)(const char*, int) = NULL;
	if (!real_open)
		real_open = dlsym(RTLD_NEXT, "open");

	int fd = real_open(filename, flags);

	if (strcmp(filename, "/dev/input/event1") == 0) {

		printf(">| someone is trying to open event1, let's remember the fd!\n");
		printf(">| (psssst: it is %d)\n", fd);
		event_fd = fd;
	}

	return fd;
}

ssize_t read(int fd, void* buf, size_t count) {

	static ssize_t (*real_read)(int, void*, size_t) = NULL;
	if (!real_read)
		real_read = dlsym(RTLD_NEXT, "read");

	ssize_t ret = real_read(fd, buf, count);

	if (fd != 0 && fd == event_fd && ret == 16)
		filter(buf);

	return ret;
}
