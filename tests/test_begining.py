from itertools import chain
import pytest
import brownie
from brownie import *
from brownie import accounts
from brownie.network import rpc
from brownie.network.state import Chain


accounts_number = [1, 2, 3, 4, 5, 6, 7, 8, 9]
amount_multiplied = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
time_period = [3600, 86400, 604800, 2629743, 31556926]
days_in_time_period = [time_period[0]/24, 1, 7, 30, 364]

#new agreement
signee = 1
receiver = 9
amount_sent = 10**5
every_period = 604800
agreement_duration = 2629743
initial_every_time_unit = 7
initial_howLong = 30
agreements_number = 0


without_signee = [signee + 1, signee + 2, signee + 3]
without_receiver = [receiver - 1, receiver - 2, receiver - 3]


less_than_amount_sent = [amount_sent - 10**2, amount_sent - 10**3, amount_sent - 10**4]
more_than_amount_sent = [amount_sent + 10**2, amount_sent + 10**3, amount_sent + 10**4]


less_than_every_period = [every_period - 10**2, every_period - 10**3, every_period - 10**4]
more_than_every_period = [every_period + 10**2, every_period + 10**3, every_period + 10**4]


less_than_agreement_duration = [agreement_duration - 10**2, agreement_duration - 10**3, agreement_duration - 10**4]
more_than_agreement_duration = [agreement_duration + 10**2, agreement_duration + 10**3, agreement_duration + 10**4]

seconds_in_day = 60 * 60 * 24

all_agreements = []
save_deploy = []

@pytest.fixture( autouse=True)
def new_agreement(AgreementBetweenSubjects):
    deploy = AgreementBetweenSubjects.deploy({'from': accounts[0]})
    save_deploy.append(deploy)
    for _ in range(10):
        new_one = deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, {'from': accounts[signee]})
        all_agreements.append(new_one.events)

signee_2 = signee
receiver_2 = receiver
amount_sent_2 = 10**18
every_period_2 = 2629743
agreement_duration_2 = 31556926
agreements_number_2 = 1

@pytest.fixture(autouse=True)
def new_agreement_2(AgreementBetweenSubjects):
    deploy = AgreementBetweenSubjects.deploy({'from': accounts[0]})
    return deploy.createAgreement(accounts[receiver_2], amount_sent_2, every_period_2, agreement_duration_2, {'from': accounts[signee_2]})
    


'''TESTING CREATEAGREEMENT FUNCTION AGREEMENT 1'''



def test_exactAgreement_id():
    '''check if the first id of the agreement is zero'''
    assert save_deploy[0].exactAgreement(agreements_number)[0] == str(agreements_number)

def test_exactAgreement_signee():
    '''check if the first address of the agreement's signee is the same as the signee'''
    assert save_deploy[0].exactAgreement(agreements_number)[1] == accounts[signee]

def test_exactAgreement_receiver():
    '''check if the first address of the agreement's receiver is the same as the accounts[0]'''
    assert save_deploy[0].exactAgreement(agreements_number)[2] == accounts[receiver]

def test_exactAgreement_amount():
    '''check if the amount of the agreement is 2'''
    assert save_deploy[0].exactAgreement(agreements_number)[3] == amount_sent  

def test_exactAgreement_initialize_transactionCreated():
    '''check if the transactionCreated is 0'''
    assert save_deploy[0].exactAgreement(agreements_number)[4] == '0'

def test_exactAgreement_deposit():
    '''check if the initial amount of the deposit is 0'''
    assert save_deploy[0].exactAgreement(agreements_number)[5] == '0'

def test_exactAgreement_status():
    '''check if the initial status is equal to "Created"'''
    assert save_deploy[0].exactAgreement(agreements_number)[6] == 'Created'

def test_exactAgreement_approved():
    '''check if the initial approve "Not Confirmed"'''
    assert save_deploy[0].exactAgreement(agreements_number)[7] == 'Not Confirmed'

def test_exactAgreement_time_creation():
    '''check if the initial time creation is block.timestamp'''
    assert save_deploy[0].exactAgreement(agreements_number)[8] == save_deploy[0].exactAgreement(0)[8]

def test_exactAgreement_every_time_unit():
    '''check if the initial every time unit is every_period'''
    assert save_deploy[0].exactAgreement(agreements_number)[9] >= seconds_in_day * initial_every_time_unit

def test_exactAgreement_position_period():
    '''check if the initial position period is 0'''
    assert save_deploy[0].exactAgreement(agreements_number)[10] == '0'

def test_exactAgreement_how_long():
    '''check if the initial how long is agreement_duration'''
    assert save_deploy[0].exactAgreement(agreements_number)[11] >= seconds_in_day * initial_howLong
#checks agreement 2
def test_exactAgreement_id_agreement_2():
    '''check if the id of the agreement 2 is one'''
    assert save_deploy[0].exactAgreement(1)[0] == '1'

def test_new_agreement_fails_require():
    '''check if the new agreement fails, because howLong > _everyTimeUnit in the require statement'''
    try:
        #length of the agreement is longer than _everyTimeUnit
        save_deploy[0].createAgreement('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', 2, 500, 5, {'from': accounts[signee]})
    except Exception as e:
        assert e.message[50:] == 'The period of the payment is greater than the duration of the contract'

