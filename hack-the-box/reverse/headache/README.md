# Headache (actually)

This is a decently detailed walkthrough so make sure to set back, relax and grab yourself some coffee (or tea, I don't judge)

## Initial Execution

First things first, the challenge provides us with a single UNIX executable. Let's try and run it to see the output...

![Initial run](img/run1.png)

Looks like it requires a key input, lets provide something random...

![Second run](img/run2.png)

It appears that it has some kind of login system. Our initial thought will be that we are required to reverse the key in order to login. So let's get started!

## Disassembling

Opening the file in IDA, we can instantly tell it's a [stripped binary](https://en.wikipedia.org/wiki/Stripped_binary) as we see no trace of any functions, so let's start discovering some of them.

First things first, let's do a string search(Shift + F12). Maybe that would point us to the main function or some other kind of clue?

![Strings](img/strings.png)

Along with a lot of random strings, we see some known strings from our first executions, such as:

* Initialising
* Enter the key:
* Login Failed!
* Login success!

We also see a blatantly fake flag, HTB{not_so_easy_lol}, let's assume and hope that's not the flag.

However, we can't yet XREF the strings to instantly find our function. As we can see, the strings belong to a LOAD:xx segment, which means its a not-yet-named ELF segment loaded from IDA, we know nothing about it yet.

Our only solution at this point is to debug step into main. Let's set a breakpoint in init_proc and slowly make our way into the program.

![Init proc](img/initprocbp.png)

We keep F8'ing and we reach the following function that does some yet unknown stuff. Let's give it a name, say "Entry" and disassemble into pseudocode.

![Init proc](img/entry1.png)

Right off the bat we see a couple of sketchy stuff.

1. A system call to 0x64, which corresponds to ptrace
2. A string ```a15abe90c112d09369d9f9da9a8c046e``` that looks nothing that we know of yet, but seems to be used as input to some function

The next thing we see is what appears to be a hardcoded condition. v3 appears to be the result of ptrace, and it's set to 101, followed by an if statement which will always succeed and call ```sub_55FF898683C1```. Stepping into ```sub_55FF898683C1``` we can see that it's blatantly our main processing function that contains the input and it's processing. Let's call it main for now.

![Init proc](img/main.png)

tbc...
