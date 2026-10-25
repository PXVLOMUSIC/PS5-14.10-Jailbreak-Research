// Offset template for PS5 firmware 14.10
// TODO: Populate with measurements from hardware
// Structure based on offsets/13.60.js

const OFFSET_wk_host_constructor_candidates = [];
const OFFSET_wk_vtable_first_element     = 0;
const OFFSET_wk_memset_import                  = 0;
const OFFSET_wk___stack_chk_guard_import       = 0;

const OFFSET_lk___stack_chk_guard              = 0;
const OFFSET_lk__thread_list                   = 0;
const OFFSET_lk_worker_wait_return             = 0;
const OFFSET_lk_pthread_create_name_np         = 0;
const OFFSET_lk_pthread_join                   = 0;
const OFFSET_lk_pthread_exit                   = 0;
const OFFSET_lk_sleep                          = 0;
const OFFSET_lk_sceKernelGetCurrentCpu         = 0;

const OFFSET_lc_memset                         = 0;
const OFFSET_lc_setjmp                         = 0;
const OFFSET_lc_longjmp                        = 0;

const OFFSET_WORKER_STACK_OFFSET         = 0;

let wk_gadgetmap = {
};

let syscall_map = {
};

const OFFSET_KERNEL_ALLPROC                    = 0;
const OFFSET_KERNEL_SECURITY_FLAGS             = 0;
const OFFSET_KERNEL_TARGETID                   = 0;
const OFFSET_KERNEL_QA_FLAGS                   = 0;
const OFFSET_KERNEL_UTOKEN_FLAGS               = 0;
const OFFSET_KERNEL_ROOTVNODE                  = 0;
const OFFSET_KERNEL_VMSPACE_P_ROOT             = 0;
const OFFSET_KERNEL_VMSPACE_VM_PMAP            = 0;
const OFFSET_KERNEL_DATA                       = 0;
const OFFSET_KERNEL_EVF_STR                    = 0;

window.KRW = {
    firmware: "14.10",
    kernelData: 0,
    allproc:    0,
    rootvnode:  0,
    kaslr: { mode: "unknown", retStatic: 0, retLow16: 0 },
    oid: {},
    walkCounter: { addr: 0, mib: [] },
    nodeMutex: 0,
    rodataProbe: { rva: 0, text: "" },
    aio: {},
    proc: {},
    kernelPid: 0,
    ucred: {},
    sysCoreAuthId: { lo: 0, hi: 0 },
    filedesc: {},
    filedescTable: {},
    pipe: {},
    dynlib: {},
};

window.SYMBOLS = {
    libkernel: {},
    libc: {},
};

// WebKit/Canvas specific (from source analysis)
// sizeof(CanvasRenderingContext2D) = 712 (mja00, x86-64 GTK build of WK-1400)
// m_canvas offset in CanvasRenderingContext = +0x20 (mja00)
// CanvasBase refCanvasBase/derefCanvasBase = vtable slots 4/5 (source confirmed)
// IsoHeap OFF: WTF_MAKE_ISO_ALLOCATED -> WTF_MAKE_FAST_ALLOCATED (source confirmed)
// Gigacage: need to verify ENABLE_GIGACAGE in PS5 config
// JSC Config: need to verify startOfStructureHeap writability
PY