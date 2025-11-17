#include "exception.hpp"


void NativeException::exception0() throw(Error0) {
    throw Error0();
}

void NativeException::exception1() {
    throw Error1();
}

void NativeException::exception2() throw(Error2) {
    throw Error2();
}

void NativeException::exception3() {
    throw Error3();
}
