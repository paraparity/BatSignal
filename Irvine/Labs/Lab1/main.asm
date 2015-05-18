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
ENDL              byte 0dh, 0ah, 0
SPACE             byte " ", 0

.code

; @registers
;   eax: lower limit within buffer
;	ebx: upper limit within buffer
;	ecx: length of the buffer segment
;   edx: buffer of integers
; @return: sorted array
;quicksort proc
;	push eax
;	sub eax, ebx
;	cmp eax
;	jge quit
;
;	push ebx
;	push ecx
;	push edx
;
;	call partition
;	
;	call quicksort
;
;	call quicksort
;
;quit:
;quicksort endp

; @registers
;   eax: lower limit within buffer
;	ebx: upper limit within buffer
;	ecx: length of the buffer segment
;   edx: buffer of integers
; @return: sorted array
;partition proc
;	xor esi, esi
;	xor edi, edi
;	shr eax, 1	; Divide by 2 for naive pivot
;	push eax
;
;sort:
;	lower:
;		mov eax, [esi]
;		cmp 
;	upper:
;		
;		cmp 
;
;	cmp esi, edi
;	jge sort	
;
;	cmp ; i < j
;	jge quit

;quit
;	pop eax
;partition endp

; @registers
;   eax: start index
;   ebx: end index
;   edx: string offset
; @return: integer value of string
atoi proc start_index:dword, end_index:dword, string_offset:dword
    mov eax, 0   ; accumulator for integer value
    mov ecx, end_index ; current index between start and end
    dec ecx

atoi_loop:
    mov edx, string_offset
    mov ebx, 0
    mov bl, [edx + ecx]
    sub ebx, 30h

    push eax ; accumulator value
    push ebx ; integer value of current character

    mov eax, end_index
    dec eax
    sub eax, ecx

    ; multiply by ten
    mov ebx, 10
    mul ebx
    cmp eax, 0
    jne skip_location
    mov eax, 1 ; this fixes issues with the ones place
    call DumpRegs

skip_location:
    ; eax * ebx = value of character based upon location in string
    pop ebx
    mul ebx
    mov ebx, eax

    ; add character value to accumulator
    pop eax
    add eax, ebx
    push eax

    dec ecx
    cmp ecx, start_index
    jne atoi_loop

    pop eax
    ret
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
    mov edx, offset ENDL
    call WriteString

    mov index, 0
    mov saved, -1
    mov len, 0

    ; parse through input
parse_loop:
    mov edx, offset message
    mov ebx, index
    mov eax, 0
    mov al, [edx + ebx]
    cmp eax, 20h
    jne end_parse_loop
    invoke atoi, saved, index, offset message

    push eax ; value of integer

    ; insert value into numbers array
    mov eax, 4
    mov ebx, len
    mul ebx
    mov ebx, eax

    ; insert value into numbers
    pop eax
    mov edx, offset numbers
    mov [edx + ebx], eax

    ; increase length of numbers
    mov eax, len
    inc eax
    mov len, eax

    ; save index
    mov eax, index
    mov saved, eax

end_parse_loop:
    mov eax, index
    inc eax
    mov index, eax

    mov ebx, offset message
    add ebx, index
    mov eax, [ebx]
    cmp eax, 0
    jne parse_loop

    ; insert sorting here
;	xor eax, eax
;	mov ebx, len
;	mov ecx, ebx
;	mov edx, numbers
;	call quicksort

    mov ecx, 0

    ; write sorted input to console
print_output_loop:
    mov edx, offset numbers
    mov eax, [edx + ecx]
    call WriteInt

    mov edx, offset SPACE
    call WriteString

    inc ecx
    cmp ecx, len
    jne print_output_loop

    mov edx, offset ENDL
    call WriteString

    ; close input file
    mov eax, file
    call CloseFile

quit:
    invoke ExitProcess, 0
main endp
end main