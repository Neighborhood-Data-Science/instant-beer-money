# Thanks for visisting the Neighborhood!

## Game Guide for Caesars Slots

Please download the above zip file and upload to Smart AutoClicker.

Once scenarios are verified, start the script for Caesars Slots.

_DISCLAIMER: This AutoClick pattern was programmed on a **Google Pixel 5**.
Therefore, the location of the images may not be in the same location on your device. 
Ensure that you go through the scenarios below by hand at least once before activating the AutoClicker._

## Scenario Walkthrough

Scenarios are based on what is currently seen on your device's screen. Therefore, you can make decisions based on certain things that are present (or not) on your screen.

Scenarios are executed from top to bottom. In this way, they act as logic gates based on what is currently seen on the screen.

Our goal in Caesars Slots is to reach a specific player level. The only way to reach the next level is to gain XP by playing the game for a set bet amount. The higher your bet amount, the more XP you will earn per spin. 

As such, it is recommended that you bet between 0.5% and 1.5% of your account size at all times:<br>

### $AccountSize \times0.5\\% \le BetSize \le AccountSize \times1.5\\%$<br>

You should also take advantage of the x2, x3, or x4 XP offers available to purchase. This will allow you to reach the next levels faster while still conserving the approriate risk levels.<br><br>

In general:

### $Level_i = i \text{, where } i \in \mathbb{N}_{>0}$, $i=g(f(x))\Rightarrow i=x$<br><br>

![alt text](https://latex.codecogs.com/png.latex?%5Cdpi%7B150%7D%20%5Cbg_white%20%5Cpagecolor%7Bwhite%7D%20g%28x%29%20%3D%20%5Cbegin%7Bcases%7D%20x%2C%20%26%20%5Ctext%7Bif%20%7D%20f%28x%29%3Dx%5C%5Cg%28f%28x%29%29%2C%20%26%20%5Ctext%7Botherwise%7D%5Cend%7Bcases%7D)<br><br>

![alt text](https://user-images.githubusercontent.com/38044300/229407861-4a9ad995-51bc-46f8-b623-f33509c0eed8.gif)<br><br>

### $x,k \in \mathbb{N}_{>0}$

The first statement defines $Level_i$ to be equal to $i$ such that when $i$ is computed as $g(f(x))$, it equals $x$. In other words, the recursive function $g(x)$ is used to determine the correct input value of $x$ such that $Level_i$ is equal to $i$.<br>

The second statement defines the recursive function $g(x)$ that outputs either $x$ if $f(x)$ equals $x$, or recursively calls itself with $f(x)$ as the input until $f(x) = x$.<br>

The final statement is a formula for determining if the player has reached the next level by obtaining the appropriate experience points (XP), denoted by $f(x)$. The formula is defined by a summation of the levels reached up to $x$, plus a bonus of $1$ if the summation of each ratio of  bet size and XP bonus to the XP required for the next level is greater than or equal to $1$ (i.e., $\frac{(BetSize_k \times XPBonus_k)}{NextLevelXP_j} \ge 1$) ,and $0$ otherwise.<br><br>

_Note that_ $NextLevelXP_j$ _is calculated within Caesars Slots._<br><br>

To my knowledge, there is no current table that contains the XP required to reach the next level.<br><br>

### **Our advantage is that we can auto spin slots and automatically play bonus games if necessary.**

In summary, our bot will play a slot game, participate in a bonus game (Nevada Snaps), and close necessary windows to continue playing the slot game.

### Here are our scenarios:

---

#### 1. Start Nevada Snaps
    If the bonus game is playable, start the game.

#### 2. Play Nevada Snaps
    If playing Nevada Snaps:
        1. Click the 'snap' button.
        2. Wait then click the 'collect' button.
        3. Close the menu.

#### 3. Spin and Stop
    If there is no bonus game playable, spin and manually stop the slot machine. 
    
#### 4. Start Mini
    Click the 'Start' prompt to start playing the slot mini game.

#### 5. Continue Game
    Continue playing the game by clicking 'Back to Game' , 'Claim Prize', or 'Collect' prompts.
    
#### 6. Close Menu
    Close any extra menus that pop up while playing or collecting rewards.
    
#### Flowchart:
```mermaid
graph TD;
    A{{Start Clicker}}-->|Watching Screen|B{Bonus Game?};
    B-->|Yes|C[[Start Nevada Snaps]];
    C-->D[[Play Nevada Snaps]];
    B-->|No|E[[Spin and Stop]];
    E-->F{Mini Game?};
    F-->|No|I;
    F-->|Yes|G[[Start Mini]];
    G-->|Finish Mini|H[[Continue Game]];
    H-->I{Random Menu?};
    D-->I;
    
    I-->|No|B;
    I-->|Yes|J[[Close Menu]];
    J-->B;
    
    
```
Please add additional screenshots and scenarios as needed. For example, the 'Close Menu' scenario will need to be updated as new ads are introduced to the game.

We did our best to capture various menu exit symbols but add more as you monitor the AutoClicker.

**Please monitor your AutoClicker.** There may be unexpected results if left unattended for long periods. 
