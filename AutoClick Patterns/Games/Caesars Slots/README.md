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

![alt text](https://latex.codecogs.com/png.latex?%5Cdpi%7B150%7D%20%5Cbg_white%20%5Cpagecolor%7Bwhite%7D%20f%28x%29%20%3D%20%5Csum_%7Bj%3D1%7D%5E%7Bx%7D%20LevelReached_%7Bj-1%7D%20&plus;%20%5Cbegin%7Bcases%7D%201%2C%20%26%20%5Ctext%7Bif%20%7D%20%5Cfrac%7B%28BetSize%20%5Ctimes%20XPBonus%29%7D%7BNextLevelXP_j%7D%20%5Cge%201%20%5C%5C0%2C%20%26%20%5Ctext%7Botherwise%7D%5Cend%7Bcases%7D%2C%20%5Cquad%20x%20%5Cin%20%5Cmathbb%7BN%7D_%7B%3E0%7D)<br><br>

The first statement defines $Level_i$ to be equal to $i$ such that when $i$ is computed as $g(f(x))$, it equals $x$. In other words, the recursive function $g(x)$ is used to determine the correct input value of $x$ such that $Level_i$ is equal to $i$.<br>

The second statement defines the recursive function $g(x)$ that outputs either $x$ if $f(x)$ equals $x$, or recursively calls itself with $f(x)$ as the input until $f(x) = x$.<br>

The final statement is a formula for determining if the player has reached the next level by obtaining the appropriate experience points (XP), denoted by $f(x)$. The formula is defined by a summation of the levels reached up to $x$, plus a bonus of $1$ if the ratio of the bet size and the XP bonus to the XP required for the next level is greater than or equal to $1$ (i.e., $\frac{(BetSize \times XPBonus)}{NextLevelXP_j} \ge 1$), and $0$ otherwise.<br><br>

_Note that_ $NextLevelXP_j$ _is calculated within Caesars Slots._<br><br>

To my knowledge, there is no current table that contains the XP required to reach the next level.<br><br>

### **Our advantage is that we can auto spin slots and automatically play bonus games if necessary.**

In summary, our bot will play a selected slot game (Wild Howl or Wild Howl Deluxe), participate in bonus game (Nevada Snaps), and close necessary windows to continue playing the game.

### Here are our scenarios:

---

#### 1. Ad for Depth
    If an 'AD' button appears on the depth upgrade, click on the button to watch an ad.

#### 2. No Revive
    If you 'fail' and the 'Revive' prompt appears, click outside the prompt to continue the game.

#### 3. Claim or No Thanks
    If there is a prompt to click 'Claim' or 'No Thanks', click the prompt. 
    
#### 4. Continue game
    If there is no Ad for Depth, continue playing the game.

#### 5. Resume Video
    If we attempt to close an ad and are met with a 'Resume or Skip' prompt:
        1. Resume the video.
        2. Wait 15 seconds before trying to close the ad again.

#### 6. Close Ads
    If we are watching an ad, attempt to close the ad once the timer has expired.

#### 7. Exit Store
    If our bot attempts to close ad and it opens the app store instead:
        1. Press back button to return to app store main screen.
        2. Swipe left-to-right on screen to return to the ad before trying to close the ad again.

#### Flowchart:
```mermaid
graph TD;
    A[Start Clicker]-->|Watching Screen|B{Ad for Depth?};
    B-->|Yes|C{{Watch Ad}};
    B-->|No|D[[Continue Game]];
    C-->|Wait until complete|E[[Close Ads]]
    E-->F{Did Ad Close?};
    F-->|No|G{Google prompt?};
    F-->|Yes|B{Ad for Depth?};
    H-->E[[Close Ads]];
    G-->|No|J{In App Store?};
    G-->|Yes|H[[Resume Video]];
    J-->|No|P{{Update Scenario}};
    J-->|Yes|O[[Exit Store]];
    O-->E;
    D-->K{Game Over?};
    K-->|Yes|L{Revive Prompt?};
    K-->|No|D;
    L-->|No|M;
    L-->|Yes|N[[No Revive]];
    N-->M[[Claim or No Thanks]];
    M-->B;
```
Please add additional screenshots and scenarios as needed. For example, the 'Close Ads' scenario will need to be updated as new ads are introduced to the game.

We did our best to capture various ad exit symbols but add more as you monitor the AutoClicker.

**Please monitor your AutoClicker.** There may be unexpected results if left unattended for long periods. 