@pytest.mark.parametrize("possibilities", [[0, 10, 15], [10, 0, 15], [10, 10, 0], [0, 0, 15], [10, 0, 0], [0, 10, 0], [0, 0, 0]])
def test_new_agreement_fails_require_larger_than_zero(possibilities):
    '''check if the creation of the new agreement fails, because the input data should be larger than 0'''
    for _ in range(7):
        try:
            save_deploy[0].createAgreement('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', possibilities[0], possibilities[1], possibilities[2], {'from': accounts[signee]})
        except Exception as e:
            assert e.message[50:] == 'All input data must be larger than 0'
    


'''TESTING CREATEAGREEMENT FUNCTION AGREEMENT 2'''


'''
def test_increment_number_of_agreements_correctly(save_deploy[0]):
    assert save_deploy[0].exactAgreement(1)[0] == '1'

def test_exactAgreement_check_large_amount(save_deploy[0]):
    the max number of digits in "amount
    assert save_deploy[0].exactAgreement(1)[3] == amount_sent_2

def test_exactAgreement_transactionCreated(save_deploy[0]):
    check that transactionCreated is 0
    assert save_deploy[0].exactAgreement(1)[4] == '0' 

def test_exactAgreement_check_large_everyTimeUnit(save_deploy[0]):
    the max number of digits in "_everyTimeUnit"
    seconds_in_day = 60 * 60 * 24
    assert save_deploy[0].exactAgreement(1)[9] >= seconds_in_day * 30

def test_exactAgreement_check_large_howLong(save_deploy[0]):
    the max number of digits in _howLong
    seconds_in_day = 60 * 60 * 24
    assert save_deploy[0].exactAgreement(1)[11] >= seconds_in_day * 365
'''


'''TESTING EVENT AGREEMENTINFO INSIDE CREATEAGREEMENT FUNCTION'''



def test_event_AgreementInfo_agreementId():
    '''check if the event AgreementInfo emits correctly agreementId'''
    assert all_agreements[0][0][0].get("agreementId") == save_deploy[0].exactAgreement(agreements_number)[0]

def test_event_AgreementInfo_agreementSignee():
    '''check if the event AgreementInfo emits correctly agreementSignee'''
    assert all_agreements[0][0][0].get("agreementSignee") == save_deploy[0].exactAgreement(agreements_number)[1]

def test_event_AgreementInfo_agreementReceiver():
    '''check if the event AgreementInfo emits correctly agreementReceiver'''
    assert all_agreements[0][0][0].get("agreementReceiver") == save_deploy[0].exactAgreement(agreements_number)[2]

def test_event_AgreementInfo_agreementAmount():
    '''check if the event AgreementInfo emits correctly agreementAmount'''
    assert all_agreements[0][0][0].get("agreementAmount") == save_deploy[0].exactAgreement(agreements_number)[3]

def test_event_AgreementInfo_transactionCreated():
    '''check if the event AgreementInfo emits correctly agreementAmount'''
    assert all_agreements[0][0][0].get("agreementTransactionCreated") == save_deploy[0].exactAgreement(agreements_number)[4]

def test_event_AgreementInfo_agreementDeposit():
    '''check if the event AgreementInfo emits correctly agreementAmount'''
    assert all_agreements[0][0][0].get("agreementDeposit") == save_deploy[0].exactAgreement(agreements_number)[5]

def test_event_AgreementInfo_agreementStatus():
    '''check if the event AgreementInfo emits correctly agreementStatus'''
    assert all_agreements[0][0][0].get("agreementStatus") == save_deploy[0].exactAgreement(agreements_number)[6]

def test_event_AgreementInfo_agreementApproved():
    '''check if the event AgreementInfo emits correctly agreementStatus'''
    assert all_agreements[0][0][0].get("agreementApproved") == save_deploy[0].exactAgreement(agreements_number)[7]

def test_event_AgreementInfo_agreementTimeCreation():
    '''check if the event AgreementInfo emits correctly agreementTimeCreation'''
    assert all_agreements[0][0][0].get("agreementTimeCreation") == save_deploy[0].exactAgreement(agreements_number)[8]

def test_event_AgreementInfo_agreementTimePeriods():
    '''check if the event AgreementInfo emits correctly agreementTimePeriods in seconds'''
    assert all_agreements[0][0][0].get("agreementTimePeriods") == save_deploy[0].exactAgreement(agreements_number)[9]

def test_event_AgreementInfo_agreementPositionPeriod():
    '''check if the event AgreementInfo emits correctly agreementPositionPeriod in days'''
    assert all_agreements[0][0][0].get("agreementPositionPeriod") == save_deploy[0].exactAgreement(agreements_number)[10]

def test_event_AgreementInfo_agreementTimeDuration():
    '''check if the event AgreementInfo emits correctly agreementTimeDuration in seconds'''
    assert all_agreements[0][0][0].get("agreementTimeDuration") == save_deploy[0].exactAgreement(agreements_number)[11]

def test_event_AgreementInfo_equals_Agreement():
    '''check if the length of the AgreementInfo elements is the same as in exactAgreements'''
    agreement = save_deploy[0].exactAgreement(0)
    event = all_agreements[0][0][0]
    assert len(agreement) == len(event)
    


'''TESTING MYSENDERAGREEMENTS FUNCTION'''



