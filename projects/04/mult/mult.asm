// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@R2 // This address will accumulate the result
M = 0 
@R0 // Stores RAM[1] inside D so we can use that number as a counter
D = M 
@COUNTER
M = D

(LOOP) // This loop will accumulate R1 to RESULT R0 Times
@COUNTER
D = M
@END
D;JEQ // If counter is 0 then we can go to end
@R1
D = M
@R2
M = M + D
@COUNTER
M = M - 1
@LOOP
0;JMP

(END)
0;JMP