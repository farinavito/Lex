from itertools import chain
import pytest
import brownie
from brownie import *
from brownie import accounts
from brownie.network import rpc
from brownie.network.state import Chain

#new agreement
signee = 1
receiver = 9
amount_sent = 10**1
every_period = 604800
agreement_duration = 2629743
initial_every_time_unit = 7
initial_howLong = 30
agreements_number = 0


without_signee = [signee + 1, signee + 2, signee + 3]
without_receiver = [receiver - 1, receiver - 2, receiver - 3]


less_than_amount_sent = [amount_sent - 5, amount_sent - 6, amount_sent - 7]
more_than_amount_sent = [amount_sent + 10**2, amount_sent + 10**3, amount_sent + 10**4]


less_than_every_period = [every_period - 10**2, every_period - 10**3, every_period - 10**4]
more_than_every_period = [every_period + 10**2, every_period + 10**3, every_period + 10**4]


less_than_agreement_duration = [agreement_duration - 10**2, agreement_duration - 10**3, agreement_duration - 10**4]
more_than_agreement_duration = [agreement_duration + 10**5, agreement_duration + 10**6, agreement_duration + 10**7]

seconds_in_day = 60 * 60 * 24



@pytest.fixture()
def deploy(AgreementBetweenSubjects, module_isolation):
    return AgreementBetweenSubjects.deploy({'from': accounts[0]})

@pytest.fixture(autouse=True)
def new_agreement(deploy, module_isolation):
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    return deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[signee], 'value': amount_sent})
    

signee_2 = signee
receiver_2 = receiver
amount_sent_2 = 10**1
every_period_2 = 2629743
agreement_duration_2 = 31556926
initial_every_time_unit_2 = 30
initial_howLong_2 = 364
agreements_number_2 = 1

@pytest.fixture(autouse=True)
def new_agreement_2(deploy, module_isolation):
    chain = Chain()
    now = chain.time()
    startAgreement = now + 4
    return deploy.createAgreement(accounts[receiver_2], amount_sent_2, every_period_2, agreement_duration_2, startAgreement, {'from': accounts[signee_2], 'value': amount_sent_2})
    


'''TESTING CREATEAGREEMENT FUNCTION AGREEMENT 1'''



def test_exactAgreement_id(deploy):
    '''check if the first id of the agreement is zero'''
    assert deploy.exactAgreement(agreements_number)[0] == str(agreements_number)

def test_exactAgreement_signee(deploy):
    '''check if the first address of the agreement's signee is the same as the signee'''
    assert deploy.exactAgreement(agreements_number)[1] == accounts[signee]

def test_exactAgreement_receiver(deploy):
    '''check if the first address of the agreement's receiver is the same as the accounts[0]'''
    assert deploy.exactAgreement(agreements_number)[2] == accounts[receiver]

def test_exactAgreement_amount(deploy):
    '''check if the amount of the agreement is 2'''
    assert deploy.exactAgreement(agreements_number)[3] == amount_sent  

def test_exactAgreement_initialize_transactionCreated(deploy):
    '''check if the transactionCreated is 0'''
    assert deploy.exactAgreement(agreements_number)[4] == '0'

def test_exactAgreement_deposit(deploy):
    '''check if the initial amount of the deposit is amount_sent'''
    assert deploy.exactAgreement(agreements_number)[5] == amount_sent

def test_exactAgreement_status(deploy):
    '''check if the initial status is equal to "Created"'''
    assert deploy.exactAgreement(agreements_number)[6] == 'Created'

def test_exactAgreement_approved(deploy):
    '''check if the initial approve "Not Confirmed"'''
    assert deploy.exactAgreement(agreements_number)[7] == 'Not Confirmed'

def test_exactAgreement_time_creation(deploy):
    '''check if the initial time creation is startAgreement'''
    assert deploy.exactAgreement(agreements_number)[8] == deploy.exactAgreement(0)[8]

def test_exactAgreement_every_time_unit(deploy):
    '''check if the initial every time unit is every_period'''
    assert deploy.exactAgreement(agreements_number)[9] >= seconds_in_day * initial_every_time_unit

def test_exactAgreement_position_period(deploy):
    '''check if the initial position period is 0'''
    assert deploy.exactAgreement(agreements_number)[10] == '0'

def test_exactAgreement_how_long(deploy):
    '''check if the initial how long is agreement_duration'''
    assert deploy.exactAgreement(agreements_number)[11] >= seconds_in_day * initial_howLong

def test_new_agreement_fails_require(deploy):
    '''check if the new agreement fails, because howLong > _everyTimeUnit in the require statement'''
    try:
        chain = Chain()
        now = chain.time()
        startAgreement = now + 10000
        #length of the agreement is longer than _everyTimeUnit
        deploy.createAgreement('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', 2, 500, 5, startAgreement, {'from': accounts[signee], 'value': amount_sent})
    except Exception as e:
        assert e.message[50:] == 'The period of the payment is greater than the duration of the contract'

@pytest.mark.parametrize("possibilities", [[0, 10, 15], [10, 0, 15], [10, 10, 0], [0, 0, 15], [10, 0, 0], [0, 10, 0], [0, 0, 0]])
def test_new_agreement_fails_require_larger_than_zero(possibilities, deploy):
    '''check if the creation of the new agreement fails, because the input data should be larger than 0'''
    for _ in range(7):
        try:
            chain = Chain()
            now = chain.time()
            startAgreement = now + 10000
            deploy.createAgreement('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', possibilities[0], possibilities[1], possibilities[2], startAgreement, {'from': accounts[signee], 'value': amount_sent})
        except Exception as e:
            assert e.message[50:] == 'All input data must be larger than 0'

