%module error

%{
#include "error.h"

PyObject *PyExc_Error = NULL;
%}

%init {
    PyExc_Error = PyErr_NewException("_error.Error", NULL, NULL);
    Py_INCREF(PyExc_Error);
    PyModule_AddObject(m, "Error", PyExc_Error);
}

// SWIG_From_frag(int) = SWIG_From_int
// Native な値を Python オブジェクトに変換する。
%typemap(out, fragment=SWIG_From_frag(int)) int error0, int error1 {

    if (1 == result) {
        SWIG_Error(SWIG_RuntimeError, "1");
        SWIG_fail;
    }

    if (2 == result) {
        SWIG_SetErrorObj(SWIG_ErrorType(SWIG_RuntimeError), SWIG_From_int(result));
        SWIG_fail;
    }

    if (3 == result) {
        SWIG_SetErrorObj(PyExc_Error, SWIG_From_int(result));
        SWIG_fail;
    }

    $result = SWIG_From_int(result);
}

%pythoncode %{
    Error = _error.Error
%}

%include "error.h"