def test_MySenderAgreements_fails_require():
    '''check if the MySenderAgreements fails, because msg.sender == _myAddress in the require statement'''
    try:
        #wrong sender's address
        save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[without_receiver[0]]})
    except Exception as e:
        assert e.message[50:] == "The address provided doesn't correspond with the one you're logged in"

def test_MySenderAgreements_emits_correctly_agreementId_agreements_1():
    '''check if the MySenderAgreements function emits correctly the agreementId from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementId'] == save_deploy[0].exactAgreement(agreements_number)[0]   

def test_MySenderAgreements_emits_correctly_agreementSignee_agreements_1():
    '''check if the MySenderAgreements function emits correctly the agreementSignee from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementSignee'] == save_deploy[0].exactAgreement(agreements_number)[1]

def test_MySenderAgreements_emits_correctly_agreementReceiver_agreements_1():
    '''check if the MySenderAgreements function emits correctly the agreementReceiver from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementReceiver'] == save_deploy[0].exactAgreement(agreements_number)[2]

def test_MySenderAgreements_emits_correctly_agreementAmount_agreements_1():
    '''check if the MySenderAgreements function emits correctly the agreementAmount from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementAmount'] == save_deploy[0].exactAgreement(agreements_number)[3]

def test_MySenderAgreements_emits_correctly_agreementTransactionCreated():
    '''check if the MySenderAgreements function emits correctly the agreementTransactionCreated from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementTransactionCreated'] == save_deploy[0].exactAgreement(agreements_number)[4]

def test_MySenderAgreements_emits_correctly_agreementDeposit_agreements_1():
    '''check if the MySenderAgreements function emits correctly the agreementDeposit from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementDeposit'] == save_deploy[0].exactAgreement(agreements_number)[5]

def test_MySenderAgreements_emits_correctly_agreementStatus_agreements_1():
    '''check if the MySenderAgreements function emits correctly the agreementStatus from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementStatus'] == save_deploy[0].exactAgreement(agreements_number)[6]

def test_MySenderAgreements_emits_correctly_agreementApproved_agreements_1():
    '''check if the MySenderAgreements function emits correctly the agreementApproved from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementApproved'] == save_deploy[0].exactAgreement(agreements_number)[7]

def test_MySenderAgreements_emits_correctly_agreementTimeCreation_agreements_1():
    '''check if the MySenderAgreements function emits correctly the agreementTimeCreation from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementTimeCreation'] == save_deploy[0].exactAgreement(agreements_number)[8]

def test_MySenderAgreements_emits_correctly_agreementTimePeriods_agreements_1():
    '''check if the MySenderAgreements function emits correctly the agreementTimePeriods from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementTimePeriods'] == save_deploy[0].exactAgreement(agreements_number)[9]

def test_MySenderAgreements_emits_correctly_agreementPositionPeriod_agreements_1():
    '''check if the MySenderAgreements function emits correctly the agreementPositionPeriod from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementPositionPeriod'] == save_deploy[0].exactAgreement(agreements_number)[10]

def test_MySenderAgreements_emits_correctly_agreementTimeDuration_agreements_1():
    '''check if the MySenderAgreements function emits correctly the agreementTimeDuration from agreement 1'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[0]['agreementTimeDuration'] == save_deploy[0].exactAgreement(agreements_number)[11]
#checks agreement 2
def test_MySenderAgreements_emits_correctly_agreementId_agreements_2():
    '''check if the MySenderAgreements function emits correctly the agreementId from agreement 2'''
    assert save_deploy[0].MySenderAgreements(accounts[signee], {'from': accounts[signee]}).events[1]['agreementId'] == save_deploy[0].exactAgreement(1)[0]

def test_mySenderAgreements_emits_correct_id_accounts_1():
    '''check if the mapping mySenderAgreements emits correct agreementId for the first element in the mapping of address signee'''
    assert save_deploy[0].mySenderAgreements(accounts[signee], 0) == '0'

def test_mySenderAgreements_emits_correct_id_accounts_2():
    '''check if the mapping mySenderAgreements is returning correctly the ids'''
    assert save_deploy[0].mySenderAgreements(accounts[signee], 1) == '1'




'''TESTING MYRECEIVERAGREEMENTS FUNCTION'''



def test_MyReceiverAgreements_fails_require():
    '''check if the MyReceiverAgreements fails, because msg.sender == _myAddress in the require statement'''
    try:
        #wrong sender's address
        save_deploy[0].MyReceiverAgreements(accounts[signee], {'from': accounts[without_signee[0]]})
    except Exception as e:
        assert e.message[50:] == "The address provided doesn't correspond with the one you're logged in"

def test_MyReceiverAgreements_emits_correctly_agreementId_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementId from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementId'] == save_deploy[0].exactAgreement(agreements_number)[0]

def test_MyReceiverAgreements_emits_correctly_agreementSignee_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementSignee from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementSignee'] == save_deploy[0].exactAgreement(agreements_number)[1]

def test_MyReceiverAgreements_emits_correctly_agreementReceiver_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementReceiver from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementReceiver'] == save_deploy[0].exactAgreement(agreements_number)[2]

def test_MyReceiverAgreements_emits_correctly_agreementAmount_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementAmount from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementAmount'] == save_deploy[0].exactAgreement(agreements_number)[3]

