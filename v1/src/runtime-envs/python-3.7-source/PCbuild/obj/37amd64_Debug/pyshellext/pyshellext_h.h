

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


 /* File created by MIDL compiler version 8.01.0622 */
/* at Tue Jan 19 03:14:07 2038
 */
/* Compiler settings for ..\PC\pyshellext.idl:
    Oicf, W1, Zp8, env=Win64 (32b run), target_arch=AMD64 8.01.0622 
    protocol : all , ms_ext, c_ext, robust
    error checks: allocation ref bounds_check enum stub_data 
    VC __declspec() decoration level: 
         __declspec(uuid()), __declspec(selectany), __declspec(novtable)
         DECLSPEC_UUID(), MIDL_INTERFACE()
*/
/* @@MIDL_FILE_HEADING(  ) */



/* verify that the <rpcndr.h> version is high enough to compile this file*/
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 500
#endif

#include "rpc.h"
#include "rpcndr.h"

#ifndef __RPCNDR_H_VERSION__
#error this stub requires an updated version of <rpcndr.h>
#endif /* __RPCNDR_H_VERSION__ */


#ifndef __pyshellext_h_h__
#define __pyshellext_h_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

#ifndef __PyShellExt_FWD_DEFINED__
#define __PyShellExt_FWD_DEFINED__

#ifdef __cplusplus
typedef class PyShellExt PyShellExt;
#else
typedef struct PyShellExt PyShellExt;
#endif /* __cplusplus */

#endif 	/* __PyShellExt_FWD_DEFINED__ */


/* header files for imported files */
#include "ocidl.h"

#ifdef __cplusplus
extern "C"{
#endif 



#ifndef __PyShellExtLib_LIBRARY_DEFINED__
#define __PyShellExtLib_LIBRARY_DEFINED__

/* library PyShellExtLib */
/* [version][uuid] */ 


DEFINE_GUID(LIBID_PyShellExtLib,0x44039A76,0x3BDD,0x41C1,0xA3,0x1B,0x71,0xC0,0x02,0x02,0xCE,0x81);

DEFINE_GUID(CLSID_PyShellExt,0xBEA218D2,0x6950,0x497B,0x94,0x34,0x61,0x68,0x3E,0xC0,0x65,0xFE);

#ifdef __cplusplus

class DECLSPEC_UUID("BEA218D2-6950-497B-9434-61683EC065FE")
PyShellExt;
#endif
#endif /* __PyShellExtLib_LIBRARY_DEFINED__ */

/* Additional Prototypes for ALL interfaces */

/* end of Additional Prototypes */

#ifdef __cplusplus
}
#endif

#endif


