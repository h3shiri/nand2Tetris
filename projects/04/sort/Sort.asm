@R15
D = M
@OUTER_COUNTER
M = D
(OUTER_LOOP)	
	@R15
	D = M
	@INNER_COUNTER
	M = D - 1 
	@R14 //Make POSITION hold the begin address of the array
	D = M
	@POSITION
	M = D
	@OUTER_COUNTER
	M = M - 1
	D = M
	@END
	D;JEQ
	@INNER_LOOP
	D;JNE
	
(INNER_LOOP)
	@POSITION
	A = M
	D = M //D is now array[i]
	A = A + 1 //M is now array[i+1]
	D = D - M; //So now if D is positive we need to swap them
	@SWAP
	D;JGT
	@POSITION
	M = M + 1 //Move to the next value
	@INNER_COUNTER //Check if we should finish the inner loop
	M = M - 1
	D = M
	@OUTER_LOOP
	D;JEQ
	@INNER_LOOP
	D;JNE
(SWAP)
	@POSITION
	A = M
	D = M
	@TEMP
	A = M
	M = D
	@POSITION
	A = M
	A = A + 1
	D = M
	@POSITION
	A = M
	M = D
	@TEMP
	A = M
	D = M
	@POSITION
	A = M
	A = A + 1
	M = D
	@INNER_LOOP
	0;JMP	
(END)
0;JEQ