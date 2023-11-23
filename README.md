# Sudoku Solver With Statistics
### Video Demo:  [Link to the video](<https://youtu.be/Rp9DP0_PK_Q>)
## Description:

This program is devoted to three main concepts, some of them related to programming,
other just things I like to. It achieves set goals using sudoku puzzles.

#### KNOWN ISSUES:
When the code starts for the first time in hangs for a brief moment. It probably happens because numpy is initialized. So keep that in mind while using. Any usage after the initialization if fast as it should be. If anyone know how to mitigate this, please write to me.

### **_Main concepts:_**
1.  My love to **data**, especially their collection and preservation. It's kinda what I do in everyday
professional life, where me and my team gather data related to our competition's activity
in the advertisement space. This concept is achieved by:
    * Data collection -> some parts of my code gather data for validation, manipulation and
    preservation in various ways, for further eyeballing and analysis 🙂
    * Data preservation -> is done in two ways, writing solutions and other data to file,
    and collecting stats for each of these processes including:
      * date,
      * time,
      * numbers of operations
      * successes
      * see the rest by yourselves 😃
    * Data presentation -> this is done by simple tables due to the way the proigram was designed.
    I wanted it to be a CLI and as such the only way to communicate is via the terminal window.
2.  Learning new things which I did not know how to do, and which I wanted to learn more.
Those things were:
    * **Recursion** -> Well it still gives me some trouble, but I guess the general idea is understandable.
    One of the easiest ways to solve a Sudoku puzzle is **recursion**, so it seemed the natural way
    of things.
    * **Backtracking** -> There is no recursion without backtracking in a puzzle like this. Besides
    this concept is also pretty useful in other algorithms which I intend to learn more about after
    completing this course.
    * **Databases** and **SQL** -> beforehand I didn't know anything about those things,
    but as it turned out it's not a such difficult thing. **SQLite3** built in Python itself is perfect
    for my needs, and online sources of knowledge on the topic of **SQL**. I probably know nothing yet,
    but it's enough to make the job done.
    * **Program states** -> like built in menus which let the user navigate through it and perform
    various activities. Achieving this was possible thanks to **while loops** and **match case**
    statements. Next step to get more experience and know how to properly use this concept is
    probably make something in Pygame.
3. Applying new things I've learned from the lectures and solving problem sets.
   * Reading and writing to csv by using **_csv_ module**.
   * Validating things using regex and built in **_re_ module**.
   * **_Reusing code_** written earlier, any applying it to my new needs. It's nice to copy-paste and adjust, or simply use lines.py to count how much you have written 🙂
   * **Typehint**.
   * **Docstrings**.
   * Using modules which other people wrote. Here good examples are DLXSudoku and Tabulate.
   * **Comprehensions** - lists and dicts comprehensions were used.


### **Program construction:**

1. Program uses **CLI** to communicate with the user and to output information.
2. Use CLI **arguments** to communicate what you want to do:
   * args [-h] [-m M] [-f FN] [-s] [-c] [-st] [-p | -tf | -t]
   * [-f FN] [-st] <- One of these two is a must.
3. Program is divided into two main blocks. Statistics and solving.
   * Statistics have built in menu for navigation and performing given tasks.
   * Solving - solves provided puzzles and outputs solutions in one of two ways
     * To screen -> if you have a couple of puzzles you can see the results
     * To file -> if the numbers are great, this is the desired way of the output.
4. Flags:
   * **[-m M]** >>> solver method:
     * Recursion & backtracking.
     * Recursion, backtracking and checking for valid and most probable values for given grid field.
     * Dlxsudoku
     * Random Walk... Use only for very little number of puzzles. Preferably one set.
     * Cake Algorithm
   * **[-f FN]** >>> filename or filepath to the data. File should be a *.csv or *.txt file containing
   puzzles or puzzles and sample solutions for further comparison. Each row is separated puzzle or
   puzzle/solution set.
   * **[-s]** >>> used when your file contains solutions to the puzzles.
   * **[-c]** >>> comparison option if your data contains solutions to compare to.
   * **[-p | -tf | -t]** >>> ways of presentation the data:
     * _-p_ >>> to screen
     * _-tf_ >>> write to file
     * _-t_ >>> test pipeline designed to compare each solve method and pass in clean environment.
     No output other dan comparison statistics.
   * use -h or --help for more information.
