# Simple Hamming

    ----------------------------------------
    |                                      |
    |            Simple Hamming            |
    |                                      |
    |            by LC (or ZHZ)            |
    |             zhang_hz@pku.edu.cn      |
    |                                      |
    ----------------------------------------
This is a simple demo program to demonstrate Hamming coding system. You can perform encoding, decoding and correctness checking on code sequences by calling this program.

## License

MIT LICENSE.

## Hamming Code

Denote a bit sequence as $(x_1x_2x_3\cdots x_n)_2$, where $x_i=0, 1,\ i=1,2,3,\cdots$. When the sequence is filled with data, meaning $x_1\sim x_n$ are all "data bits", there is no chance for the target to determine whether the message sequence it received is correct or wrong.

**Parity code** provides the ability to check correctness. We insert one bit (denoted as $p$) into the sequence every $k$ bits. The sequence becomes $x_1x_2x_3\cdots x_kp_1x_{k+1}x_{k+2}\cdots x_{2k}p_2\cdots$. When $1$ appears odd times in subsequence $x_{ik+1}x_{ik+2}\cdots x_{ik+k}$, place a $0$ on $p_{i+1}$, otherwise a $1$. Such coding is called **odd-parity checking**. The **even-parity checking** follows the same rule.

````
x1 x2 x3 x4 x5 x6 x7 p1 parity
0  1  1  0  1  0  1  0  even
0  1  1  0  1  0  1  1  odd
````

Parity code can only detect 1, 3, 5, etc. wrong bits in a sequence, and cannot help correct the wrong sequence. **Hamming code** has such ability! It can detect and correct 1 wrong bit. The code sequence is something like $p_1p_2x_3p_4x_5\cdots x_7p_8x_9\cdots x_{15}p_{16}x_{17}\cdots p_{2^i}x_{2^i+1}\cdots x_{2^{i+1}-1}p_{2^{i+1}}\cdots$, where $p_i,\ i=1,2,4,\cdots,2^j,\cdots, \ j=0,1,2,\cdots$ are the parity checking bits, and other $x_m$ are the data bits.

$p_{2^i}$ is the parity checking bit for the subsequence which contains all the bits which has a $1$ instead of $0$ on the $i$-th bit of their position index. One major hypothesis is that there is not likely to be more than one wrong bit in a single sequence. When finding any wrong subsequences, suppose the corresponding checking bits are $p_{2^{i_1}}, p_{2^{i_2}},\cdots$, then the wrong bit's position index is $\sum_{k}i_k$. An example is as below.

````
index		1 2 3 4 5 6 7 8 9 101112

Data bits	- - 0 - 1 0 1 - 1 1 0 0
P1-subseq	1 - 0 - 1 - 1 - 1 - 0 -	 P1=1
P2-subseq	- 0 0 - - 0 1 - - 1 0 -  P2=0
P4-subseq	- - - 0 1 0 1 - - - - 0  P4=0
P8-subseq	- - - - - - - 0 1 1 0 0  P8=0
Encoded		1 0 0 0 1 0 1 0 1 1 0 0  (Even-parity)

Wrong seq	1 0 1 0 1 0 1 0 1 1 0 0  (Even-parity)
P1-subseq	1 - 1 - 1 - 1 - 1 - 0 -	 wrong subsequence
P2-subseq	- 0 1 - - 0 1 - - 1 0 -  wrong subsequence
P4-subseq	- - - 0 1 0 1 - - - - 0  
P8-subseq	- - - - - - - 0 1 1 0 0  
wrong bit index = 1 + 2 = 3
Corrected	1 0 0 0 1 0 1 0 1 1 0 0 
````

## How2Use

The file `hamming.py` contains all hamming code operations, and they are already encapsulated. The file `main.py` is the main entrance of this program.

Call `python main.py -h` for help. Detailed parameter descriptions are included.

## Example

````
> python main.py -D AAC -B -E

Wrong bit at 2.

Enc     1 0 1 0 1 0 1 0 1 1 0 0

WBit        V      
P1      1 - 1 - 1 - 1 - 1 - 0 -   Wrong bit appear
P2      - 0 1 - - 0 1 - - 1 0 -   Wrong bit appear
P4      - - - 0 1 0 1 - - - - 0   
P8      - - - - - - - 0 1 1 0 0   

Correct 1 0 0 0 1 0 1 0 1 1 0 0 
Dec     - - 0 - 1 0 1 - 1 1 0 0 
````

