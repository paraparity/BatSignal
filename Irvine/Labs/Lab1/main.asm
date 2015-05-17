INCLUDE Irvine32.inc

.data
filename byte   "input.txt", 0
written  dword  0
message  byte   256 dup(0)
len      dword  0
capacity dword  256

file     handle ?
stdout   handle ?

.code
sort proc
sort endp

main proc
    ; open input file
    invoke CreateFile,
        addr filename,
        GENERIC_WRITE,
        DO_NOT_SHARE,
        NULL,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        0
    mov file, eax

    ; read input file into string
    mov eax, file
    mov edx, offset message
    mov ecx, capacity
    invoke ReadFromFile

    ; get handle to stdout
    invoke GetStdHandle, STD_OUTPUT_HANDLE
    mov stdout, eax

    ; write contents of input file to stdout
    invoke WriteConsole,
        stdout,
        addr message,
        len,
        addr written,
        0

    ; insert sorting here

    ; write output to std out
    invoke WriteConsole,
        stdout,
        addr message,
        len,
        addr written,
        0

    ; close input file
    mov eax, file
    call CloseFile

    invoke ExitProcess, 0
main endp
end main