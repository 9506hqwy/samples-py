%module native

%{
#include <libvirt.h>

void pyEventTimeoutCallback(int timer,
                            void *opaque) {

    PyObject *func = NULL;
    PyObject *args = NULL;

    func = (PyObject*)opaque;
    args = Py_BuildValue("(i)", timer);

    PyObject_Call(func, args, NULL);

    Py_DECREF(args);
}

void pyConnectStoragePoolEventLifecycleCallback(virConnectPtr conn,
                                                virStoragePoolPtr pool,
                                                int event,
                                                int detail,
                                                void *opaque) {
    PyObject *pyconn = NULL;
    PyObject *pypool = NULL;
    PyObject *func = NULL;
    PyObject *args = NULL;

    pyconn = SWIG_NewPointerObj(SWIG_as_voidptr(conn), SWIGTYPE_p__virConnect, 0);
    pypool = SWIG_NewPointerObj(SWIG_as_voidptr(pool), SWIGTYPE_p__virStoragePool, 0);

    func = (PyObject*)opaque;
    args = Py_BuildValue("(O, O i, i)", pyconn, pypool, event, detail);

    PyObject_Call(func, args, NULL);

    Py_DECREF(args);
}
%}

// 1つの出力パラメータを戻り値に設定する。
// 本来の戻り値と出力パラメータを配列で返却するようになる。
// - virConnectGetVersion
%apply unsigned long *OUTPUT { unsigned long *hvVer };

// 出力パラメータが文字列の配列の場合に戻り値に設定する。
// 入力から配列領域を確保し出力時に Python オブジェクトに変換する。
// - virConnectListDefinedDomains
// - virConnectListInterfaces
// - virConnectListDefinedInterfaces
// - virConnectListNetworks
// - virConnectListDefinedNetworks
// - virNodeListDevices
// - virNodeDeviceListCaps
// - virConnectListNWFilters
// - virConnectListStoragePools
// - virConnectListDefinedStoragePools
// - virStoragePoolListVolumes
%typemap(in, numinputs=1) (char ** const names, int maxnames) {
    // input 時に maxnames が返却できるメモリ領域を確保する。
    int size = (int)PyLong_AsLong($input);

    // C-API に渡す引数1 (names)
    $1 = (char**)calloc(size, sizeof(char) * 1024);
    // C-API に渡す引数2 (maxnames)
    $2 = size;
}
%typemap(argout) char ** const names {
    // 戻り値から取得した個数を取得する。
    int n = (int)PyLong_AsLong($result);

    // 出力時に変換する。
    PyObject *list = PyList_New(n);
    for (int i = 0; i < n; i++) {
        PyObject *str = PyUnicode_FromString($1[i]);
        PyList_SetItem(list, i, str);
    }

    // 出力に追加する。
    $result = SWIG_AppendOutput($result, list);

    free($1);
}

// 構造体配列ポインタの出力を戻り値に設定する。
// - virConnectListAllStoragePools
%typemap(in, numinputs=0) virStoragePoolPtr **pools (virStoragePoolPtr *tempPools) {
    // C-API に渡す引数1 (pools)
    $1 = &tempPools;
}
%typemap(argout) virStoragePoolPtr **pools {
    // 戻り値から取得した個数を取得する。
    int n = (int)PyLong_AsLong($result);

    // 出力時に変換する。
    PyObject *list = PyList_New(n);
    for (int i = 0; i < n; i++) {
        PyObject *pool = SWIG_NewPointerObj(SWIG_as_voidptr(*$1[i]), SWIGTYPE_p__virStoragePool, 0);
        PyList_SetItem(list, i, pool);
    }

    // 出力に追加する。
    $result = SWIG_AppendOutput($result, list);
}

// コールバック関数を python コードで指定し、opaque として C-API のコールバックを実行する。
// - virEventAddTimeout
%typemap(in, numinputs=1) (virEventTimeoutCallback cb, void *opaque, virFreeCallback ff) {
  // C-API に渡す引数1 (cb)
  $1 = (virEventTimeoutCallback)pyEventTimeoutCallback;
  // C-API に渡す引数2 (opaque)
  $2 = (void*)$input;
  // C-API に渡す引数23 (freecb)
  $3 = NULL;
}

// コールバック関数を python コードで指定し、opaque として C-API のコールバックを実行する。
// - virConnectStoragePoolEventRegisterAny
%typemap(in, numinputs=1) (virConnectStoragePoolEventGenericCallback cb, void *opaque, virFreeCallback freecb) {
  // C-API に渡す引数1 (cb)
  $1 = (virConnectStoragePoolEventGenericCallback)pyConnectStoragePoolEventLifecycleCallback;
  // C-API に渡す引数2 (opaque)
  $2 = (void*)$input;
  // C-API に渡す引数23 (freecb)
  $3 = NULL;
}

%inline {
#define __VIR_LIBVIRT_H_INCLUDES__
}

%include "libvirt-common.h"
%include "libvirt-host.h"
%include "libvirt-domain.h"
%include "libvirt-domain-checkpoint.h"
%include "libvirt-domain-snapshot.h"
%include "libvirt-event.h"
%include "libvirt-interface.h"
%include "libvirt-network.h"
%include "libvirt-nodedev.h"
%include "libvirt-nwfilter.h"
%include "libvirt-secret.h"
%include "libvirt-storage.h"
%include "libvirt-stream.h"
