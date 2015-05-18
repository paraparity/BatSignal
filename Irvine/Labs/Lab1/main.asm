INCLUDE Irvine32.inc

.data
filename byte  "input.txt", 0
written  dword 0
message  byte  256 dup(0)
numbers  dword 256 dup(?)
capacity dword 256
index    dword ?
saved    dword ?
len      dword ?

file     handle ?
stdout   handle ?

FILE_OPEN_ERROR   byte "Error - Failed to open input file.", 0dh, 0ah, 0
FILE_READ_ERROR   byte "Error - Failed to read input file.", 0dh, 0ah, 0
FILE_CREATE_ERROR byte "Error - Failed to create input file.", 0dh, 0ah, 0

.code
sort proc
sort endp

; @registers
;   eax: start index
;   ebx: end index
;   edx: string offset
; @return: integer value of string
atoi proc
    push ebp
    mov ebp, esp
    sub esp, 12
    mov [ebp - 4], eax  ; local storage of start
    mov [ebp - 8], ebx  ; local storage of end
    mov [ebp - 12], edx ; local storage of string offset

    mov eax, 0   ; accumulator for integer value
    mov ecx, ebx ; current index between start and end

atoi_loop:
    mov ebx, [ebp - 12]
    add ebx, ecx
    mov edx, [ebx]

    dec ecx
    cmp ecx, [ebp - 8]
    jne atoi_loop

    pop ebp
atoi endp

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
    call ReadFromFile

    jnc file_read
    mov edx, offset FILE_READ_ERROR
    call WriteString
    jmp quit

file_read:
    ; write contents of input file to console
    mov edx, offset message
    call WriteString

    ; parse through input
    mov index, 0
    mov saved, 0
parse_loop:
    mov ebx, offset message
    add ebx, index
    mov eax, [ebx]
    cmp eax, " "
    jne end_parse_loop
    mov eax, saved
    mov ebx, index
    mov edx, offset message
    call atoi
    mov ebx, index
    mov saved, ebx

end_parse_loop:
    inc index
    mov ebx, offset message
    add ebx, index
    mov eax, [ebx]
    cmp eax, 0
    jne parse_loop

    ; insert sorting here

    ; write sorted input to console
    mov edx, offset message
    call WriteString

    ; close input file
    mov eax, file
    call CloseFile

quit:
    invoke ExitProcess, 0
main endp
end main