@pytest.mark.parametrize("_amount", [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])    
def test_new_agreement_fails_require_msg_value_larger_than_amount(deploy, _amount):
    '''check if the creation of the new agreement fails, because the msg.value should be larger or equal to amount sent'''
    try:
        chain = Chain()
        now = chain.time()
        startAgreement = now + 10000
        deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[signee], 'value': _amount})
    except Exception as e:
            assert e.message[50:] == 'Deposit has to be at least the size of the amount'

def test_new_agreement_fails_require_agreementStart_larger_than_block_timestamp(deploy):
    '''check if the creation of the new agreement fails, because the _startOfTheAgreement should be larger than block.amount'''
    try:
        chain = Chain()
        now = chain.time()
        startAgreement = now - 10000
        deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[signee], 'value': amount_sent})
    except Exception as e:
            assert e.message[50:] == "The agreement can't be created in the past"

'''TESTING CREATEAGREEMENT FUNCTION AGREEMENT 2'''


def test_exactAgreement_id_2(deploy):
    '''check if the first id of the agreement is zero'''
    assert deploy.exactAgreement(agreements_number_2)[0] == str(agreements_number_2)

def test_exactAgreement_signee_2(deploy):
    '''check if the first address of the agreement's signee is the same as the signee'''
    assert deploy.exactAgreement(agreements_number_2)[1] == accounts[signee_2]

def test_exactAgreement_receiver_2(deploy):
    '''check if the first address of the agreement's receiver is the same as the accounts[0]'''
    assert deploy.exactAgreement(agreements_number_2)[2] == accounts[receiver_2]

def test_exactAgreement_amount_2(deploy):
    '''check if the amount of the agreement is 2'''
    assert deploy.exactAgreement(agreements_number_2)[3] == amount_sent_2  

def test_exactAgreement_initialize_transactionCreated_2(deploy):
    '''check if the transactionCreated is 0'''
    assert deploy.exactAgreement(agreements_number_2)[4] == '0'

def test_exactAgreement_deposit_2(deploy):
    '''check if the initial amount of the deposit is 0'''
    assert deploy.exactAgreement(agreements_number_2)[5] == amount_sent_2

def test_exactAgreement_status_2(deploy):
    '''check if the initial status is equal to "Created"'''
    assert deploy.exactAgreement(agreements_number_2)[6] == 'Created'

def test_exactAgreement_approved_2(deploy):
    '''check if the initial approve "Not Confirmed"'''
    assert deploy.exactAgreement(agreements_number_2)[7] == 'Not Confirmed'

def test_exactAgreement_time_creation_2(deploy):
    '''check if the initial time creation is block.timestamp'''
    assert deploy.exactAgreement(agreements_number_2)[8] == deploy.exactAgreement(1)[8]

def test_exactAgreement_every_time_unit_2(deploy):
    '''check if the initial every time unit is every_period'''
    assert deploy.exactAgreement(agreements_number_2)[9] >= seconds_in_day * initial_every_time_unit_2

def test_exactAgreement_position_period_2(deploy):
    '''check if the initial position period is 0'''
    assert deploy.exactAgreement(agreements_number_2)[10] == '0'

def test_exactAgreement_how_long_2(deploy):
    '''check if the initial how long is agreement_duration'''
    assert deploy.exactAgreement(agreements_number_2)[11] >= seconds_in_day * initial_howLong_2


'''TESTING EVENT AGREEMENTINFO INSIDE CREATEAGREEMENT FUNCTION'''