def test_MyReceiverAgreements_emits_correctly_agreementTransactionCreated_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementTransactionCreated from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementTransactionCreated'] == save_deploy[0].exactAgreement(agreements_number)[4]

def test_MyReceiverAgreements_emits_correctly_agreementDeposit_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementDeposit from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementDeposit'] == save_deploy[0].exactAgreement(agreements_number)[5]

def test_MyReceiverAgreements_emits_correctly_agreementStatus_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementStatus from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementStatus'] == save_deploy[0].exactAgreement(agreements_number)[6]

def test_MyReceiverAgreements_emits_correctly_agreementApproved_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementApproved from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementApproved'] == save_deploy[0].exactAgreement(agreements_number)[7]

def test_MyReceiverAgreements_emits_correctly_agreementTimeCreation_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementTimeCreation from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementTimeCreation'] == save_deploy[0].exactAgreement(agreements_number)[8]

def test_MyReceiverAgreements_emits_correctly_agreementTimePeriods_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementTimePeriods from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementTimePeriods'] == save_deploy[0].exactAgreement(agreements_number)[9]

def test_MyReceiverAgreements_emits_correctly_agreementPositionPeriod_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementPositionPeriod from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementPositionPeriod'] == save_deploy[0].exactAgreement(agreements_number)[10]

def test_MyReceiverAgreements_emits_correctly_agreementTimeDuration_agreements_1():
    '''check if the MyReceiverAgreements function emits correctly the agreementTimeDuration from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[0]['agreementTimeDuration'] == save_deploy[0].exactAgreement(agreements_number)[11]
#checks agreement 2
def test_MyReceiverAgreements_emits_correctly_agreementId_agreements_2():
    '''check if the MyReceiverAgreements function emits correctly the agreementId from agreement 1'''
    assert save_deploy[0].MyReceiverAgreements(accounts[receiver], {'from': accounts[receiver]}).events[1]['agreementId'] == '1'

def test_myReceiverAgreements_emits_correct_id_agreement_1():
    '''check if the mapping myReceiverAgreements emits correct agreementId for the first element in the mapping of address 0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'''
    assert save_deploy[0].myReceiverAgreements(accounts[receiver], 0) == '0'

def test_myReceiverAgreements_emits_correct_id_agreement_2():
    '''check if the mapping myReceiverAgreements is returning correctly the ids'''
    assert save_deploy[0].myReceiverAgreements(accounts[receiver], 1) == '1'




''' TESTING CONFIRMAGREEMENT FUNCTION'''



def test_ConfirmAgreement_agreement_already_confirmed():
    '''check if the ConfirmAgreement checks if the agreement is already confirmed'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    function_enabled = save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement is already confirmed'

@pytest.mark.parametrize("seconds_sleep",  [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_ConfirmAgreement_fail_require_2(seconds_sleep):
    '''check if the ConfirmAgreement fails if the receiver wants to confirm an agreement that has ended'''
    try:
        chain = Chain()
        chain.sleep(seconds_sleep)
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})        
    except Exception as e:
        assert e.message[50:] == "The agreement's deadline has ended"

@pytest.mark.parametrize("seconds_sleep", [0, less_than_agreement_duration[0], less_than_agreement_duration[1], less_than_agreement_duration[2]])
def test_ConfirmAgreement_fail_require_2_pair(seconds_sleep):
    '''check if the ConfirmAgreement works fine'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    assert save_deploy[0].exactAgreement(agreements_number)[7] == 'Confirmed'    
 
@pytest.mark.parametrize("accounts_number", [without_receiver[0], without_receiver[1], without_receiver[2]])
def test_ConfirmAgreement_fail_require_1(accounts_number):
    '''check if the ConfirmAgreement fails if the receiver is wrong'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[accounts_number]})        
    except Exception as e:
        assert e.message[50:] == "Only the receiver can confirm the agreement"

@pytest.mark.parametrize("accounts_number", [receiver])
def test_ConfirmAgreement_fail_require_1_pair(accounts_number):
    '''check if the ConfirmAgreement fails if the receiver is wrong'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[accounts_number]})        
    except Exception as e:
        assert e.message[50:] != "Only the receiver can confirm the agreement"

def test_ConfirmAgreement_agreement_status_confirmed():
    '''check if the ConfirmAgreement changes status to "Confirmed"'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    assert save_deploy[0].exactAgreement(agreements_number)[7] == 'Confirmed'





'''TESTING TERMINATE CONTRACT'''



#here we are contacting sendPayment prior terminating the agreement (it should be the same otherwise)

def test_terminateContract_emit_Terminated_initial_status_activated_already_terminated():
    '''checking if the event Terminated has been emitted as "This agreement has been terminated" when you want to terminate a contract'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    function_enabled = save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement is already terminated'

@pytest.mark.parametrize("accounts_number", [without_signee[0], without_signee[1], without_signee[2]])
def test_terminateContract_fails_require_wrong_address_initial_status_activated(accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
        #wrong sender's address
        save_deploy[0].terminateContract(agreements_number, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] == "Only the owner can terminate the agreement"

@pytest.mark.parametrize("accounts_number", [signee])
def test_terminateContract_fails_require_wrong_address_initial_status_activated_pair(accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
        #wrong sender's address
        save_deploy[0].terminateContract(agreements_number, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] != "Only the owner can terminate the agreement"

def test_terminateContract_function_change_status_terminated():
    '''check if the function terminateContract changes status of the agreement to "Terminated"'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == 'Terminated'

