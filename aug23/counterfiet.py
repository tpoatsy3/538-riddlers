"""
	538 Riddler Express, August 23
	Solution by Ted Poatsy

	The Problem:
	You are an expert counterfeiter, and you specialize in forging one of the
	most ubiquitous notes in global circulation, the U.S. $100 bill. You’ve been
	able to fool the authorities with your carefully crafted C-notes for some
	time, but you’ve learned that new security features will make it impossible
	for you to continue to avoid detection. As a result, you decide to deposit
	as many fake notes as you dare before the security features are implemented
	and then retire from your life of crime.

	You know from experience that the bank can only spot your fakes 25 percent
	of the time, and trying to deposit only counterfeit bills would be a ticket
	to jail. However, if you combine fake and real notes, there’s a chance the
	bank will accept your money. You have $2,500 in bona fide hundreds, plus a
	virtually unlimited supply of counterfeits. The bank scrutinizes cash
	deposits carefully: They randomly select 5 percent of the notes they receive,
	rounded up to the nearest whole number, for close examination. If they
	identify any note in a deposit as fake, they will confiscate the entire
	sum, leaving you only enough time to flee.

	How many fake notes should you add to the $2,500 in order to maximize the
	expected value of your bank account? How much free money are you likely to
	make from your strategy?
"""

import pandas as pd
import numpy as np
from scipy.special import comb
import matplotlib.pyplot as plt


# Givens
REAL_BILLS_COUNT = 25
BANK_DETECT_PROB = .25
REVIEW_PCT = 0.05
BILL_VALUE = 100


# Arbitrarily selecting 0 to 100 fake bills as initial sample space
fake_bills = list(range(0,101))

# Create an dataframe to contain each possibility
df = pd.DataFrame(np.array(fake_bills), columns=['totalFake'])

# Adding how many total bills and how many bills would then be reviewed in that scenario
df['total'] = df['totalFake'] + 25
df['reviewed'] = np.ceil(df['total'] * REVIEW_PCT)



def findExpA(fakes, selected):
	""" Let's define A as the event of a fake being drawn.
		E[A], therefore, is the expected number of fakes being drawn.

		This method calculates the dependent probability of the bank drawing any...
			possible number of fake bills into the selected group.
		Then, it weighs them by their expected value (number of fakes drawn) ...
			and by the number of possible combinations for that outcome.

		Params:
		 * fakes: Number of fake bills deposited to the bank
		 * selected: Number of bills that are selected at random

		Returns: E[A] (float64)
	"""

	# It should be assumed that to maximize your return for a single deposit, you
	# should add all $2500 of real bills.
	total = REAL_BILLS_COUNT + fakes



	# Creating 2D array used to calculate the dependent probabilities for each outcome
	q_components = [0] * (selected + 1)

	#Using selected + 1 as upper bound because a 'selection' happens between each index in the array
	for i in range(selected+1):
		q_components[i] = [0] * (selected + 1)

	# Setting probability at the beginning of the problem to 1
	q_components[0][0] = 1

	# Simulating drawing a bill
	for drawn_bill in range(selected):
		remaining_bills = total - drawn_bill


		# Playing out situations in which the drawn bill is the n-th fake to be drawn
		# (drawn_fake is the variable name used for n)
		for drawn_fake in range(selected):
			remaining_fakes = fakes - drawn_fake

			# Skip over situations where there are more fakes drawn than bills (impossible)
			if drawn_fake > drawn_bill:
				continue

			# Calc probability of not drawing a fake
			if q_components[drawn_bill + 1][drawn_fake] == 0:
				q_components[drawn_bill + 1][drawn_fake] = q_components[drawn_bill][drawn_fake] * ((remaining_bills - remaining_fakes) / remaining_bills)

			# Calc probability of drawing a fake
			if q_components[drawn_bill + 1][drawn_fake + 1] == 0:
				q_components[drawn_bill + 1][drawn_fake + 1] = q_components[drawn_bill][drawn_fake] * ((remaining_fakes) / remaining_bills)

	# Finding how many different combinations of each outcome are possible (n choose k)
	combos = [0] * (selected + 1)
	for i in range(selected + 1):
		combos[i] = comb(selected, i)

	# Summing the expected values together
	expA = 0
	for val in range(selected + 1):
		expA += val * combos[val] * q_components[selected][val]

	return expA



# Finding the expected value of A in each scenario
df['expA'] = df.apply(lambda x: findExpA(int(x['totalFake']), int(x['reviewed'])), axis=1)



"""
	Let's define B as the event that a fake bill is detected. Since the bank
	either finds a fake bill and confiscates the sum or not, the expected value
	of B then is the probability that any fraud is detected. Or, equally, the
	probability that all frauds are not detected.

	Note: These calculations relys on the assumption that no real bills will
	errantly be determined as counterfeits.
"""

# Finding the expected value of B
df['expB'] = df.apply(lambda x: (1-BANK_DETECT_PROB) ** x['expA'], axis=1)


def payoff(bills, expB):
	"""
	Calculates the expected pay-off of the counterfeiter's... craft.

	Params:
	 * bills: Integer value of total bills submitted for deposit
	 * expB: Float value of the expected value of the event that a fake bill is detected

	Returns:
	 * Expected value of sum added to the counterfeiter's bank account

	"""

	full_profit = bills * BILL_VALUE
	prob_success = expB

	# Probability of failure is not included because the bank will sieze the whole
	# 	deposit after detecting a single fake.
	return (full_profit*prob_success)


# Applying pay-off method to the dataframe
df['expPayoff'] = df.apply(lambda x: payoff(int(x['total']), float(x['expB'])), axis=1)


# Creating a plot of the sample space
plt.figure()
plt.plot(df['total'], df['expPayoff'])

# The 'max' function on the expPayoff column showed that 60 bills (35 fakes) was
# 	the optimal outcome, but thie graph showed that 80 bills (55 fakes) was close
# 	as well. A closer look showed that they had the same expected payoff so both
# 	are highlighted on the graph.
plt.text(60, df.at[35, 'expPayoff'], "${:.2f}".format(df.at[35, 'expPayoff']))
plt.text(80, df.at[55, 'expPayoff'], "${:.2f}".format(df.at[55, 'expPayoff']))

plt.show()