def test_event_AgreementInfo_agreementId(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementId'''
    assert new_agreement.events[0]["agreementId"] == deploy.exactAgreement(agreements_number)[0]

def test_event_AgreementInfo_agreementSignee(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementSignee'''
    assert new_agreement.events[0]["agreementSignee"] == deploy.exactAgreement(agreements_number)[1]

def test_event_AgreementInfo_agreementReceiver(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementReceiver'''
    assert new_agreement.events[0]["agreementReceiver"] == deploy.exactAgreement(agreements_number)[2]

def test_event_AgreementInfo_agreementAmount(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementAmount'''
    assert new_agreement.events[0]["agreementAmount"] == deploy.exactAgreement(agreements_number)[3]

def test_event_AgreementInfo_transactionCreated(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly TransactionCreated'''
    assert new_agreement.events[0]["agreementTransactionCreated"] == deploy.exactAgreement(agreements_number)[4]

def test_event_AgreementInfo_agreementDeposit(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementDeposit'''
    assert new_agreement.events[0]["agreementDeposit"] == deploy.exactAgreement(agreements_number)[5]

def test_event_AgreementInfo_agreementStatus(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementStatus'''
    assert new_agreement.events[0]["agreementStatus"] == deploy.exactAgreement(agreements_number)[6]

def test_event_AgreementInfo_agreementApproved(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementApproved'''
    assert new_agreement.events[0]["agreementApproved"] == deploy.exactAgreement(agreements_number)[7]

def test_event_AgreementInfo_agreementTimeCreation(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementTimeCreation'''
    assert new_agreement.events[0]["agreementTimeCreation"] == deploy.exactAgreement(agreements_number)[8]

def test_event_AgreementInfo_agreementTimePeriods(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementTimePeriods in seconds'''
    assert new_agreement.events[0]["agreementTimePeriods"] == deploy.exactAgreement(agreements_number)[9]

def test_event_AgreementInfo_agreementPositionPeriod(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementPositionPeriod in days'''
    assert new_agreement.events[0]["agreementPositionPeriod"] == deploy.exactAgreement(agreements_number)[10]

def test_event_AgreementInfo_agreementTimeDuration(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementTimeDuration in seconds'''
    assert new_agreement.events[0]["agreementTimeDuration"] == deploy.exactAgreement(agreements_number)[11]

def test_event_AgreementInfo_equals_Agreement(deploy, new_agreement):
    '''check if the length of the AgreementInfo elements is the same as in exactAgreements'''
    agreement = deploy.exactAgreement(0)
    event = new_agreement.events[0][0]
    assert len(agreement) == len(event)
    


'''TESTING MYSENDERAGREEMENTS FUNCTION'''



def test_mySenderAgreements_emits_correct_id_accounts_1(deploy):
    '''check if the mapping mySenderAgreements emits correct agreementId for the first element in the mapping of address signee'''
    assert deploy.mySenderAgreements(accounts[signee], 0) == '0'

def test_mySenderAgreements_emits_correct_id_accounts_2(deploy):
    '''check if the mapping mySenderAgreements is returning correctly the ids'''
    assert deploy.mySenderAgreements(accounts[signee], 1) == '1'




'''TESTING MYRECEIVERAGREEMENTS FUNCTION'''




def test_myReceiverAgreements_emits_correct_id_agreement_1(deploy):
    '''check if the mapping myReceiverAgreements emits correct agreementId for the first element in the mapping of address 0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'''
    assert deploy.myReceiverAgreements(accounts[receiver], 0) == '0'

def test_myReceiverAgreements_emits_correct_id_agreement_2(deploy):
    '''check if the mapping myReceiverAgreements is returning correctly the ids'''
    assert deploy.myReceiverAgreements(accounts[receiver], 1) == '1'




''' TESTING confirmAgreement FUNCTION'''



def test_confirmAgreement_agreement_already_confirmed(deploy):
    '''check if the confirmAgreement checks if the agreement is already confirmed'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    function_enabled = deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement is already confirmed'

@pytest.mark.parametrize("seconds_sleep",  [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_confirmAgreement_fail_require_2(deploy, seconds_sleep):
    '''check if the confirmAgreement fails if the receiver wants to confirm an agreement that has ended'''
    try:
        chain = Chain()
        chain.sleep(seconds_sleep)
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})        
    except Exception as e:
        assert e.message[50:] == "The agreement's deadline has ended"

@pytest.mark.parametrize("seconds_sleep", [0, less_than_agreement_duration[0], less_than_agreement_duration[1], less_than_agreement_duration[2]])
def test_confirmAgreement_fail_require_2_pair(deploy, seconds_sleep):
    '''check if the confirmAgreement works fine'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[7] == 'Confirmed'    
 
@pytest.mark.parametrize("accounts_number", [without_receiver[0], without_receiver[1], without_receiver[2]])
def test_confirmAgreement_fail_require_1(deploy, accounts_number):
    '''check if the confirmAgreement fails if the receiver is wrong'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[accounts_number]})        
    except Exception as e:
        assert e.message[50:] == "Only the receiver can confirm the agreement"

@pytest.mark.parametrize("accounts_number", [receiver])
def test_confirmAgreement_fail_require_1_pair(deploy, accounts_number):
    '''check if the confirmAgreement fails if the receiver is wrong'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[accounts_number]})        
    except Exception as e:
        assert e.message[50:] != "Only the receiver can confirm the agreement"

def test_confirmAgreement_agreement_status_confirmed(deploy):
    '''check if the confirmAgreement changes status to "Confirmed"'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[7] == 'Confirmed'

def test_confirmAgreement_notify_user(deploy):
    '''check if the confirmAgreement emits an event '''
    function_initialize = deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]}) 
    assert function_initialize.events[0][0]['message'] == "The agreement was confirmed"

def test_confirmAgreement_terminated_notify_user(deploy):
    '''check if the confirmAgreement emits an event when already terminated'''
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    function_initialize = deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]}) 
    assert function_initialize.events[0][0]['message'] == "The agreement is already terminated"



'''TESTING TERMINATE CONTRACT'''



#here we are contacting sendPayment prior terminating the agreement (it should be the same otherwise)

def test_terminateContract_emit_Terminated_initial_status_activated_already_terminated(deploy):
    '''checking if the event Terminated has been emitted as "This agreement has been terminated" when you want to terminate a contract'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    function_enabled = deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement is already terminated'

@pytest.mark.parametrize("accounts_number", [without_signee[0], without_signee[1], without_signee[2]])
def test_terminateContract_fails_require_wrong_address_initial_status_activated(deploy, accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
        #wrong sender's address
        deploy.terminateContract(agreements_number, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] == "Only the owner can terminate the agreement"

@pytest.mark.parametrize("accounts_number", [signee])
def test_terminateContract_fails_require_wrong_address_initial_status_activated_pair(deploy, accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
        #wrong sender's address
        deploy.terminateContract(agreements_number, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] != "Only the owner can terminate the agreement"

def test_terminateContract_function_change_status_terminated(deploy):
    '''check if the function terminateContract changes status of the agreement to "Terminated"'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    assert deploy.exactAgreement(agreements_number)[6] == 'Terminated'

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
@pytest.mark.parametrize("value_sent", [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_transfer_deposit_back_to_signee(deploy, value_sent, time):
    '''check if the deposit is transfered back to the signee'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    balance_signee = accounts[signee].balance() 
    chain = Chain()
    chain.sleep(time)
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    deploy.withdrawAsTheSignee(agreements_number, {'from': accounts[signee]})
    assert accounts[signee].balance() == balance_signee + amount_sent

@pytest.mark.parametrize("value_sent", [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_transfer_deposit_back_to_signee_pair(deploy, value_sent):
    '''check if the deposit is not transfered back to the signee'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
        deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    except Exception as e:
        assert e.message[50:] == "The deposit is not the same as the agreed in the terms"

@pytest.mark.parametrize("value_sent", [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_transfer_deposit_back_to_receiver(deploy, value_sent):
    '''check if the deposit is transfered back to the receiver'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    balance_receiver = accounts[receiver].balance() 
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + amount_sent

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])    
@pytest.mark.parametrize("value_sent", [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_transfer_msg_value_back_to_signee_2(deploy, value_sent, time):
    '''check if the deposit is transfered back to the signee'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    balance_signee = accounts[signee].balance() 
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*value_sent})
    chain = Chain()
    chain.sleep(time)
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    deploy.withdrawAsTheSignee(agreements_number, {'from': accounts[signee]})
    assert accounts[signee].balance() == balance_signee - 4*value_sent + amount_sent

@pytest.mark.parametrize("value_sent", [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_transfer_msg_value_back_to_receiver_2(deploy, value_sent):
    '''check if the deposit is transfered back to the receiver'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    balance_receiver = accounts[receiver].balance()  
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*value_sent})
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + 4*value_sent + amount_sent

def test_terminateContract_function_change_status_terminated_deposit(deploy):
    '''check if the function terminateContract changes deposit to zero"'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    assert deploy.exactAgreement(agreements_number)[5] == '0'

def test_terminateContract_emit_Terminated_initial_status_activated(deploy):
    '''checking if the event Terminated has been emitted as "This agreement has been terminated" when you want to terminate a contract'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    function_enabled = deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement has been terminated'

#here we aren't contacting sendPayments prior terminating the contract

@pytest.mark.parametrize("accounts_number", [without_signee[0], without_signee[1], without_signee[2]])
def test_terminateContract_fails_require_wrong_address_initial_status_activated_without_sendPayments(deploy, accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        #wrong sender's address
        deploy.terminateContract(agreements_number, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] == "Only the owner can terminate the agreement"

@pytest.mark.parametrize("accounts_number", [signee])
def test_terminateContract_fails_require_wrong_address_initial_status_activated_without_sendPayments_pair(deploy, accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        #wrong sender's address
        deploy.terminateContract(agreements_number, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] != "Only the owner can terminate the agreement"

def test_terminateContract_function_change_status_terminated_without_sendPayments(deploy):
    '''check if the function terminateContract changes status of the agreement to "Terminated"'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    assert deploy.exactAgreement(agreements_number)[6] == 'Terminated'

def test_transfer_deposit_back_to_signee_2(deploy):
    '''check if the deposit is transfered back to the signee'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    balance_signee = accounts[signee].balance() 
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    assert accounts[signee].balance() == balance_signee

def test_terminateContract_function_change_status_terminated_deposit_2(deploy):
    '''check if the function terminateContract changes deposit to 0'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    assert deploy.exactAgreement(agreements_number)[5] == '0'

def test_terminateContract_emit_Terminated_initial_status_activated_without_sendPayments(deploy):
    '''checking if the event Terminated has been emitted as "This agreement has been terminated" when you want to terminate a contract'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    function_enabled = deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement has been terminated'



'''TESTING SENDPAYMENT, INITIALIZINGPOSITIONPERIOD AND TIMENOTBREACHED FUNCTIONS'''


#can we check the require, revert
#What happens if the unix timestamp is larger or equal to 19th Jan 2038?
#what happens if teh transaction cannot be sent?

#Checking the require statements 

@pytest.mark.parametrize("accounts_number", [without_signee[0], without_signee[1], without_signee[2]])
def test_sendPayments_fails_require_wrong_address(deploy, accounts_number):
    '''check if the sendPayments fails, because exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        #wrong signer's address
        deploy.sendPayment(agreements_number, {'from': accounts[accounts_number], 'value': amount_sent})
    except Exception as e:
        assert e.message[50:] == "Only the owner can pay the agreement's terms"

@pytest.mark.parametrize("accounts_number", [signee])
def test_sendPayments_fails_require_wrong_address_pair(deploy, accounts_number):
    '''check if the sendPayments fails, because exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        #wrong signer's address
        deploy.sendPayment(agreements_number, {'from': accounts[accounts_number], 'value': amount_sent})
    except Exception as e:
        assert e.message[50:] != "Only the owner can pay the agreement's terms"

def test_sendPayments_fails_require_not_confirmed(deploy):
    '''check if the sendPayments fails, because exactAgreement[_id].approved)) == "Confirmed" in the require statement'''
    try:
        #no confirmation
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    except Exception as e:
        assert e.message[50:] == "The receiver has to confirm the contract"

#Checking when the agreement's status is "Created"

def test_sendPayments_require_statement_fails_agreement_not_started(deploy):
    '''check if the require statement fails when the agreement hasn't started yet'''
    try:
        chain = Chain()
        now = chain.time()
        _startAgreement = now + 10
        
        deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, _startAgreement, {'from': accounts[signee], 'value': amount_sent})
        assert deploy.exactAgreement(2)[8] == _startAgreement
        deploy.confirmAgreement(2, {'from': accounts[receiver]})
        deploy.sendPayment(2, {'from': accounts[signee], 'value': amount_sent})
    except Exception as e:
        assert e.message[50:] == "The agreement hasn't started yet"

@pytest.mark.parametrize("seconds_sleep",  [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_sendPayments_require_statement_fails_agreement_not_ended(deploy, seconds_sleep):
    '''check if the require statement fails when the agreement's deadline has ended'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        chain = Chain()
        chain.sleep(seconds_sleep)
        #now = chain.time()
        #assert deploy.exactAgreement(agreements_number)[8] >= now
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})      
    except Exception as e:
        assert e.message[50:] == "This agreement's deadline has ended"

@pytest.mark.parametrize("seconds_sleep",  [less_than_agreement_duration[0], less_than_agreement_duration[1], less_than_agreement_duration[2]])
def test_sendPayments_require_statement_fails_agreement_not_ended_pair(deploy, seconds_sleep):
    '''check if the require statement works fine when the agreement's deadline has not ended'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Activated'      
  
@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_sendPayments_fails_require_smaller_deposit_initial_status_created(deploy, value_sent):
    '''check if the sendPayments fails, because exactAgreement[_id].amount <= msg.value in the require statement'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        #'value' is smaller than it should be
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    except Exception as e:
        assert e.message[50:] == "The deposit is not the same as the agreed in the terms"

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_sendPayments_fails_require_smaller_deposit_initial_status_created_pair(deploy, value_sent):
    '''checking if the status is changed to "Activated" when msg.value is larger or equal to agreedDeposit'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Activated'

def test_sendPayments_change_initializePeriod_initial_status_created(deploy):
    '''checking if the InitializedPeriod is initialize (sum of agreementTimeCreation and everyTimeUnit) when msg.value is larger or equal to agreedDeposit'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[10] == deploy.exactAgreement(0)[8] + deploy.exactAgreement(0)[9]

def test_sendPayments_emit_NotifyUser_initial_status_created(deploy):
    '''checking if the event has been emitted as "We have activate the agreement" when msg.value is larger or equal to agreedDeposit'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    function_enabled = deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    message = function_enabled.events[0][0]['message']
    assert message == 'We have activate the agreement'



#Checking when the agreement's status is "Activated"
#if the transaction sent was on time

def test_timeNotBreached(deploy):
    '''check if the timeNotBreached function correctly increments positionPeriod. This is for checking inside sendPayments function'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    new_agreement_position = deploy.exactAgreement(0)[10]
    #the contract has been activated, now send the the money again
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})    
    assert deploy.exactAgreement(agreements_number)[10] == new_agreement_position + deploy.exactAgreement(0)[9]

def test_transactionCreated_updated(deploy):
    '''check if the time of the call to function sendPayment is stored'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[4] != '0'

def test_transactionCreated_updated_once_again(deploy):
    '''check if the time of the call to function sendPayment changes after another call to this function'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()  
    chain.sleep(3)
    first_call = deploy.exactAgreement(agreements_number)[4]
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[4] != first_call

    #if the amount <= msg.value
 
@pytest.mark.parametrize("seconds_sleep",  [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_timeNotBreached_fail_if_statement(deploy, seconds_sleep):
    '''check if the timeNotBreached fails because transaction was sent after the agreement's deadline - it fails because of the check in the confirmAgreement function'''
    try:
        chain = Chain()
        chain.sleep(seconds_sleep)
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    except Exception as e:        
        assert e.message[50:] == "The agreement's deadline has ended"

@pytest.mark.parametrize("seconds_sleep",  [less_than_agreement_duration[0], less_than_agreement_duration[1], less_than_agreement_duration[2]])
def test_timeNotBreached_fail_if_statement_pair(deploy, seconds_sleep):
    '''check if the timeNotBreached works fine when confirmAgreement check is passed'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Activated'

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value(deploy, value_sent):
    '''check if the msg.value is sent when amount <= msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    balance_receiver = accounts[receiver].balance() 
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + value_sent

@pytest.mark.parametrize("value_sent",  [amount_sent])
@pytest.mark.parametrize("value_decreased",  [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value_pair(deploy, value_sent, value_decreased):
    '''check if the msg.value is not sent when amount <= msg.value in the timeNotBreached, the contract terminates'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent - value_decreased}) 
    assert deploy.exactAgreement(agreements_number)[6] == 'Terminated'

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value_check_signee(deploy, value_sent):
    '''check if the balance of the signee is changed when amount <= msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    balance_signee = accounts[signee].balance() 
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert accounts[signee].balance() == balance_signee - value_sent

@pytest.mark.parametrize("value_sent",  [amount_sent])
@pytest.mark.parametrize("value_decreased",  [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value_check_signee_pair(deploy, value_sent, value_decreased):
    '''check if the balance of the signee is the same when amount > msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    balance_signee = accounts[signee].balance() 
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent - value_decreased}) 
    deploy.withdrawAsTheSignee(agreements_number, {'from': accounts[signee]})
    assert accounts[signee].balance() == balance_signee + value_sent
   
def test_timeNotBreached_value_large_amount_emit_NotifyUser(deploy):
    '''check if the event NotifyUser is emitted when amount <= msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    #the contract has been activated, now send the money again
    function_initialize = deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert function_initialize.events[0][0]['message'] == "Transaction was sent to the receiver"

    #if the amount > msg.value

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_status(deploy, value_sent):
    '''check if the status is changed when amount > msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    #the contract has been activated, now send the smaller quantity of money again
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    assert deploy.exactAgreement(agreements_number)[6] == "Terminated"

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_status_pair(deploy, value_sent):
    '''check if the status stays the same when amount < msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    assert deploy.exactAgreement(agreements_number)[6] == "Activated"

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_send_deposit(deploy, value_sent):
    '''check if the deposit is sent to the receiver when amount > msg.value in the timeNotBreached'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
        deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})
    except Exception as e :
        assert e.message[50:] == "There aren't any funds to withdraw"

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_send_deposit_pair(deploy, value_sent):
    '''check if the deposit isn't sent (but the sending value) to the receiver when amount < msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance() 
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]}) 
    assert accounts[receiver].balance() == balance_receiver + value_sent

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_deposit_equals_zero(deploy, value_sent):
    '''check if the deposit is back on zero when amount > msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert deploy.exactAgreement(agreements_number)[5] == "0"

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_deposit_equals_zero_pair(deploy, value_sent):
    '''check if the deposit is not sent back on zero when amount < msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert deploy.exactAgreement(agreements_number)[5] != "0"

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_return_transaction(deploy, value_sent):
    '''check if the transaction is sent back to the signee when amount > msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})  
    balance_signee = accounts[signee].balance() 
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    deploy.withdrawAsTheSignee(agreements_number, {'from': accounts[signee]})
    assert accounts[signee].balance() == balance_signee + amount_sent

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_return_transaction_pair(deploy, value_sent):
    '''check if the transaction is reduced from the signee when amount < msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})  
    balance_signee = accounts[signee].balance() 
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent}) 
    assert accounts[signee].balance() == balance_signee - value_sent

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])    
def test_timeNotBreached_value_smaller_amount_emit_Terminated(deploy, value_sent):
    '''check if the event Terminated is emitted when amount > msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    #the contract has been activated, now send the smaller quantity of money again
    function_initialize = deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    assert function_initialize.events[0][0]['message'] == "This agreement was terminated due to different payment than in the terms"

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]]) 
def test_timeNotBreached_value_smaller_amount_emit_Terminated_pair(deploy, value_sent):
    '''check if the event NotifyUser is emitted when amount < msg.value in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    function_initialize = deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': value_sent})
    assert function_initialize.events[0][0]['message'] == "Transaction was sent to the receiver"

    

#if the transaction wasn't sent on time

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_received_on_time_false_1st_part_if_statement(deploy, seconds_sleep):
    '''check if the timeNotBreached returns false, when transactionCreated > positionPeriod'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Terminated' 

@pytest.mark.parametrize("seconds_sleep",  [60*60*24*8, 60*60*24*9, 60*60*24*10])
def test_timeNotBreached_received_on_time_false_2nd_part_if_statement(deploy, seconds_sleep):
    '''check if the timeNotBreached returns false, when transaction received wasn't on time'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Terminated'

@pytest.mark.parametrize("seconds_sleep",  [agreement_duration, 2629744, 26297440])
def test_timeNotBreached_breached_on_time_false_3rd_part_if_statement(deploy, seconds_sleep):
    '''check if the timeNotBreached returns false, when the deadline of the agreement has ended'''
    chain = Chain()
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    
    for _ in range(3):
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
        chain.sleep(60400)
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == "Terminated"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_status(deploy, seconds_sleep):
    '''check if the status is changed to Terminated when timeNotBreached is breached in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    assert deploy.exactAgreement(agreements_number)[6] == "Terminated"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_status_pair(deploy, seconds_sleep):
    '''check if the status is not changed to Terminated when timeNotBreached is not breached in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    assert deploy.exactAgreement(agreements_number)[6] == "Activated"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_send_deposit(deploy, seconds_sleep):
    '''check if the deposit is sent to the receiver when timeNotBreached is breached in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent}) 
    deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + amount_sent

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_send_deposit_pair(deploy, seconds_sleep):
    '''check if the deposit isn't sent to the receiver (but the value is) when timeNotBreached is not breached in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent}) 
    deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + 4*amount_sent

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_deposit_equals_zero(deploy, seconds_sleep):
    '''check if the deposit is equal zero when timeNotBreached is breached in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    assert deploy.exactAgreement(agreements_number)[5] == "0"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_deposit_equals_zero_pair(deploy, seconds_sleep):
    '''check if the deposit is not equal zero when timeNotBreached is not breached in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    assert deploy.exactAgreement(agreements_number)[5] != "0"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_return_transaction(deploy, seconds_sleep):
    '''check if the transaction is sent back to the signee when timeNotBreached is breached in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})  
    balance_signee = accounts[signee].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    deploy.withdrawAsTheSignee(agreements_number, {'from': accounts[signee]})
    assert accounts[signee].balance() == balance_signee

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_return_transaction_pair(deploy, seconds_sleep):
    '''check if the transaction is not sent back to the signee (it's sent to the receiver) when timeNotBreached is not breached in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})  
    balance_signee = accounts[signee].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent}) 
    assert accounts[signee].balance() == balance_signee - amount_sent

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_emit_Terminated(deploy, seconds_sleep):
    '''check if the event Terminated is emitted when timeNotBreached is breached in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    function_initialize = deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert function_initialize.events[0][0]['message'] == "This agreement was terminated due to late payment"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_emit_Terminated_pair(deploy, seconds_sleep):
    '''check if the event Terminated is not emitted when timeNotBreached is not breached in the timeNotBreached'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    function_initialize = deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    assert function_initialize.events[0][0]['message'] != "This agreement was terminated due to late payment"

#Checking when the agreement's status is "Terminated"

def test_terminateContract_emit_Terminated_initial_status_terminated(deploy):
    '''check if the sendPayments emits correctly the message when the status is "Terminated"'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    with brownie.reverts("This agreement was already terminated"):
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})



''' TESTING WASCONTRACTBREACHED FUNCTION '''


 
@pytest.mark.parametrize("wrong_accounts",  [without_receiver[0], without_receiver[1], without_receiver[2]])
def test_wasContractBreached_require_receiver_equals_msg_sender(deploy, wrong_accounts):
    '''check if the wasContractBreached fails, because exactAgreement[_id].receiver == msg.sender is the require statement'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    with brownie.reverts("The receiver in the agreement's id isn't the same as the address you're logged in"):
        #wrong signee's address
        deploy.wasContractBreached(agreements_number, {'from': accounts[wrong_accounts]})

@pytest.mark.parametrize("right_accounts",  [receiver])
def test_wasContractBreached_require_receiver_equals_msg_sender_pair(deploy, right_accounts):
    '''check if the wasContractBreached doesn't fail'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
        deploy.wasContractBreached(agreements_number, {'from': accounts[right_accounts]})
    except Exception as e:        
        assert e.message[50:] == "This agreement's deadline has ended"

def test_wasContractBreached_fail_if_statement_in_timeNotBreached(deploy):
    '''check if the timeNotBreached fails because transaction was sent after the agreement's deadline - it fails because of the check in the confirmAgreement function'''
    try:
        deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
        chain = Chain()
        chain.sleep(2629800)
        deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
        deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    except Exception as e:        
        assert e.message[50:] == "This agreement's deadline has ended"

#if timeNotBreached is True

def test_wasContractBreached_timeNotBreached_true_emit_NotifyUser(deploy):
    '''check if the wasContractBreached function when timeNotBreached is true, emits NotifyUser'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement wasn't breached"

#check 3 parts of the if statement in timeWasntBreached

#if timeNotBreached is False
@pytest.mark.skip(reason='doesn not work correctly')
#seconds_sleep must be more then agreement_duration, but less then agreement_duration + 7 days
@pytest.mark.parametrize("seconds_sleep",  [2629761, 3000000, 3234542, 3234543, 9999999])
def test_wasContractBreached_received_on_time_false(deploy, seconds_sleep):
    '''check if the wasContractBreached returns false, when transaction received wasn't on time, but doesn't wait 7 days for withdraw'''
    try:
        deploy.confirmAgreement(1, {'from': accounts[receiver_2]})
        deploy.sendPayment(1, {'from': accounts[signee_2], 'value': amount_sent})
        chain = Chain()
        chain.sleep(seconds_sleep)
        deploy.wasContractBreached(1, {'from': accounts[receiver_2]})
    #deploy.sendPayment(1, {'from': signee, 'value': amount_sent})
    #deploy.wasContractBreached(1, {'from': receiver})

    #function_initialize = deploy.wasContractBreached(1, {'from': receiver})
    #assert function_initialize.events[0][0]['message'] == "The agreement wasn't breached"

    #assert deploy.exactAgreement(1)[6] == "Terminated"
    except Exception as e:        
        assert e.message[50:] == "You have to wait at least 7 days after breached deadline to withdraw the deposit"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_Terminated(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, changes status to Terminated'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[6] == "Terminated"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_Terminated_pair(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't change status to Terminated'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[6] == "Activated"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_send_deposit(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, sends a deposit to the receiver'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance()
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + amount_sent

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_send_deposit_pair(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't send a deposit to the receiver'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance()
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + 4*amount_sent

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_deposit_equals_zero_1(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, changes deposit to 0'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[5] == '0'

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_deposit_equals_zero_1_pair(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't change deposit to 0'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[5] != '0'

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_emit_Terminated(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, emits NotifyUser'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "This agreement is already terminated"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_emit_Terminated_pair(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't emit NotifyUser'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] != "This agreement is already terminated"

def test_wasContractBreached_agreement_not_activated(deploy):
    '''check if the wasContractBreached function emits NotifyUser when timeNotBreached is false'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement wasn't breached"

def test_wasContractBreached_status_created_notify_user(deploy):
    '''check if the wasContractBreached function emits NotifyUser when exactAgreement[_id].agreementTimeCreation + (6*60*60*24) > block.timestamp'''
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement wasn't breached"

@pytest.mark.skip(reason='doesn not work correctly')
def test_wasContractBreached_status_created_require_fails(deploy):
    '''check if the wasContractBreached function emits NotifyUser when exactAgreement[_id].agreementTimeCreation + (6*60*60*24) > block.timestamp'''
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])    
def test_wasContractBreached_status_created_status_terminated(deploy, seconds_sleep):
    '''check if the wasContractBreached function emits NotifyUser when exactAgreement[_id].agreementTimeCreation + (6*60*60*24) > block.timestamp fails'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[6] == "Terminated" 

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])    
def test_wasContractBreached_status_created_status_terminated(deploy, seconds_sleep):
    '''check if the wasContractBreached function emits NotifyUser when exactAgreement[_id].agreementTimeCreation + (6*60*60*24) > block.timestamp fails'''
    balance_receiver = accounts[receiver].balance()
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + amount_sent

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]]) 
def test_wasContractBreached_status_created_deposit_zero(deploy, seconds_sleep):
    '''check if the wasContractBreached function emits NotifyUser when exactAgreement[_id].agreementTimeCreation + (6*60*60*24) > block.timestamp fails'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[5] == '0'

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_status_created_false_emit_Terminated(deploy, seconds_sleep):
    '''check if the wasContractBreached function emits NotifyUser when exactAgreement[_id].agreementTimeCreation + (6*60*60*24) > block.timestamp fails'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "This agreement has been terminated"



'''TEST WITHDRAWASTHERECEIVER'''



@pytest.mark.parametrize("wrong_account", [without_receiver[0], without_receiver[1], without_receiver[2]])
def test_withdrawAsTheReceiver_first_reguire_fails(deploy, wrong_account):
    '''require statement exactAgreement[_id].receiver == msg.sender fails'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    with brownie.reverts("Your logged in address isn't the same as the contract's receiver address"):
        deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[wrong_account]})

def test_withdrawAsTheReceiver_first_reguire_fails_pair(deploy):
    '''require statement exactAgreement[_id].receiver == msg.sender doesn't fail'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    function_initialize = deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "We have transfered ethers"

def test_withdrawAsTheReceiver_second_reguire_fails_case_1(deploy):
    '''require statement withdraw_receiver[exactAgreement[_id].receiver] > 0 fails, because we send only the deposit'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    with brownie.reverts("There aren't any funds to withdraw"):
        deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})

