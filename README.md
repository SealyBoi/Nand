This whole project was based off of https://nandgame.com and their step-by-step introduction to nand.
This took a lot of time and effort but in the end was a worth while experience. I can't say I've seen
this anywhere else, so enjoy the pleasure of staring at something that should never have been made in
the first place.

If you would like to run it, I am using Python 3.12. I don't believe any outside
packages are required, so it should run easily on any Python version (unless there are compilation
changes of course).

Do note that since this is written in Python, it is pretty slow for a "Processor". It takes its time
performing work that should be done on hardware, not software. This is just a simulation OF that
software. You can change up the instructions as you please to watch it run. It understands a
16-bit instruction set that I have left below. Enjoy!

Basic chart of instructions
ci | - | - | * | - | u | op1 | op0 | zx | sw | a | d | *a | lt | eq | gt | decimal | hex | assembler
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0000 | A = 0

As long as ci is not 1, it is considered an assignment to A
ci | - | - | * | - | u | op1 | op0 | zx | sw | a | d | *a | lt | eq | gt | decimal | hex | assembler
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 9232 | 2410 | A = 9232

After flipping ci, you can do a lot more.
ci | - | - | * | - | u | op1 | op0 | zx | sw | a | d | *a | lt | eq | gt | decimal | hex | assembler
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 32768 | 8000 | D&A

When u is 0, op1 and op0 are 'and' and 'or' operations respectively.
ci | - | - | * | - | u | op1 | op0 | zx | sw | a | d | *a | lt | eq | gt | decimal | hex | assembler
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 33280 | 8200 | D^A
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 32768 | 8000 | D|A

When u is 1, the default operation is 'D+A'. op1 becomes 'subtraction' while op0 becomes 'replace right with 1'
ci | - | - | * | - | u | op1 | op0 | zx | sw | a | d | *a | lt | eq | gt | decimal | hex | assembler
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 34304 | 8600 | D-A
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 34048 | 8500 | D+1

Changing a, d, or *a to 1 will assign the current equation to that value. i.e. A = D+A

Changing lt, eq, gt to 1 will create a jump. i.e. A; JEQ
