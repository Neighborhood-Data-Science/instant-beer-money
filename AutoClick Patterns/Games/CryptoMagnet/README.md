# Thanks for visisting the Neighborhood!

## Game Guide for CryptoMagnet

Please download the above zip file and upload to Smart AutoClicker.

_DISCLAIMER: This AutoClick pattern was programmed on a Google Pixel 6.
Therefore, the location of the images may not be in the same location. 
Ensure that you go through the scenarios below by hand at least once before activating the AutoClicker._

## Scenario Walkthrough

Scenarios are based on what is currently seen on your devices screen. Therefore, you can make decisions based on certain things that are present (or not) on your screen. 

Scenarios are executed from top to bottom. In this way, they act as logic gates based on what is currently seen on the screen.

Our goal in CryptoMagent is to reach 10,000 (10K) meters.
However, once you reach a certain depth, it will cost you billions of dollars to pay for one depth upgrade.

**Our advantage is that we can watch ads to gain a free depth upgrade.**

### Here are our scenarios:

---

#### 1. Ad for Depth
    If an 'AD' button appears on the depth upgrade, click on the button to watch an ad.

#### 2. No Revive
    If you 'fail' and the 'Revive' prompt appears, click outside the prompt to continue the game

#### 3. Continue game
    If there is no Ad for Depth, continue playing the game.

#### 4. Close Ads
    If we are watching an ad, attempt to close the ad once the timer has expired.

#### 5. Resume Video
    If we attempt to close an ad and are met with a 'Resume or Skip' prompt:
        1. Resume the video 
        2. Wait 15 seconds before trying to close the ad again.

FlowChart:
```mermaid
graph TD;
    A[Start Clicker]-->|Watching Screen|B(Ad for Depth?);
    B-->C(Yes);
    B-->D(No);
    C-->|Click on 'AD' button|E(Watch Ad);
    E-->|Watching Ad|F(Close Ad);
    F-->I{Did Ad Close?};
    I-->K(No);
    I-->|Yes|B(Ad for Depth?);
    K-->P{Google prompt?};
    P-->|No|S(Wait);
    P-->|Yes|Q(Click Resume)-->R(Wait 15s);
    R-->F(Close Ad);
    D-->G(Continue Game);
    G-->L{Game Over?};
    L-->M(Yes);
    M-->N{Revive Prompt?};
    N-->|Yes|O(Click outside prompt);
    N-->|No|T(Click 'Claim' or 'No thanks' to continue.);
    O-->|Wait|T(Click 'Claim' or 'No thanks' to continue.);
    O-->B(Ad for Depth?);
    T-->B(Ad for Depth?);
    
    ```