5. Program should throw nice and understandable error messages when the user messes something up.
in case something not working or when bugs are found please contact me a t the email shown in the help.
6. Navigation in statistics is achieved by "0-5", "B", "Y", "N". Inputs are treated key insensitively.
7. Program uses SQLIte3, and creates DB file called **"stats.db"** inside which it creates
**"statistics"** table. When DB dump is selected program creates **"dbdump.csv"** file.
8. When writing solutions to file, one named **"results.csv"** is created.
9. Tests are provided in **"test_project.py"** where several functions are tested.
   * **Deleting** of database entries is available. The user can delete entries or drop the whole DB.
   * **Dumping** the DB contents into a *.csv file is available, i.e. for further data manipulation in
   external software.



### **Dependencies:**

This proigram needs some external libraries to wor properly.
Use <ins>**pip install**</ins>:
*  dlxsudoku
*  argparse
*  datetime
*  tabulate
*  random
*  numpy
*  typing
*  sqlite3
*  tqdm
*  time
*  csv
*  sys
*  os
*  re



### **Usage:**
1. Type <ins>**python project.py -h_**</ins> for detailed instruction.
2. Type <ins>**python project.py -f sudoku.txt -tf**</ins> for solving and writing results to file.
3. Type <ins>**python project.py -f sudoku.csv -tf -s -c**</ins> for solving and comparing results to provided solutions.
4. Type <ins>**python project.py -f sudoku.csv -t -s -m 2**</ins> for solving using second method and using test pipeline
5. Type <ins>**python project.py -st**</ins> for use built in menu system and see stats of conducted runs.

<br>

#### Example of output:

**To screen:**

PUZZLE <br>
['5' '0' '2' '0' '0' '7' '0' '3' '0'] <br>
['0' '6' '3' '0' '0' '2' '0' '7' '0'] <br>
['0' '8' '4' '9' '1' '0' '0' '0' '0'] <br>
['1' '2' '0' '0' '0' '0' '0' '0' '0'] <br>
['0' '3' '0' '2' '6' '4' '7' '1' '5'] <br>
['4' '0' '0' '5' '0' '1' '0' '0' '0'] <br>
['0' '0' '1' '0' '3' '0' '0' '9' '0'] <br>
['3' '4' '0' '0' '9' '0' '0' '0' '0'] <br>
['0' '0' '0' '0' '0' '0' '0' '8' '1'] <br>
 <br>
SOLUTION <br>
['5' '1' '2' '6' '4' '7' '8' '3' '9'] <br>
['9' '6' '3' '8' '5' '2' '1' '7' '4'] <br>
['7' '8' '4' '9' '1' '3' '5' '6' '2'] <br>
['1' '2' '5' '3' '7' '9' '6' '4' '8'] <br>
['8' '3' '9' '2' '6' '4' '7' '1' '5'] <br>
['4' '7' '6' '5' '8' '1' '9' '2' '3'] <br>
['2' '5' '1' '7' '3' '8' '4' '9' '6'] <br>
['3' '4' '8' '1' '9' '6' '2' '5' '7'] <br>
['6' '9' '7' '4' '2' '5' '3' '8' '1'] <br>

<br>

**To file:**

Testing...: 100%|██████████████████████████| 6200/6200 [00:00<00:00, 9222.66it/s]
<br>
Method of presentation: to file<br>
Solve method name: Cake algorithm<br>
Test date: 2023-10-08<br>
Test start time: 22:45:04<br>
Test duration time: 0.6804807186126709<br>
Puzzles read: 6200<br>
Solutions found: 6200<br>
Avg. solve time: 0.00010975495461494693<br>
<br>
Program has ended.<br>

<br>

#### Special Thanks to Ducky! You are the best! ❤️ 🦆
#### Also a big Thank You to David Malan and his Team for making CS50P. 👨‍🏫
#### And one goes to Cisco Networking Academy for the kickoff my learning path. 👍

Contact me at pokeplacek@gmail.com
