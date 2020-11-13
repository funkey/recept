#include <cstdint>
#include <array>
#include <limits>

#define ARMA_DONT_USE_LAPACK
#define ARMA_DONT_USE_BLAS
#include <armadillo>

using namespace arma;

class kalman_filter {

public:

	typedef float T;

	typedef Col<T> col;
	typedef Mat<T> mat;
	typedef col::fixed<2> vec_x;
	typedef col::fixed<1> vec_z;
	typedef mat::fixed<2, 2> mat_xx;
	typedef mat::fixed<2, 1> mat_xz;
	typedef mat::fixed<1, 2> mat_zx;
	typedef mat::fixed<1, 1> mat_zz;

	kalman_filter(const T& sigma_x, const T& sigma_z) {

		_I.eye();
		_F = {
			{1, 1},
			{0, 1}
		};
		_H = {
			{1, 0}
		};
		_Q = {
			{0.25, 0.5},
			{0.5, 1}
		};
		_Q *= sigma_x;
		_R = sigma_z;

		reset();
	}

	inline void reset() {

		_x[1] = std::numeric_limits<T>::max();
	}

	inline T step(const T& z) {

		if (_x[1] == std::numeric_limits<T>::max()) {

			_x = {z, 0};
			_P = {
				{1.0, 0},
				{0, 1.0}
			};

			return z;
		}

		// predict
		_x = _F*_x;
		_P = _F*_P*_F.t() + _Q;

		// update
		_K = _P*_H.t()*(_H*_P*_H.t() + _R).i();
		_x = _x + _K*(z - _H*_x);
		_P = (_I - _K*_H)*_P;

		return _x[0];
	}

private:

	// state
	vec_x _x;
	// state covariance
	mat_xx _P;

	// state transition
	mat_xx _F;
	// measurement
	mat_zx _H;
	// covariance of process noise
	mat_xx _Q;
	// covariance of observation noise
	mat_zz _R;

	// identity matrix
	mat_xx _I;
	// Kalman gain
	mat_xz _K;
};


static kalman_filter kalman_x(0.01, 100.0);
static kalman_filter kalman_y(0.01, 100.0);

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

		kalman_x.reset();
		kalman_y.reset();
	}

	if (type == 3) {

		if (code == 0) {

			value = (uint32_t)kalman_x.step((float)value);

		} else if (code == 1) {

			value = (uint32_t)kalman_y.step((float)value);
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

	if (strcmp(filename, "/dev/input/event1") == 0) {

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