def test_withdrawAsTheReceiver_second_reguire_fails_case_2(deploy):
    '''require statement withdraw_receiver[exactAgreement[_id].receiver] > 0 fails, because we already withdraw the funds'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})
    with brownie.reverts("There aren't any funds to withdraw"):
        deploy.withdrawAsTheReceiver(agreements_number, {'from': accounts[receiver]})



'''TEST WITHDRAWASTHESIGNEE'''



@pytest.mark.parametrize("wrong_account", [without_signee[0], without_signee[1], without_signee[2]])
def test_withdrawAsTheSignee_first_reguire_fails(deploy, wrong_account):
    '''require statement exactAgreement[_id].signee == msg.sender fails'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    with brownie.reverts("Your logged in address isn't the same as the contract's signee address"):
        deploy.withdrawAsTheSignee(agreements_number, {'from': accounts[wrong_account]})

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_withdrawAsTheSignee_first_reguire_fails_pair(deploy, time):
    '''require statement exactAgreement[_id].signee == msg.sender doesn't fail'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    chain = Chain()
    chain.sleep(time)
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    function_initialize = deploy.withdrawAsTheSignee(agreements_number, {'from': accounts[signee]})
    assert function_initialize.events[0][0]['message'] == "We have transfered ethers"

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_withdrawAsTheSignee_second_reguire_fails(deploy, time):
    '''require statement withdraw_receiver[exactAgreement[_id].signee] > 0 fails, because we already withdraw the funds'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(time)
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    deploy.withdrawAsTheSignee(agreements_number, {'from': accounts[signee]})
    with brownie.reverts("There aren't any funds to withdraw"):
        deploy.withdrawAsTheSignee(agreements_number, {'from': accounts[signee]})



