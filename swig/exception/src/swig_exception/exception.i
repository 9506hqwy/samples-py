%module exception

%{
#include "exception.hpp"
%}

%catches(Error1) NativeException::exception1;

%typemap(throws) Error2 %{
    PyObject *err = SWIG_NewPointerObj(&$1, $&1_descriptor, SWIG_POINTER_OWN);
    SWIG_SetErrorObj(SWIG_ErrorType(SWIG_RuntimeError), err);
    SWIG_fail;
%}

%exception exception3 {
    try {
        $action
    }
    catch (Error3 &e) {
        PyObject *err = SWIG_NewPointerObj(&e, SWIGTYPE_p_Error3, SWIG_POINTER_OWN);
        SWIG_SetErrorObj(SWIG_ErrorType(SWIG_RuntimeError), err);
        SWIG_fail;
    }
}

%include "exception.hpp"
