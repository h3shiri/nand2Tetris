@R15  // Acting as the quotient in our algorithm.
M = 0 // Setting R15 to be the result initiated with zero.
@14   // Assuming the first bit is ignored due to signed coding.
D = A
@i
M = D // i = 14 , assuming the numbers are signed somehow.
@RE // Remainder for the long devision algorithm.
M = 0  // Reminder = 0
@16384 // We assume bumbers are coded as signed and thus thirst bit is ignored.
D = A 
@MASK
M = D // MASK = 16384 or in binary (0100 0000 0000 0000).
(FIXED_LOOP)
	@RE
	M = M<< // shifting the remainder the left.
	//checking the i bit of R13
	@R13
	D = M // D = R13
	@MASK // M = appropriate power of 2
	D = D & M // D currently holds the flag, whether the i bit is on.
	@SKIP_ADDITION
	D;JLE
	@RE 	  // M = RE
	M = M + 1 // turning on the first bit (it was zero due to the previous step shifting)

	(SKIP_ADDITION)
	@RE
	D = M // D = RE
	@R14 //
	D = D - M // D = RE - divisor
	@INDEX_DECREASE
	D;JLT // Condition for modifying Q and R
	@RE
	M = D // RE = RE - divisor (namely R14)
	@R15 // Acting as Q
	D = M // D = Q
	@MASK
	D = D | M // Q(i) is set to 1
	@R15
	M = D // Now our quotient has been modified appropriately.
	(INDEX_DECREASE)
	@i
	M = M - 1
	@MASK
	M = M>> // shifting the mask to the right, focus on the next bit.
	@i
	D = M // D = i
	@FIXED_LOOP 
	D;JGE

	@END
	0;JMP

(END)
//possible exit scenario.
