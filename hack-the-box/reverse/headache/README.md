# Headache (actually)

## Initial Execution

First things first, the challenge provides us with a single UNIX executable. Let's try and run it to see the output...

![Initial run](img/run1.png)

Looks like it requires a key input, lets provide something random...

![Second run](img/run2.png)

It appears that it has some kind of login system. Our initial thought will be that we are required to reverse the key in order to login. So let's get started!

## Disassembling

Opening the file in IDA, we can instantly tell it's a [stripped binary](https://en.wikipedia.org/wiki/Stripped_binary) as we see no trace of any functions, so let's start discovering some of them.

First things first, let's do a string search. Maybe that would point us to the main function or some other kind of clue?

![Second run](img/strings.png)

Along with a lot of random strings, we see some known strings from our first executions, such as:

* Initialising
* Enter the key:
* Login Failed!
* Login success!

We also see a blatantly fake flag, HTB{not_so_easy_lol}, let's assume and hope that's not the flag.
