# Ccanary

This challenge includes a demonstration of a simple buffer overflow attack, with a little twist.

## Initial Thoughts

Since we are given the source code, let's have a look at it:

![Initial Thoughts](img/initial.png)

We can see that a local struct data is created, containing the user input, followed by a function pointer and then by a variable that will later decide wether or not the flag will be printed. Quite obviously, we need to overwrite that variable to 1.

Let's have a look at the struct to tell what's going on:

![Struct Data](img/struct.png)

We can see that user input is 32 bytes, so we should be able to easily overflow that and reach the variable we want to overflow.

The problem arises at line 44 of main, where the second field of the struct, the function pointer, is called. In a normal call this would just call the canary function and move on, however in the case of an overflow, the address will be overwritten and the garbage in it will act as an address to be called, which will obviously lead in the termination of the program if the address is not correct.