@pytest.mark.parametrize("value_sent", [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_transfer_deposit_back_to_signee(value_sent):
    '''check if the deposit is transfered back to the signee'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    balance_signee = accounts[signee].balance() 
    save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    assert accounts[signee].balance() == balance_signee + value_sent

@pytest.mark.parametrize("value_sent", [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_transfer_deposit_back_to_signee_pair(value_sent):
    '''check if the deposit is not transfered back to the signee'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
        save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    except Exception as e:
        assert e.message[50:] == "The deposit is not the same as the agreed in the terms"
    

'''
#not implemented 
def test_transfer_msg_value_back_to_signee():
    check if the deposit is transfered back to the signee
    save_deploy[0].ConfirmAgreement(3, {'from': receiver})
    save_deploy[0].sendPayment(3, {'from': accounts[6], 'value': 20})
    balance_signee = accounts[6].balance() 
    save_deploy[0].sendPayment(3, {'from': accounts[6], 'value': 20})
    save_deploy[0].terminateContract(3, {'from': accounts[6]})
    assert accounts[6].balance() == balance_signee + 20
'''

def test_terminateContract_function_change_status_terminated_deposit():
    '''check if the function terminateContract changes deposit to zero"'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    assert save_deploy[0].exactAgreement(agreements_number)[5] == '0'

def test_terminateContract_emit_Terminated_initial_status_activated():
    '''checking if the event Terminated has been emitted as "This agreement has been terminated" when you want to terminate a contract'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    function_enabled = save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement has been terminated'

#here we aren't contacting sendPayments prior terminating the contract

@pytest.mark.parametrize("accounts_number", [without_signee[0], without_signee[1], without_signee[2]])
def test_terminateContract_fails_require_wrong_address_initial_status_activated_without_sendPayments(accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        #wrong sender's address
        save_deploy[0].terminateContract(agreements_number, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] == "Only the owner can terminate the agreement"

@pytest.mark.parametrize("accounts_number", [signee])
def test_terminateContract_fails_require_wrong_address_initial_status_activated_without_sendPayments_pair(accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        #wrong sender's address
        save_deploy[0].terminateContract(agreements_number, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] != "Only the owner can terminate the agreement"

def test_terminateContract_function_change_status_terminated_without_sendPayments():
    '''check if the function terminateContract changes status of the agreement to "Terminated"'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == 'Terminated'

def test_transfer_deposit_back_to_signee_2():
    '''check if the deposit is transfered back to the signee'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    balance_signee = accounts[signee].balance() 
    save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    assert accounts[signee].balance() == balance_signee

def test_terminateContract_function_change_status_terminated_deposit_2():
    '''check if the function terminateContract changes deposit to 0'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    assert save_deploy[0].exactAgreement(agreements_number)[5] == '0'

def test_terminateContract_emit_Terminated_initial_status_activated_without_sendPayments():
    '''checking if the event Terminated has been emitted as "This agreement has been terminated" when you want to terminate a contract'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    function_enabled = save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement has been terminated'



'''TESTING SENDPAYMENT, INITIALIZINGPOSITIONPERIOD AND TIMENOTBREACHED FUNCTIONS'''


#can we check the require, revert
#What happens if the unix timestamp is larger or equal to 19th Jan 2038?
#what happens if teh transaction cannot be sent?

#Checking the require statements 

@pytest.mark.parametrize("accounts_number", [without_signee[0], without_signee[1], without_signee[2]])
def test_sendPayments_fails_require_wrong_address(accounts_number):
    '''check if the sendPayments fails, because exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        #wrong signer's address
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[accounts_number], 'value': amount_sent})
    except Exception as e:
        assert e.message[50:] == "Only the owner can pay the agreement's terms"

@pytest.mark.parametrize("accounts_number", [signee])
def test_sendPayments_fails_require_wrong_address_pair(accounts_number):
    '''check if the sendPayments fails, because exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        #wrong signer's address
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[accounts_number], 'value': amount_sent})
    except Exception as e:
        assert e.message[50:] != "Only the owner can pay the agreement's terms"

def test_sendPayments_fails_require_not_confirmed():
    '''check if the sendPayments fails, because exactAgreement[_id].approved)) == "Confirmed" in the require statement'''
    try:
        #no confirmation
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    except Exception as e:
        assert e.message[50:] == "The receiver has to confirm the contract"

#Checking when the agreement's status is "Created"

@pytest.mark.parametrize("seconds_sleep",  [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_sendPayments_require_statement_fails_agreement_not_ended(seconds_sleep):
    '''check if the require statement fails when the agreement's deadline has ended'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        chain = Chain()
        chain.sleep(seconds_sleep)
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})      
    except Exception as e:
        assert e.message[50:] == "This agreement's deadline has ended"

@pytest.mark.parametrize("seconds_sleep",  [less_than_agreement_duration[0], less_than_agreement_duration[1], less_than_agreement_duration[2]])
def test_sendPayments_require_statement_fails_agreement_not_ended_pair(seconds_sleep):
    '''check if the require statement works fine when the agreement's deadline has not ended'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == 'Activated'      
  
@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_sendPayments_fails_require_smaller_deposit_initial_status_created(value_sent):
    '''check if the sendPayments fails, because exactAgreement[_id].amount <= msg.value in the require statement'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        #'value' is smaller than it should be
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    except Exception as e:
        assert e.message[50:] == "The deposit is not the same as the agreed in the terms"

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_sendPayments_fails_require_smaller_deposit_initial_status_created_pair(value_sent):
    '''checking if the status is changed to "Activated" when msg.value is larger or equal to agreedDeposit'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == 'Activated'

def test_sendPayments_change_initializePeriod_initial_status_created():
    '''checking if the InitializedPeriod is initialize (sum of agreementTimeCreation and everyTimeUnit) when msg.value is larger or equal to agreedDeposit'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[10] == save_deploy[0].exactAgreement(0)[8] + save_deploy[0].exactAgreement(0)[9]

def test_sendPayments_change_agreementDeposit_initial_status_created():
    '''checking if the deposit has been initialized to msg.value when msg.value is larger or equal to agreedDeposit'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[5] == amount_sent

def test_sendPayments_emit_NotifyUser_initial_status_created():
    '''checking if the event has been emitted as "We have activate the agreement" when msg.value is larger or equal to agreedDeposit'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    function_enabled = save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    message = function_enabled.events[0][0]['message']
    assert message == 'We have activate the agreement'



#Checking when the agreement's status is "Activated"
#if the transaction sent was on time

def test_timeNotBreached():
    '''check if the timeNotBreached function correctly increments positionPeriod. This is for checking inside sendPayments function'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    new_agreement_position = save_deploy[0].exactAgreement(0)[10]
    #the contract has been activated, now send the the money again
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})    
    assert save_deploy[0].exactAgreement(agreements_number)[10] == new_agreement_position + save_deploy[0].exactAgreement(0)[9]

def test_transactionCreated_updated():
    '''check if the time of the call to function sendPayment is stored'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[4] != '0'

def test_transactionCreated_updated_once_again():
    '''check if the time of the call to function sendPayment changes after another call to this function'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()  
    chain.sleep(3)
    first_call = save_deploy[0].exactAgreement(agreements_number)[4]
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[4] != first_call

    #if the amount <= msg.value
 
@pytest.mark.parametrize("seconds_sleep",  [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_timeNotBreached_fail_if_statement(seconds_sleep):
    '''check if the timeNotBreached fails because transaction was sent after the agreement's deadline - it fails because of the check in the ConfirmAgreement function'''
    try:
        chain = Chain()
        chain.sleep(seconds_sleep)
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    except Exception as e:        
        assert e.message[50:] == "The agreement's deadline has ended"

@pytest.mark.parametrize("seconds_sleep",  [less_than_agreement_duration[0], less_than_agreement_duration[1], less_than_agreement_duration[2]])
def test_timeNotBreached_fail_if_statement_pair(seconds_sleep):
    '''check if the timeNotBreached works fine when ConfirmAgreement check is passed'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == 'Activated'

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value(value_sent):
    '''check if the msg.value is sent when amount <= msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    balance_receiver = accounts[receiver].balance() 
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert accounts[receiver].balance() == balance_receiver + value_sent

@pytest.mark.parametrize("value_sent",  [amount_sent])
@pytest.mark.parametrize("value_decreased",  [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value_pair(value_sent, value_decreased):
    '''check if the msg.value is not sent when amount <= msg.value in the timeNotBreached, the contract terminates'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent - value_decreased}) 
    assert save_deploy[0].exactAgreement(agreements_number)[6] == 'Terminated'

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value_check_signee(value_sent):
    '''check if the balance of the signee is changed when amount <= msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    balance_signee = accounts[signee].balance() 
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert accounts[signee].balance() == balance_signee - value_sent

@pytest.mark.parametrize("value_sent",  [amount_sent])
@pytest.mark.parametrize("value_decreased",  [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value_check_signee_pair(value_sent, value_decreased):
    '''check if the balance of the signee is the same when amount <= msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    balance_signee = accounts[signee].balance() 
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent - value_decreased}) 
    assert accounts[signee].balance() == balance_signee

'''
tried to test failed sent , but couldn't fugure it out
@pytest.mark.vvv
def test_timeNotBreached_value_large_amount_fail_sending(save_deploy[0]):
    check if the "Failed to send Ether" is outposted when sending the money fails
    try:
        save_deploy[0].ConfirmAgreement(5, {'from': "0x0000000000000000000000000000000000000000"})
        save_deploy[0].sendPayment(5, {'from': accounts[6]})
        #save_deploy[0].sendPayment(5, {'from': accounts[6], 'value': 20})
    except Exception as e:        
        assert e.message[50:] == "Failed to send Ether"'''
   
def test_timeNotBreached_value_large_amount_emit_NotifyUser():
    '''check if the event NotifyUser is emitted when amount <= msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    #the contract has been activated, now send the money again
    function_initialize = save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert function_initialize.events[0][0]['message'] == "Transaction was sent to the receiver"

    #if the amount > msg.value

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_status(value_sent):
    '''check if the status is changed when amount > msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    #the contract has been activated, now send the smaller quantity of money again
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == "Terminated"

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_status_pair(value_sent):
    '''check if the status stays the same when amount < msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == "Activated"

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_send_deposit(value_sent):
    '''check if the deposit is sent to the receiver when amount > msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance() 
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert accounts[receiver].balance() == balance_receiver + amount_sent

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_send_deposit_pair(value_sent):
    '''check if the deposit isn't sent (but the sending value) to the receiver when amount < msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance() 
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert accounts[receiver].balance() == balance_receiver + value_sent

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_deposit_equals_zero(value_sent):
    '''check if the deposit is back on zero when amount > msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert save_deploy[0].exactAgreement(agreements_number)[5] == "0"

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_deposit_equals_zero_pair(value_sent):
    '''check if the deposit is not sent back on zero when amount < msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert save_deploy[0].exactAgreement(agreements_number)[5] != "0"

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_return_transaction(value_sent):
    '''check if the transaction is sent back to the signee when amount > msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})  
    balance_signee = accounts[signee].balance() 
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert accounts[signee].balance() == balance_signee

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_return_transaction_pair(value_sent):
    '''check if the transaction is reduced from the signee when amount < msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})  
    balance_signee = accounts[signee].balance() 
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert accounts[signee].balance() == balance_signee - value_sent

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])    
def test_timeNotBreached_value_smaller_amount_emit_Terminated(value_sent):
    '''check if the event Terminated is emitted when amount > msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    #the contract has been activated, now send the smaller quantity of money again
    function_initialize = save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    assert function_initialize.events[0][0]['message'] == "This agreement was terminated due to different payment than in the terms"

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]]) 
def test_timeNotBreached_value_smaller_amount_emit_Terminated_pair(value_sent):
    '''check if the event NotifyUser is emitted when amount < msg.value in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    function_initialize = save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    assert function_initialize.events[0][0]['message'] == "Transaction was sent to the receiver"

    

#if the transaction wasn't sent on time

@pytest.mark.parametrize("seconds_sleep",  [every_period, 604801, 688888])
def test_timeNotBreached_received_on_time_false_1st_part_if_statement(seconds_sleep):
    '''check if the timeNotBreached returns false, when transactionCreated > positionPeriod'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == 'Terminated' 

@pytest.mark.parametrize("seconds_sleep",  [60*60*24*7, 60*60*24*8, 60*60*24*10])
def test_timeNotBreached_received_on_time_false_2nd_part_if_statement(seconds_sleep):
    '''check if the timeNotBreached returns false, when transaction received wasn't on time'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == 'Terminated'

@pytest.mark.parametrize("seconds_sleep",  [2240000, agreement_duration, 2629744, 26297440])
def test_timeNotBreached_breached_on_time_false_3rd_part_if_statement(seconds_sleep):
    '''check if the timeNotBreached returns false, when the deadline of the agreement has ended'''
    chain = Chain()
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    
    for _ in range(3):
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
        chain.sleep(60400)
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == "Terminated"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_status(seconds_sleep):
    '''check if the status is changed to Terminated when timeNotBreached is breached in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    assert save_deploy[0].exactAgreement(agreements_number)[6] == "Terminated"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_status_pair(seconds_sleep):
    '''check if the status is not changed to Terminated when timeNotBreached is not breached in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    assert save_deploy[0].exactAgreement(agreements_number)[6] == "Activated"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_send_deposit(seconds_sleep):
    '''check if the deposit is sent to the receiver when timeNotBreached is breached in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent}) 
    assert accounts[receiver].balance() == balance_receiver + amount_sent

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_send_deposit_pair(seconds_sleep):
    '''check if the deposit isn't sent to the receiver (but the value is) when timeNotBreached is not breached in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent}) 
    assert accounts[receiver].balance() == balance_receiver + 4*amount_sent

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_deposit_equals_zero(seconds_sleep):
    '''check if the deposit is equal zero when timeNotBreached is breached in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    assert save_deploy[0].exactAgreement(agreements_number)[5] == "0"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_deposit_equals_zero_pair(seconds_sleep):
    '''check if the deposit is not equal zero when timeNotBreached is not breached in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    assert save_deploy[0].exactAgreement(agreements_number)[5] != "0"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_return_transaction(seconds_sleep):
    '''check if the transaction is sent back to the signee when timeNotBreached is breached in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})  
    balance_signee = accounts[signee].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    assert accounts[signee].balance() == balance_signee

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_return_transaction_pair(seconds_sleep):
    '''check if the transaction is not sent back to the signee (it's sent to the receiver) when timeNotBreached is not breached in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})  
    balance_signee = accounts[signee].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    assert accounts[signee].balance() == balance_signee - amount_sent

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_emit_Terminated(seconds_sleep):
    '''check if the event Terminated is emitted when timeNotBreached is breached in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    function_initialize = save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert function_initialize.events[0][0]['message'] == "This agreement was terminated due to late payment"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_emit_Terminated_pair(seconds_sleep):
    '''check if the event Terminated is not emitted when timeNotBreached is not breached in the timeNotBreached'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    function_initialize = save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert function_initialize.events[0][0]['message'] != "This agreement was terminated due to late payment"

#Checking when the agreement's status is "Terminated"

def test_terminateContract_emit_Terminated_initial_status_terminated():
    '''check if the sendPayments emits correctly the message when the status is "Terminated"'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    save_deploy[0].terminateContract(agreements_number, {'from': accounts[signee]})
    with brownie.reverts("This agreement was already terminated"):
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    


#Checking when the agreement's status is else
#this test will fail because i don't know how to change the status
#def test_timeNotBreached_breached_value_larger_amount_status_not_defined(save_deploy[0]):
    '''check if the status is changed when timeNotBreached is breached in the timeNotBreached'''
    #save_deploy[0].ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    #save_deploy[0].sendPayment(0, {'from': signee, 'value': 20})
    #save_deploy[0].exactAgreement(0).status = "The status is something else"
    #assert save_deploy[0].exactAgreement(0)[6] == "The status is something else"
    #the contract has been activated, now send the smaller quantity of money again
    #with brownie.reverts("There is no agreement with this id"):
        #save_deploy[0].sendPayment(0, {'from': signee, 'value': 20})




''' TESTING WASCONTRACTBREACHED FUNCTION '''


 
@pytest.mark.parametrize("wrong_accounts",  [without_receiver[0], without_receiver[1], without_receiver[2]])
def test_wasContractBreached_require_receiver_equals_msg_sender(wrong_accounts):
    '''check if the wasContractBreached fails, because exactAgreement[_id].receiver == msg.sender is the require statement'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    with brownie.reverts("The receiver in the agreement's id isn't the same as the address you're logged in"):
        #wrong signee's address
        save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[wrong_accounts]})

@pytest.mark.parametrize("right_accounts",  [receiver])
def test_wasContractBreached_require_receiver_equals_msg_sender_pair(right_accounts):
    '''check if the wasContractBreached doesn't fail'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
        save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[right_accounts]})
    except Exception as e:        
        assert e.message[50:] == "This agreement's deadline has ended"

def test_wasContractBreached_fail_if_statement_in_timeNotBreached():
    '''check if the timeNotBreached fails because transaction was sent after the agreement's deadline - it fails because of the check in the ConfirmAgreement function'''
    try:
        save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
        chain = Chain()
        chain.sleep(2629800)
        save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
        save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[receiver]})
    except Exception as e:        
        assert e.message[50:] == "This agreement's deadline has ended"

#if timeNotBreached is True

def test_wasContractBreached_timeNotBreached_true_emit_NotifyUser():
    '''check if the wasContractBreached function when timeNotBreached is true, emits NotifyUser'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    function_initialize = save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement wasn't breached"

#check 3 parts of the if statement in timeWasntBreached

#if timeNotBreached is False
@pytest.mark.skip(reason='doesn not work correctly')
#seconds_sleep must be more then agreement_duration, but less then agreement_duration + 7 days
@pytest.mark.parametrize("seconds_sleep",  [2629761, 3000000, 3234542, 3234543, 9999999])
def test_wasContractBreached_received_on_time_false(seconds_sleep):
    '''check if the wasContractBreached returns false, when transaction received wasn't on time, but doesn't wait 7 days for withdraw'''
    try:
        save_deploy[0].ConfirmAgreement(1, {'from': accounts[receiver_2]})
        save_deploy[0].sendPayment(1, {'from': accounts[signee_2], 'value': amount_sent})
        chain = Chain()
        chain.sleep(seconds_sleep)
        save_deploy[0].wasContractBreached(1, {'from': accounts[receiver_2]})
    #save_deploy[0].sendPayment(1, {'from': signee, 'value': amount_sent})
    #save_deploy[0].wasContractBreached(1, {'from': receiver})

    #function_initialize = save_deploy[0].wasContractBreached(1, {'from': receiver})
    #assert function_initialize.events[0][0]['message'] == "The agreement wasn't breached"

    #assert save_deploy[0].exactAgreement(1)[6] == "Terminated"
    except Exception as e:        
        assert e.message[50:] == "You have to wait at least 7 days after breached deadline to withdraw the deposit"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_Terminated(seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, changes status to Terminated'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == "Terminated"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_Terminated_pair(seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't change status to Terminated'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert save_deploy[0].exactAgreement(agreements_number)[6] == "Activated"
 
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_send_deposit(seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, sends a deposit to the receiver'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance()
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + amount_sent

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_send_deposit_pair(seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't send a deposit to the receiver'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance()
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + 4*amount_sent

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_deposit_equals_zero_1(seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, changes deposit to 0'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert save_deploy[0].exactAgreement(agreements_number)[5] == '0'

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_deposit_equals_zero_1_pair(seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't change deposit to 0'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert save_deploy[0].exactAgreement(agreements_number)[5] != '0'

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_emit_Terminated(seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, emits NotifyUser'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    function_initialize = save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "This agreement is already terminated"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_emit_Terminated_pair(seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't emit NotifyUser'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    save_deploy[0].sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    function_initialize = save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] != "This agreement is already terminated"

def test_wasContractBreached_agreement_not_activated():
    '''check if the wasContractBreached function emits NotifyUser when timeNotBreached is false'''
    save_deploy[0].ConfirmAgreement(agreements_number, {'from': accounts[receiver]})
    function_initialize = save_deploy[0].wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "This agreement hasn't been activated"

