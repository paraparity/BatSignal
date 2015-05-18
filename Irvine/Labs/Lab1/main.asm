INCLUDE Irvine32.inc

.data
filename byte   "input.txt", 0
written  dword  0
message  byte   256 dup(0)
len      dword  0
capacity dword  256

file     handle ?
stdout   handle ?

FILE_OPEN_ERROR byte "Error - Failed to open input file.", 0dh, 0ah, 0
FILE_READ_ERROR byte "Error - Failed to read input file.", 0dh, 0ah, 0

.code
sort proc
sort endp

main proc
    ; open input file
    mov edx, offset filename
    call OpenInputFile
    mov file, eax

    cmp eax, INVALID_HANDLE_VALUE
    jne file_opened
    mov edx, offset FILE_OPEN_ERROR
    call WriteString
    jmp quit

file_opened:
    ; read input file into string
    mov edx, offset message
    mov ecx, capacity
    invoke ReadFromFile

    jnc file_read
    mov edx, offset FILE_READ_ERROR
    call WriteString
    jmp quit

file_read:
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

quit:
    invoke ExitProcess, 0
main endp
end main