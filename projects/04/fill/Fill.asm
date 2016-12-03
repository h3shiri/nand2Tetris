// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(START)
	@WHITE //initialize colors
	M = 0
	@BLACK
	M = -1
	@SCREEN
	D = A
	@8192 //set marker to ammount of end of screen
	D = D + A
	@MARKER
	M = D
	@8192 // set counter to have the ammount of registers in the screen
	D = A
	@COUNTER
	M = D
	
	@KBD //check keyboard activity and act accordingly
	D = M
	@WHITE
	D;JEQ
	@BLACK
	D;JNE

(BLACK)
	@BLACK
	D = M
	@MARKER
	A = M
	M = D
	@MARKER
	M = M - 1
	@COUNTER
	M = M -1
	D = M
	@START
	D;JEQ
	@BLACK
	D;JNE

(WHITE)
	@WHITE
	D = M
	@MARKER
	A = M
	M = D
	@MARKER
	M = M - 1
	@COUNTER
	M = M -1
	D = M
	@START
	D;JEQ
	@WHITE
	D;JNE
