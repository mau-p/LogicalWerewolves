---
theme: jekyll-theme-cayman
layout: post
usemathjax: true
---
# Logical Werewolves

## The Game
We initialize the game with $x$ werewolves and $y$ villagers, therefore
the total number of agents is $m=x+y$. One villager is set to be the
little girl, who can see the werewolves with a probability $p_{sw}$.
Additionally, every agent $a$ has a reliability score $r_a$. The game
has two phases: the day and night phase. The phases follow each other
consecutively, starting from the night phase. During the night phase the
werewolves kill the villager with the highest reliability score. During
the day phase all agents vote on an agent to vote off. The werewolves
vote for a random villager, while the villagers vote for the agent with
the lowest reliability score. If the little girl saw the werewolves, she
votes for a random werewolf; Otherwise she follows the villager voting
strategy. The game ends when there are no werewolves or no villagers
left. Below we show a flowchart of the game.

| ![flowchart](assets/images/flowchart.png) |
|:--:|
| Figure 1: a flowchart of the game The Werewolves of Millers Hollow |

## Formal model
The formal model of our simulation is as follows:
 - a set of $m$ agents $A =$ \{ $a_1, a_2, ..., a_m$ \}.
 - a set of $x$ werewolves, $W \subset A$, $|W| = x$.
 - a set of $y$ villagers, $V \subset A$, $|V| = y$.
 - a singleton set for the little girl, $L \subset V$, $|L| = 1$.
 - a set of propositions $P =$ \{ $w_1, w_2, ..., w_m, l_1, l_2, ..., l_m$ \}, where:
    - $w_i = t$ iff $a_i \in W$
    - $l_i = t$ iff $a_i \in L$
 - sets $W$ and $V$ are mutually exclusive, $W \cap V = \emptyset$,\
 hence for some $a_i \in A$, iff $w_i = f$ then $a_i \in V$
 - a set of reliability scores $Rs =$ \{ $r_1, r_2, ..., r_m$ \}.

After every phase, the agent $a_i$ that was killed or voted off is removed from $A$.\
Then a truthful public announcement is done about $w_i$ and $l_i$ and the reliablity scores $Rs$ are updated according to $w_i$.\
All $a_j \in A$ that voted to remove $a_i$ get $r_j = r_j + 1$ if $w_j = t$, and $r_j = r_j - 1$ if $w_j = f$.

In all states:
 - every $a_i \in W$ knows $w_j$ for all $a_j \in A$.
 - every $a_i \in L$ knows $l_j$ for all $a_j \in A$.

In at least one state:
 - every $a_i \in L$ knows $w_j$ for all $a_j \in A$.
 - iff not $L=\emptyset$, every $a_i \in W$ considers possible $l_j$ for $a_j \in A$ with $max(Rs)$
 - every $a_i \in V \setminus{L}$ considers possible $w_j$ for $a_j \in A$ with $min(Rs)$

Our Kripke model is defined as follows:
$M ::= \langle S, \pi, R_1, ..., R_m \rangle$, with:\\
 - $S = tbd$
 - $\pi (s_i)(w_j) = t$ iff $a_j \in W$
 - $\pi (s_i)(l_j) = t$ iff $a_j \in L$
 - $R = tbd$