'''TEST GETWITHDRAWALRECEIVER'''




@pytest.mark.parametrize("wrong_account", [without_receiver[0], without_receiver[1], without_receiver[2]])
def test_getWithdrawalReceiver_reguire_fails(deploy, wrong_account):
    '''require statement exactAgreement[_id].receiver == msg.sender fails'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    with brownie.reverts("Your logged in address isn't the same as the contract's receiver address"):
        deploy.getWithdrawalReceiver(agreements_number, {'from': accounts[wrong_account]})

def test_getWithdrawalReceiver_reguire_fails_pair(deploy):
    '''require statement exactAgreement[_id].receiver == msg.sender doesn't fail'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    function_initialize = deploy.getWithdrawalReceiver(agreements_number, {'from': accounts[receiver]})
    assert function_initialize == 4*amount_sent

def test_getWithdrawalReceiver_uninitialize(deploy):
    '''check if the withdraw_receiver is empty after only sending the deposit'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    function_initialize = deploy.getWithdrawalReceiver(agreements_number, {'from': accounts[receiver]})
    assert function_initialize == 0




'''TEST GETWITHDRAWALSIGNEE'''



@pytest.mark.parametrize("wrong_account", [without_signee[0], without_signee[1], without_signee[2]])
def test_getWithdrawalsignee_reguire_fails(deploy, wrong_account):
    '''require statement exactAgreement[_id].signee == msg.sender fails'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    with brownie.reverts("Your logged in address isn't the same as the contract's signee address"):
        deploy.getWithdrawalSignee(agreements_number, {'from': accounts[wrong_account]})

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_getWithdrawalSignee_reguire_fails_pair(deploy, time):
    '''require statement exactAgreement[_id].signee == msg.sender doesn't fail'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': 4*amount_sent})
    chain = Chain()
    chain.sleep(time)
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    function_initialize = deploy.getWithdrawalSignee(agreements_number, {'from': accounts[signee]})
    assert function_initialize == amount_sent

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_getWithdrawalSignee_uninitialize(deploy, time):
    '''check if the withdraw_signee is not empty after only sending the deposit'''
    deploy.confirmAgreement(agreements_number, {'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[signee], 'value': amount_sent})
    chain = Chain()
    chain.sleep(time)
    deploy.terminateContract(agreements_number, {'from': accounts[signee]})
    function_initialize = deploy.getWithdrawalSignee(agreements_number, {'from': accounts[signee]})
    assert function_initialize == amount_sent