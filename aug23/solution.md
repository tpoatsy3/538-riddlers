# Counterfieters

August 23rd Riddler Express

### Problem Description

You are an expert counterfeiter, and you specialize in forging one of the most ubiquitous notes in global circulation, the U.S. $100 bill. You’ve been able to fool the authorities with your carefully crafted C-notes for some time, but you’ve learned that new security features will make it impossible for you to continue to avoid detection. As a result, you decide to deposit as many fake notes as you dare before the security features are implemented and then retire from your life of crime.

You know from experience that the bank can only spot your fakes 25 percent of the time, and trying to deposit only counterfeit bills would be a ticket to jail. However, if you combine fake and real notes, there’s a chance the bank will accept your money. You have $2,500 in bona fide hundreds, plus a virtually unlimited supply of counterfeits. The bank scrutinizes cash deposits carefully: They randomly select 5 percent of the notes they receive, rounded up to the nearest whole number, for close examination. If they identify any note in a deposit as fake, they will confiscate the entire sum, leaving you only enough time to flee.

How many fake notes should you add to the $2,500 in order to maximize the expected value of your bank account? How much free money are you likely to make from your strategy?

### Answer

You can maximize the expected value of your bank account most by depositing either $6000 ($2500 in real bills, $3500 in fake bills) or $8000 ($2500 in real bills, $5500 in fake bills). Both of those deposits have the same expected value added to your bank account, $3626.67.

### Showing The Work

The problem can be split into three sub-problems. First, given a deposit containing both real and fake notes, how many fakes do you expect to be drawn for inspection? In other words, what's your exposure to risk? 

The expected value of fake bills to be inspected depends on how many bills will be inspected and the composition of your deposit. The number of bills that will be inspected is defined in the problem as 5% of the deposited bills, rounded up to the nearest whole number. Now, the problem is analogous to picking certain cards from a shuffled deck. Use dependent probability to find what the likelihood of the bank picking a certain amount of the fake bills in their inspected file. Then, multiply those probabilities by how many compibinations of that option there are (fake bills choose inspected bills) and the weight of each outcome (the number of fake bills inspected in that scenario). 

For example, with 27 deposited notes (25 real, 2 fake), the bank will pick 2 bills for inspection. There is a 2/(26*27) probability that both fakes will be randomly selected. Also, there is a 50/(26*27) probability that one fake will be selected, which could happen in two ways (either fake being the fake selected). The rest of the probability is that zero fakes are selected. The expected value of fakes selected in this scenario is the weight of each scenario times the probability of the scenario times the possibilities of each scenario, summed. So, for this example, that would look like this:

` Expected Value = 2 * 1 * (2/(26*27)) + 1 * 2 * (50/(26/27)) = 104/702 = 4/27`

So, with 27 deposited notes, you'd expect that 4/27 notes will be inspected.

The second part of the problem is given how many notes you expect to be inspected, how many will actually be detected?

The problem says that the bank can catch a counterfiet 25% of the time. But if any of the fakes are detected, the bank confiscates the whole deposit. So, no fake note can be detected. Translated into a more clear probability problem: the first fake cannot be detected and the second note cannot be detected and so on. So we'll take the 75% chance that the note will evade detection and raise it to the power of the amount of bills we expect to be inspected. In the same example as before that would be `.75^(4/27)`, which means roughly 95.83% of the time, your counterfeits would go unnoticed in this scenario. 

Finally, the last problem is what's the expected value of your deposit? The bank's all-or-nothing policy made this calcuation simple. Multiply the deposited sum by the likelihood that your bills will go undetected to get your expected deposit. With the same example as before, the calculation of .9583 * $2700 means you'd expect 2587.34 in your bank account.

### See also
I wrote this problem as a python script following the same process. It's `conterfiet.py`. The output, which graphs the number of bills deposited against the expected pay-off, is saved as `couterfeit_plot.png`. 


