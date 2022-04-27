

WHY
---

I see smart contracts as means of resolving one of the most difficult problems - How can I trust someone I don't know and with whom I don't have physical contact that her/his actions will back up what we have agreed upon?
I think by creating a system that allows us to trust one another even if we are complete strangers will eventually lead to new and far better relationships between subjects, consequently to new economies - ones that we haven't seen before.
Just imagine how this could help to create a new world. A world were trusting strangers will be taken for granted. 

-------------------------------------------------
* How does this smart contract follow the above?
-------------------------------------------------

Our first implementation (and for sure not our last) of the vision we have mentioned above is enabling people to back up their words of sending money to other subjects. 
Lets make a mental experiment. Imagine someone tells another person, institution or organisation: "I will send you 1 ether every month for a whole year starting 3 months from now." How can you be sure she/he will actually do that? You can't be. 
Therefore, I have created a system were you will loose money, if you don't fulfill your commitments. 

SHORT SUMMARY OF INTENDED USE
------------------------------

-----------------------------------------------
* What this smart contract should be used for?
-----------------------------------------------
I invision it to be used for donations, fundings, alimony and other commitments I can't think off. This is meant to be used in cases where multiple transactions are going to be sent to obey the agreement.
It could be used for singular transaction, but keep in mind that you will have to send a deposit of the amount you have agreed upon when you create an agreement. Therefore, this isn't the most best use case for singular transactions.

---------------------------------------------------
* What this smart contract SHOULD NOT be used for?
---------------------------------------------------
It shouldn't be used for any agreements where one subject commits sending money and other providing services and goods for the received money. 
This smart contract DOESN'T have an implementation of checking if the payer is receiving goods or services for his/her money.
The purpose of this smart contract is to check if the subject who commited sending money really does that. Otherwise, the deposit will be sent to the receiver.

---------------------------------------------------------------
* Short step by step summary on how to use this smart contract:
----------------------------------------------------------------
	1) The sender creates an agreement where he/she defines the receiver's address, amount of money he/she will send each time period, time period of every transaction (every day, week, month, ...), for how long these agreement will last and from which date on this agreement begins. 
	   Additionally, the sender will have to send the amount you have agreed upon when you create an agreement. This amount will be used as the deposit, which will be sent to the receiver if the agreement is breached.
	   The sender will get back the deposit if he/she fulfills his/her obligations in the agreement.
	2) Now the agreement is activated. The sender needs to fulfill his/her obligations in the agreement by sending the right amount of money in the correct time periods. Otherwise, he/she will loose the deposit. 
	3) The receiver can check if the agreement was breached by calling wasContractBreached function. He/She will received the deposit in the case of a breach.
	4) once the sender sends the last deposit, the contract will be terminated and he/she will be able to retrieve his/her deposit.
	5) The sender and receiver can withdraw the money that belongs to them by calling a withdraw function.

------------------------------------------------------------------
* Why are there 2 contracts in this repo?
------------------------------------------------------------------
This contract is attended to be deployed with AddressProtector smart contract, which provides more safety towards people who deploy smart contract. If you want to learn more, please check our ProtectSmartContracts repository
