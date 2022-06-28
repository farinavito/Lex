from itertools import chain
import pytest
import brownie
from brownie import *
from brownie import accounts
from brownie.network import rpc
from brownie.network.state import Chain

#new agreement
commission = 1
sender = 1
receiver = 9
amount_sent = 10**1
every_period = 604800
agreement_duration = 2629743
initial_every_time_unit = 7
initial_howLong = 30
agreements_number = 1


without_sender = [sender + 1, sender + 2, sender + 3]
without_receiver = [receiver - 1, receiver - 2, receiver - 3]


less_than_amount_sent = [amount_sent - 5, amount_sent - 6, amount_sent - 7]
more_than_amount_sent = [amount_sent + 10**2, amount_sent + 10**3, amount_sent + 10**4]


less_than_every_period = [every_period - 10**2, every_period - 10**3, every_period - 10**4]
more_than_every_period = [every_period + 10**2, every_period + 10**3, every_period + 10**4]


less_than_agreement_duration = [agreement_duration - 10**2, agreement_duration - 10**3, agreement_duration - 10**4]
more_than_agreement_duration = [agreement_duration + 10**5, agreement_duration + 10**6, agreement_duration + 10**7]

seconds_in_day = 60 * 60 * 24

protectorOwnerAddress = 1
protectorWaitingToBeOwnerAddress = 2
addressProtector1 = 3
addressProtector2 = 4
addressProtector3 = 5
addressProtector4 = 6
addressProtector5 = 7

@pytest.fixture()
def deploy(AgreementBetweenSubjects, module_isolation):
    return AgreementBetweenSubjects.deploy({'from': accounts[0]})

@pytest.fixture(autouse=True)
def new_agreement(deploy, module_isolation):
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    return deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[sender], 'value': amount_sent})
    

sender_2 = sender
receiver_2 = receiver
amount_sent_2 = 10**1
every_period_2 = 2629743
agreement_duration_2 = 31556926
initial_every_time_unit_2 = 30
initial_howLong_2 = 364
agreements_number_2 = 2

@pytest.fixture(autouse=True)
def new_agreement_2(deploy, module_isolation):
    chain = Chain()
    now = chain.time()
    startAgreement = now + 4
    return deploy.createAgreement(accounts[receiver_2], amount_sent_2, every_period_2, agreement_duration_2, startAgreement, {'from': accounts[sender_2], 'value': amount_sent_2})



'''TESTING CREATEAGREEMENT FUNCTION AGREEMENT 1'''

    

def test_exactAgreement_id(deploy):
    '''check if the first id of the agreement is zero'''
    assert deploy.exactAgreement(agreements_number)[0] == str(agreements_number)

def test_exactAgreement_sender(deploy):
    '''check if the first address of the agreement's sender is the same as the sender'''
    assert deploy.exactAgreement(agreements_number)[1] == accounts[sender]

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

def test_exactAgreement_time_creation(deploy):
    '''check if the initial time creation is startAgreement'''
    assert deploy.exactAgreement(agreements_number)[7] == deploy.exactAgreement(1)[7]

def test_exactAgreement_every_time_unit(deploy):
    '''check if the initial every time unit is every_period'''
    assert deploy.exactAgreement(agreements_number)[8] >= seconds_in_day * initial_every_time_unit

def test_exactAgreement_position_period(deploy):
    '''check if the initial position period is 0'''
    assert deploy.exactAgreement(agreements_number)[9] == '0'

def test_exactAgreement_how_long(deploy):
    '''check if the initial how long is agreement_duration'''
    assert deploy.exactAgreement(agreements_number)[10] >= seconds_in_day * initial_howLong

def test_new_agreement_fails_require(deploy):
    '''check if the new agreement fails, because howLong > _everyTimeUnit in the require statement'''
    try:
        chain = Chain()
        now = chain.time()
        startAgreement = now + 10000
        #length of the agreement is longer than _everyTimeUnit
        deploy.createAgreement('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', 2, 500, 5, startAgreement, {'from': accounts[sender], 'value': amount_sent})
        pytest.fail("The try-except concept has failed in test_new_agreement_fails_require")
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
            deploy.createAgreement('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', possibilities[0], possibilities[1], possibilities[2], startAgreement, {'from': accounts[sender], 'value': amount_sent})
            pytest.fail("The try-except concept has failed in test_new_agreement_fails_require_larger_than_zero")
        except Exception as e:
            assert e.message[50:] == 'All input data must be larger than 0'

@pytest.mark.parametrize("_amount", [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])    
def test_new_agreement_fails_require_msg_value_larger_than_amount(deploy, _amount):
    '''check if the creation of the new agreement fails, because the msg.value should be larger or equal to amount sent'''
    try:
        chain = Chain()
        now = chain.time()
        startAgreement = now + 10000
        deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[sender], 'value': _amount})
        pytest.fail("The try-except concept has failed in test_new_agreement_fails_require_msg_value_larger_than_amount")
    except Exception as e:
            assert e.message[50:] == 'Deposit has to be at least the size of the amount'

def test_new_agreement_fails_require_agreementStart_larger_than_block_timestamp(deploy):
    '''check if the creation of the new agreement fails, because the _startOfTheAgreement should be larger than block.amount'''
    try:
        chain = Chain()
        now = chain.time()
        startAgreement = now - 10000
        deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[sender], 'value': amount_sent})
        pytest.fail("The try-except concept has failed in test_new_agreement_fails_require_agreementStart_larger_than_block_timestamp")
    except Exception as e:
            assert e.message[50:] == "The agreement can't be created in the past"

def test_event_id(deploy):
    '''check if the id in the emitted event is correct when a new agreement is created'''
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    function_initialize = deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[sender], 'value': amount_sent})
    assert function_initialize.events[0][0]['agreementId'] == 3

def test_event_sender(deploy):
    '''check if the sender in the emitted event is correct when a new agreement is created'''
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    function_initialize = deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[5], 'value': amount_sent})
    assert function_initialize.events[0][0]['agreementSender'] == accounts[5]

def test_event_receiver(deploy):
    '''check if the receiver in the emitted event is correct when a new agreement is created'''
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    function_initialize = deploy.createAgreement(accounts[7], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[5], 'value': amount_sent})
    assert function_initialize.events[0][0]['agreementReceiver'] == accounts[7]

def test_event_amount(deploy):
    '''check if the amount in the emitted event is correct when a new agreement is created'''
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    function_initialize = deploy.createAgreement(accounts[receiver], 15**10, every_period, agreement_duration, startAgreement, {'from': accounts[5], 'value': 18**10})
    assert function_initialize.events[0][0]['agreementAmount'] == 15**10

def test_event_TransactionCreated(deploy):
    '''check if the TransactionCreated in the emitted event is correct when a new agreement is created and msg.value is smaller than 1000'''
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    function_initialize = deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[5], 'value': 10**18})
    assert function_initialize.events[0][0]['agreementTransactionCreated'] == 0

def test_event_deposit(deploy):
    '''check if the deposit in the emitted event is correct when a new agreement is created and msg.value is smaller than 1000'''
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    function_initialize = deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[5], 'value': 10**18})
    assert function_initialize.events[0][0]['agreementDeposit'] == 10**18 

def test_event_status(deploy):
    '''check if the status in the emitted event is correct when a new agreement is created'''
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    function_initialize = deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[5], 'value': amount_sent})
    assert function_initialize.events[0][0]['agreementStatus'] == "Created"

def test_event_StartDate(deploy):
    '''check if the StartDate in the emitted event is correct when a new agreement is created'''
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    function_initialize = deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[5], 'value': amount_sent})
    assert function_initialize.events[0][0]['agreementStartDate'] == startAgreement

def test_event_TimePeriods(deploy):
    '''check if the TimePeriods in the emitted event is correct when a new agreement is created'''
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    function_initialize = deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[5], 'value': amount_sent})
    assert function_initialize.events[0][0]['agreementTimePeriods'] == every_period

def test_event_PositionPeriod(deploy):
    '''check if the PositionPeriod in the emitted event is correct when a new agreement is created'''
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    function_initialize = deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[5], 'value': amount_sent})
    assert function_initialize.events[0][0]['agreementPositionPeriod'] == "0"

def test_event_TimeDuration(deploy):
    '''check if the TimeDuration in the emitted event is correct when a new agreement is created'''
    chain = Chain()
    now = chain.time()
    startAgreement = now + 1
    function_initialize = deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, startAgreement, {'from': accounts[5], 'value': amount_sent})
    assert function_initialize.events[0][0]['agreementTimeDuration'] == agreement_duration 


'''TESTING CREATEAGREEMENT FUNCTION AGREEMENT 2'''



def test_exactAgreement_id_2(deploy):
    '''check if the first id of the agreement is zero'''
    assert deploy.exactAgreement(agreements_number_2)[0] == str(agreements_number_2)

def test_exactAgreement_sender_2(deploy):
    '''check if the first address of the agreement's sender is the same as the sender'''
    assert deploy.exactAgreement(agreements_number_2)[1] == accounts[sender_2]

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

def test_exactAgreement_time_creation_2(deploy):
    '''check if the initial time creation is block.timestamp'''
    assert deploy.exactAgreement(agreements_number_2)[7] == deploy.exactAgreement(2)[7]

def test_exactAgreement_every_time_unit_2(deploy):
    '''check if the initial every time unit is every_period'''
    assert deploy.exactAgreement(agreements_number_2)[8] >= seconds_in_day * initial_every_time_unit_2

def test_exactAgreement_position_period_2(deploy):
    '''check if the initial position period is 0'''
    assert deploy.exactAgreement(agreements_number_2)[9] == '0'

def test_exactAgreement_how_long_2(deploy):
    '''check if the initial how long is agreement_duration'''
    assert deploy.exactAgreement(agreements_number_2)[10] >= seconds_in_day * initial_howLong_2



'''TESTING EVENT AGREEMENTINFO INSIDE CREATEAGREEMENT FUNCTION'''



def test_event_AgreementInfo_agreementId(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementId'''
    assert new_agreement.events[0]["agreementId"] == deploy.exactAgreement(agreements_number)[0]

def test_event_AgreementInfo_agreementSender(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementsender'''
    assert new_agreement.events[0]["agreementSender"] == deploy.exactAgreement(agreements_number)[1]

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

def test_event_AgreementInfo_agreementStartDate(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementStartDate'''
    assert new_agreement.events[0]["agreementStartDate"] == deploy.exactAgreement(agreements_number)[7]

def test_event_AgreementInfo_agreementTimePeriods(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementTimePeriods in seconds'''
    assert new_agreement.events[0]["agreementTimePeriods"] == deploy.exactAgreement(agreements_number)[8]

def test_event_AgreementInfo_agreementPositionPeriod(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementPositionPeriod in days'''
    assert new_agreement.events[0]["agreementPositionPeriod"] == deploy.exactAgreement(agreements_number)[9]

def test_event_AgreementInfo_agreementTimeDuration(deploy, new_agreement):
    '''check if the event AgreementInfo emits correctly agreementTimeDuration in seconds'''
    assert new_agreement.events[0]["agreementTimeDuration"] == deploy.exactAgreement(agreements_number)[10]

def test_event_AgreementInfo_equals_Agreement(deploy, new_agreement):
    '''check if the length of the AgreementInfo elements is the same as in exactAgreements'''
    agreement = deploy.exactAgreement(0)
    event = new_agreement.events[0][0]
    assert len(agreement) == len(event)
    


'''TESTING MYSENDERAGREEMENTS FUNCTION'''



def test_mySenderAgreements_emits_correct_id_accounts_1(deploy):
    '''check if the mapping mySenderAgreements emits correct agreementId for the first element in the mapping of address sender'''
    assert deploy.mySenderAgreements(accounts[sender], 0) == '1'

def test_mySenderAgreements_emits_correct_id_accounts_2(deploy):
    '''check if the mapping mySenderAgreements is returning correctly the ids'''
    assert deploy.mySenderAgreements(accounts[sender], 1) == '2'



'''TESTING MYRECEIVERAGREEMENTS FUNCTION'''



def test_myReceiverAgreements_emits_correct_id_agreement_1(deploy):
    '''check if the mapping myReceiverAgreements emits correct agreementId for the first element in the mapping of address 0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'''
    assert deploy.myReceiverAgreements(accounts[receiver], 0) == '1'

def test_myReceiverAgreements_emits_correct_id_agreement_2(deploy):
    '''check if the mapping myReceiverAgreements is returning correctly the ids'''
    assert deploy.myReceiverAgreements(accounts[receiver], 1) == '2'



'''TESTING SENDPAYMENT, INITIALIZINGPOSITIONPERIOD AND TIMENOTBREACHED FUNCTIONS'''

#Checking the require statements 

@pytest.mark.parametrize("accounts_number", [without_sender[0], without_sender[1], without_sender[2]])
def test_sendPayments_fails_require_wrong_address(deploy, accounts_number):
    '''check if the sendPayments fails, because exactAgreement[_id].sender == msg.sender in the require statement'''
    try:
        #wrong signer's address
        deploy.sendPayment(agreements_number, {'from': accounts[accounts_number], 'value': amount_sent})
        pytest.fail("The try-except concept has failed in test_sendPayments_fails_require_wrong_address")
    except Exception as e:
        assert e.message[50:] == "Only the sender can pay the agreement's terms"

@pytest.mark.parametrize("accounts_number", [sender])
def test_sendPayments_fails_require_wrong_address_pair(deploy, accounts_number):
    '''check if the sendPayments doesn't fail, because exactAgreement[_id].sender == msg.sender in the require statement'''
    #right signer's address
    deploy.sendPayment(agreements_number, {'from': accounts[accounts_number], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Activated'
        

#Checking when the agreement's status is "Created"
def test_sendPayments_require_statement_fails_agreement_not_started(deploy):
    '''check if the require statement fails when the agreement hasn't started yet'''
    try:
        chain = Chain()
        now = chain.time()
        _startAgreement = now + 10
        
        deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, _startAgreement, {'from': accounts[sender], 'value': amount_sent})
        deploy.sendPayment(3, {'from': accounts[sender], 'value': amount_sent})
        pytest.fail("The try-except concept has failed in test_sendPayments_require_statement_fails_agreement_not_started")
    except Exception as e:
        assert e.message[50:] == "The agreement hasn't started yet"

def test_sendPayments_require_statement_fails_agreement_not_started_pair(deploy):
    '''check if the require statement does not fail when the agreement has started'''
    chain = Chain()
    _now = chain.time()
    deploy.createAgreement(accounts[receiver], amount_sent, every_period, agreement_duration, _now, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(3, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(3)[6] == 'Activated'

@pytest.mark.parametrize("seconds_sleep",  [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_sendPayments_require_statement_fails_agreement_not_ended(deploy, seconds_sleep):
    '''check if the require statement fails when the agreement's deadline has ended'''
    try:
        chain = Chain()
        chain.sleep(seconds_sleep)
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
        pytest.fail("The try-except concept has failed in test_sendPayments_require_statement_fails_agreement_not_ended")      
    except Exception as e:
        assert e.message[50:] == "The agreement's deadline has ended"

@pytest.mark.parametrize("seconds_sleep",  [less_than_agreement_duration[0], less_than_agreement_duration[1], less_than_agreement_duration[2]])
def test_sendPayments_require_statement_fails_agreement_not_ended_pair(deploy, seconds_sleep):
    '''check if the require statement works fine when the agreement's deadline has not ended'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Activated'      

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_sendPayments_fails_require_smaller_deposit_initial_status_created(deploy, value_sent):
    '''check if the sendPayments fails, because exactAgreement[_id].amount <= msg.value in the require statement'''
    try:
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
        pytest.fail("The try-except concept has failed in test_sendPayments_fails_require_smaller_deposit_initial_status_created") 
    except Exception as e:
        assert e.message[50:] == "The deposit is not the same as agreed in the terms"

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_sendPayments_fails_require_smaller_deposit_initial_status_created_pair(deploy, value_sent):
    '''checking if the status is changed to "Activated" when msg.value is larger or equal to agreedDeposit'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Activated'

def test_sendPayments_change_initializePeriod_initial_status_created(deploy):
    '''checking if the InitializedPeriod is initialize (sum of agreementStartDate and everyTimeUnit) when msg.value is larger or equal to agreedDeposit'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[9] == deploy.exactAgreement(1)[7] + deploy.exactAgreement(1)[8]

def test_sendPayments_emit_NotifyUser_initial_status_created(deploy):
    '''checking if the event has been emitted as "The agreement has been activated" when msg.value is larger or equal to agreedDeposit'''
    function_enabled = deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    message = function_enabled.events[0][0]['message']
    assert message == 'The agreement has been activated'



#Checking when the agreement's status is "Activated"
#if the transaction sent was on time

def test_timeNotBreached(deploy):
    '''check if the timeNotBreached function correctly increments positionPeriod. This is for checking inside sendPayments function'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    new_agreement_position = deploy.exactAgreement(agreements_number)[9]
    #the contract has been activated, now send the the money again
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})    
    assert deploy.exactAgreement(agreements_number)[9] == new_agreement_position + deploy.exactAgreement(agreements_number)[8]

def test_transactionCreated_updated(deploy):
    '''check if the time of the call to function sendPayment is stored'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[4] != '0'

def test_transactionCreated_updated_once_again(deploy):
    '''check if the time of the call to function sendPayment changes after another call to this function'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()  
    chain.sleep(3)
    first_call = deploy.exactAgreement(agreements_number)[4]
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[4] != first_call

@pytest.mark.parametrize("seconds_sleep",  [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_timeNotBreached_fail_if_statement(deploy, seconds_sleep):
    '''check if the timeNotBreached fails because transaction was sent after the agreement's deadline - it fails because of the check in the confirmAgreement function'''
    chain = Chain()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Terminated'

@pytest.mark.parametrize("seconds_sleep",  [less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_fail_if_statement_pair(deploy, seconds_sleep):
    '''check if the timeNotBreached works fine'''
    
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Activated'

    #if the amount <= msg.value

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value(deploy, value_sent):
    '''check if the msg.value is sent when amount <= msg.value in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
    balance_receiver = accounts[receiver].balance() 
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + value_sent

@pytest.mark.parametrize("value_sent",  [amount_sent, more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_larger_amount_send_value_totalEtherCommited_increased(deploy, value_sent):
    '''check if totalEtherCommited increases'''
    allEth = deploy.totalEtherCommited()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
    assert deploy.totalEtherCommited() == allEth + value_sent

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value_check_sender(deploy, value_sent):
    '''check if the balance of the sender is changed when amount <= msg.value in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
    balance_sender = accounts[sender].balance() 
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent}) 
    assert accounts[sender].balance() == balance_sender - value_sent

@pytest.mark.parametrize("value_sent",  [more_than_amount_sent[0], more_than_amount_sent[1], more_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value_check_sender_returned_excess(deploy, value_sent):
    '''check if the excess money is returned to the sender when he sends more than he should'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
    balance_sender = accounts[sender].balance() 
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
    deploy.withdrawAsThesender({'from': accounts[sender]}) 
    assert accounts[sender].balance() == balance_sender - value_sent + (value_sent - deploy.exactAgreement(agreements_number)[3])

def test_timeNotBreached_value_large_amount_emit_NotifyUser(deploy):
    '''check if the event NotifyUser is emitted when amount <= msg.value in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    #the contract has been activated, now send the money again
    function_initialize = deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert function_initialize.events[0][0]['message'] == "Transaction was sent to the receiver"

    #if the transaction sent was the last one

def test_timeNotBreached_breached_on_time_last_payment_deposit_sender(deploy):
    '''check if the deposit is returned to the sender when isLastPayment returns true'''
    chain = Chain()
    balance_sender = accounts[sender].balance() 
    deposit = deploy.exactAgreement(agreements_number)[5]
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    
    for _ in range(3):
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
        chain.sleep(60400)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.withdrawAsThesender({'from': accounts[sender]}) 
    assert accounts[sender].balance() == balance_sender  - 3*amount_sent - deposit

def test_timeNotBreached_breached_on_time_last_payment_totalDepositSent(deploy):
    '''check if the totalDepositSent is increased  when isLastPayment returns true'''
    chain = Chain()
    depositsTogether = deploy.totalDepositSent()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    agreementsdeposit = deploy.exactAgreement(agreements_number)[5]
    
    for _ in range(3):
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
        chain.sleep(60400)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.totalDepositSent() == depositsTogether + agreementsdeposit

def test_timeNotBreached_breached_on_time_last_payment_deposit_0(deploy):
    '''check if the deposit of the contract is 0 when isLastPayment returns true'''
    chain = Chain()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    
    for _ in range(3):
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
        chain.sleep(60400)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[5] == 0

def test_timeNotBreached_breached_on_time_last_payment_status_terminated(deploy):
    '''check if the status is changed to "Terminated" when isLastPayment returns true'''
    chain = Chain()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    
    for _ in range(3):
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
        chain.sleep(60400)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == "Terminated"

def test_timeNotBreached_breached_on_time_last_payment_emit(deploy):
    '''check if the event is emited when isLastPayment returns true'''
    chain = Chain()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    
    for _ in range(3):
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
        chain.sleep(60400)
    function_initialize = deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert function_initialize.events[0][0]['message'] == "You have fullfilled all your obligations"

    #if the amount > msg.value

@pytest.mark.parametrize("value_sent",  [amount_sent])
@pytest.mark.parametrize("value_decreased",  [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value_withdraw_sender(deploy, value_sent, value_decreased):
    '''check if the msg.value is not sent when amount >= msg.value in the timeNotBreached, the funds are returned to the sender'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
    balance_sender = accounts[sender].balance() 
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent - value_decreased})
    deploy.withdrawAsThesender({'from': accounts[sender]}) 
    assert accounts[sender].balance() == balance_sender 

@pytest.mark.parametrize("value_sent",  [amount_sent])
@pytest.mark.parametrize("value_decreased",  [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_large_amount_send_value_pair_event(deploy, value_sent, value_decreased):
    '''check if the msg.value is not sent when amount <= msg.value in the timeNotBreached, the contract terminates'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
    function_initialized = deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent - value_decreased}) 
    assert function_initialized.events[0][0]['message'] == "The amount sent is lower than in the agreement"

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_status(deploy, value_sent):
    '''check if the status is remains the same when amount > msg.value in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent})
    assert deploy.exactAgreement(agreements_number)[6] == "Activated"

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_send_deposit(deploy, value_sent):
    '''check if the deposit isn't sent to the receiver when amount > msg.value in the timeNotBreached'''
    try:
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent}) 
        deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
        pytest.fail("The try-except concept has failed in test_timeNotBreached_value_smaller_amount_send_deposit") 
    except Exception as e :
        assert e.message[50:] == "There aren't any funds to withdraw"

@pytest.mark.parametrize("value_sent",  [0, less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_timeNotBreached_value_smaller_amount_deposit_equals_zero(deploy, value_sent):
    '''check if the deposit isn't back on zero when amount > msg.value in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': value_sent}) 
    assert deploy.exactAgreement(agreements_number)[5] == amount_sent
    

#if the transaction wasn't sent on time

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_received_on_time_false_1st_part_if_statement(deploy, seconds_sleep):
    '''check if the timeNotBreached returns false, when transactionCreated > positionPeriod'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Terminated' 

@pytest.mark.parametrize("seconds_sleep",  [60*60*24*8, 60*60*24*9, 60*60*24*10])
def test_timeNotBreached_received_on_time_false_2nd_part_if_statement(deploy, seconds_sleep):
    '''check if the timeNotBreached returns false, when transaction received wasn't on time'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == 'Terminated'

@pytest.mark.parametrize("seconds_sleep",  [agreement_duration, 2629744, 26297440])
def test_timeNotBreached_breached_on_time_false_3rd_part_if_statement(deploy, seconds_sleep):
    '''check if the timeNotBreached returns false, when the deadline of the agreement has ended'''
    chain = Chain()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    
    for _ in range(3):
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
        chain.sleep(60400)
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.exactAgreement(agreements_number)[6] == "Terminated"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_status(deploy, seconds_sleep):
    '''check if the status is changed to Terminated when timeNotBreached is breached in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent}) 
    assert deploy.exactAgreement(agreements_number)[6] == "Terminated"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_status_pair(deploy, seconds_sleep):
    '''check if the status is not changed to Terminated when timeNotBreached is not breached in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent}) 
    assert deploy.exactAgreement(agreements_number)[6] == "Activated"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_send_deposit(deploy, seconds_sleep):
    '''check if the deposit is sent to the receiver when timeNotBreached is breached in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent}) 
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + amount_sent

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_send_deposit_pair(deploy, seconds_sleep):
    '''check if the deposit isn't sent to the receiver (but the value is) when timeNotBreached is not breached in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent}) 
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + 4*amount_sent

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_totalDepositSent(deploy, seconds_sleep):
    '''check if totalDepositSent increases by the deposit'''
    depositsTogether = deploy.totalDepositSent()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    agreementsdeposit = deploy.exactAgreement(agreements_number)[5]
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent}) 
    assert deploy.totalDepositSent() == depositsTogether + agreementsdeposit

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_deposit_equals_zero(deploy, seconds_sleep):
    '''check if the deposit is equal zero when timeNotBreached is breached in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent}) 
    assert deploy.exactAgreement(agreements_number)[5] == "0"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_deposit_equals_zero_pair(deploy, seconds_sleep):
    '''check if the deposit is not equal zero when timeNotBreached is not breached in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent}) 
    assert deploy.exactAgreement(agreements_number)[5] != "0"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_return_transaction(deploy, seconds_sleep):
    '''check if the transaction is sent back to the sender when timeNotBreached is breached in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})  
    balance_sender = accounts[sender].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent}) 
    deploy.withdrawAsThesender({'from': accounts[sender]})
    assert accounts[sender].balance() == balance_sender

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_return_transaction_pair(deploy, seconds_sleep):
    '''check if the transaction is not sent back to the sender (it's sent to the receiver) when timeNotBreached is not breached in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})  
    balance_sender = accounts[sender].balance() 
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent}) 
    assert accounts[sender].balance() == balance_sender - amount_sent

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_emit_Terminated(deploy, seconds_sleep):
    '''check if the event Terminated is emitted when timeNotBreached is breached in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    function_initialize = deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert function_initialize.events[0][0]['message'] == "The agreement was terminated due to late payment"

@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_timeNotBreached_breached_on_time_false_emit_Terminated_pair(deploy, seconds_sleep):
    '''check if the event Terminated is not emitted when timeNotBreached is not breached in the timeNotBreached'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    function_initialize = deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert function_initialize.events[0][0]['message'] != "The agreement was terminated due to late payment"

#Checking when the agreement's status is "Terminated"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_terminateContract_emit_Terminated_initial_status_terminated(deploy, seconds_sleep):
    '''check if the sendPayments emits correctly the message when the status is "Terminated"'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    with brownie.reverts("The agreement is already terminated"):
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})



''' TESTING WASCONTRACTBREACHED FUNCTION '''


@pytest.mark.aaa
@pytest.mark.parametrize("wrong_accounts",  [without_receiver[0], without_receiver[1], without_receiver[2]])
def test_wasContractBreached_require_receiver_equals_msg_sender(deploy, wrong_accounts):
    '''check if the wasContractBreached fails, because exactAgreement[_id].receiver == msg.sender is the require statement'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    with brownie.reverts("Your logged in address isn't the same as the agreement's receiver"):
        #wrong sender's address
        deploy.wasContractBreached(agreements_number, {'from': accounts[wrong_accounts]})
@pytest.mark.aaa
@pytest.mark.parametrize("right_accounts",  [receiver])
def test_wasContractBreached_require_receiver_equals_msg_sender_pair(deploy, right_accounts):
    '''check if the wasContractBreached doesn't fail'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[right_accounts]})
    assert function_initialize.events[0][0]['message'] == "The agreement wasn't breached"

#if timeNotBreached is True
@pytest.mark.aaa
def test_wasContractBreached_timeNotBreached_true_emit_NotifyUser(deploy):
    '''check if the wasContractBreached function when timeNotBreached is true, emits NotifyUser'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement wasn't breached"

#else
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_Terminated(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, changes status to Terminated'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[6] == "Terminated"
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_Terminated_pair(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't change status to Terminated'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[6] == "Activated"
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_send_deposit(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, sends a deposit to the receiver'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance()
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + amount_sent
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_send_deposit_pair(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't send a deposit to the receiver'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance()
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + amount_sent
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_deposit_equals_zero_1(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, changes deposit to 0'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[5] == '0'
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_status_deposit_equals_zero_1_pair(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't change deposit to 0'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[5] != '0'
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_true_totalDepositSent(deploy, seconds_sleep):
    '''check if the totalDepositSent() is incremented by the deposit'''
    totalDepositBefore = deploy.totalDepositSent()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    agreementsDeposit = deploy.exactAgreement(agreements_number)[5]
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.totalDepositSent() == totalDepositBefore + agreementsDeposit
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0] + 1000000, more_than_every_period[1] + 1000000, more_than_every_period[2] + 1000000])
def test_wasContractBreached_timeNotBreached_false_emit_Terminated_event(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is false, emits NotifyUser'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    #deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent})
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement has been terminated"
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [0, less_than_every_period[0], less_than_every_period[1], less_than_every_period[2]])
def test_wasContractBreached_timeNotBreached_false_emit_Terminated_pair(deploy, seconds_sleep):
    '''check if the wasContractBreached function when timeNotBreached is true, doesn't emit NotifyUser'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent})
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement wasn't breached"
@pytest.mark.aaa
def test_wasContractBreached_agreement_not_activated(deploy):
    '''check if the wasContractBreached function emits NotifyUser when timeNotBreached is false'''
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement hasn't been breached"

#if (exactAgreement[_id].agreementStartDate + (6*60*60*24) > block.timestamp)
@pytest.mark.aaa
def test_wasContractBreached_status_created_notify_user(deploy):
    '''check if the wasContractBreached function emits NotifyUser when exactAgreement[_id].agreementStartDate + (6*60*60*24) > block.timestamp'''
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement hasn't been breached"

#else
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])    
def test_wasContractBreached_status_created_status_terminated(deploy, seconds_sleep):
    '''check if the wasContractBreached function changes its status to "Terminated"'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[6] == "Terminated" 
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])    
def test_wasContractBreached_status_deposit(deploy, seconds_sleep):
    '''check if the wasContractBreached function returns deposit if the agreement was breached'''
    balance_receiver = accounts[receiver].balance()
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + amount_sent
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]]) 
def test_wasContractBreached_status_created_deposit_zero(deploy, seconds_sleep):
    '''check if the deposit of the breached agreement is equal 0'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.exactAgreement(agreements_number)[5] == '0'
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]]) 
def test_wasContractBreached_status_created_totalDepositsent(deploy, seconds_sleep):
    '''check if the totalDepositSent is increased by the deposit'''
    totalDepositBefore = deploy.totalDepositSent()
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.totalDepositSent() == totalDepositBefore + deploy.exactAgreement(agreements_number)[5]
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_status_created_false_emit_Terminated(deploy, seconds_sleep):
    '''check if the wasContractBreached function emits NotifyUser when exactAgreement[_id].agreementStartDate + (6*60*60*24) > block.timestamp fails'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement was terminated"

#status not Created or Activated
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_already_Terminated(deploy, seconds_sleep):
    '''check if the an event is emitted'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement is already terminated"
@pytest.mark.aaa
@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])    
def test_wasContractBreached_already_Terminated_2(deploy, seconds_sleep):
    '''check if the an event is emitted"'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    function_initialize = deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "The agreement is already terminated"



'''TEST WITHDRAWASTHERECEIVER'''



def test_withdrawAsTheReceiver_first_reguire_fails_case_1(deploy):
    '''require statement withdraw_receiver[exactAgreement[_id].receiver] > 0 fails, because we send only the deposit'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    with brownie.reverts("There aren't any funds to withdraw"):
        deploy.withdrawAsTheReceiver({'from': accounts[receiver]})

def test_withdrawAsTheReceiver_first_reguire_fails_case_2(deploy):
    '''require statement withdraw_receiver[exactAgreement[_id].receiver] > 0 fails, because we already withdraw the funds'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    with brownie.reverts("There aren't any funds to withdraw"):
        deploy.withdrawAsTheReceiver({'from': accounts[receiver]})

def test_withdrawAsTheReceiver_withdrawal_sent(deploy):
    '''Check if the withdrawal was sent to receiver'''
    receiver_balance = accounts[receiver].balance()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert accounts[receiver].balance() == receiver_balance + amount_sent

def test_withdrawAsTheReceiver_withdrawal_sent_event(deploy):
    '''check if the event is emitted'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    function_initialize = deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "Withdrawal has been transfered"

def test_withdrawAsTheReceiver_withdrawal_sent_2(deploy):
    '''Check if the withdrawal was sent to receiver'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    receiver_balance = accounts[receiver].balance()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert accounts[receiver].balance() == receiver_balance + amount_sent

def test_withdrawAsTheReceiver_withdrawal_sent_2_event(deploy):
    '''check if the event is emitted'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    function_initialize = deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "Withdrawal has been transfered"

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_withdrawAsTheReceiver_withdrawal_sent_3(deploy, time):
    '''Check if the withdrawal was sent to the receiver'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    receiver_balance = accounts[receiver].balance()
    agreementsDeposit = deploy.exactAgreement(agreements_number)[5]
    chain = Chain()
    chain.sleep(time)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert accounts[receiver].balance() == receiver_balance + agreementsDeposit

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_withdrawAsTheReceiver_withdrawal_sent_3_event(deploy, time):
    '''check if the event is emitted'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(time)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    function_initialize = deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "Withdrawal has been transfered"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_withdrawal_sent_4(deploy, seconds_sleep):
    '''Check if the withdrawal was sent to the receiver'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    balance_receiver = accounts[receiver].balance()
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + amount_sent

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])
def test_wasContractBreached_withdrawal_sent_4_event(deploy, seconds_sleep):
    '''check if the event is emitted'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    function_initialize = deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "Withdrawal has been transfered"

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])    
def test_wasContractBreached_withdrawal_sent_5(deploy, seconds_sleep):
    '''Check if the withdrawal was sent to the receiver'''
    balance_receiver = accounts[receiver].balance()
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert accounts[receiver].balance() == balance_receiver + amount_sent

@pytest.mark.parametrize("seconds_sleep",  [more_than_every_period[0], more_than_every_period[1], more_than_every_period[2]])    
def test_wasContractBreached_withdrawal_sent_5_event(deploy, seconds_sleep):
    '''check if the event is emitted'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    function_initialize = deploy.withdrawAsTheReceiver({'from': accounts[receiver]})
    assert function_initialize.events[0][0]['message'] == "Withdrawal has been transfered"



'''TEST WITHDRAWASTHESENDER'''



def test_withdrawAsThesender_first_reguire_fails(deploy):
    '''require statement withdraw_receiver[exactAgreement[_id].sender] > 0 fails, because we have no funds'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    with brownie.reverts("There aren't any funds to withdraw"):
        deploy.withdrawAsThesender({'from': accounts[sender]})

def test_withdrawAsThesender_first_reguire_fails_2(deploy):
    '''require statement withdraw_receiver[exactAgreement[_id].sender] > 0 fails, because we have no funds'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent})
    deploy.withdrawAsThesender({'from': accounts[sender]})
    with brownie.reverts("There aren't any funds to withdraw"):
        deploy.withdrawAsThesender({'from': accounts[sender]})

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_withdrawAsThesender_withdrawal_sent_1(deploy, time):
    '''Check if the withdrawal is sent'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 3*amount_sent})
    sender_balance = accounts[sender].balance()
    chain = Chain()
    chain.sleep(time)
    deploy.withdrawAsThesender({'from': accounts[sender]})
    assert accounts[sender].balance() == sender_balance + 2*amount_sent

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_withdrawAsThesender_withdrawal_sent_1_event(deploy, time):
    '''check if the event is emitted'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 3*amount_sent})
    chain = Chain()
    chain.sleep(time)
    function_initialize = deploy.withdrawAsThesender({'from': accounts[sender]})
    assert function_initialize.events[0][0]['message'] == "Withdrawal has been transfered"

@pytest.mark.parametrize("amount", [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_withdrawAsThesender_withdrawal_sent_2(deploy, amount):
    '''Check if the withdrawal is sent'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    sender_balance = accounts[sender].balance()
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount})
    deploy.withdrawAsThesender({'from': accounts[sender]})
    assert accounts[sender].balance() == sender_balance

@pytest.mark.parametrize("amount", [less_than_amount_sent[0], less_than_amount_sent[1], less_than_amount_sent[2]])
def test_withdrawAsThesender_withdrawal_sent_2_event(deploy, amount):
    '''check if the even is emitted'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount})
    function_initialize = deploy.withdrawAsThesender({'from': accounts[sender]})
    assert function_initialize.events[0][0]['message'] == "Withdrawal has been transfered"

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_withdrawAsThesender_withdrawal_sent_3(deploy, time):
    '''Check if the withdrawal is sent'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    sender_balance = accounts[sender].balance()
    chain = Chain()
    chain.sleep(time)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.withdrawAsThesender({'from': accounts[sender]})
    assert accounts[sender].balance() == sender_balance 

@pytest.mark.parametrize("time", [more_than_agreement_duration[0], more_than_agreement_duration[1], more_than_agreement_duration[2]])
def test_withdrawAsThesender_withdrawal_sent_3_event(deploy, time):
    '''Check if the event is emitted'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(time)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    function_initialize = deploy.withdrawAsThesender({'from': accounts[sender]})
    assert function_initialize.events[0][0]['message'] == "Withdrawal has been transfered"


'''TEST GETWITHDRAWALRECEIVER'''



@pytest.mark.parametrize("not_sender", [1, 2, 3, 4, 5, 6, 7, 8])
def test_getWithdrawalReceiver_not_receiver(deploy, not_sender):
    '''check if addresses that aren't agreements receiver's, have nothing to withdraw'''
    assert deploy.getWithdrawalReceiver({'from': accounts[receiver]}) == 0

def test_getWithdrawalReceiver_uninitialize_receiver(deploy):
    '''check if the receiver's address, is uninitialized'''
    assert deploy.getWithdrawalReceiver({'from': accounts[receiver]}) == 0

def test_getWithdrawalReceiver_uninitialize_receiver_2(deploy):
    '''check if the receiver's address, is uninitialized'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.getWithdrawalReceiver({'from': accounts[receiver]}) == 0

def test_getWithdrawalReceiver_exact_value(deploy):
    '''check if the receiver gets the exact value as agreed'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.getWithdrawalReceiver({'from': accounts[receiver]}) == amount_sent

def test_getWithdrawalReceiver_exact_value_2(deploy):
    '''check if the receiver gets the exact value as agreed'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 4*amount_sent})
    assert deploy.getWithdrawalReceiver({'from': accounts[receiver]}) == amount_sent

def test_getWithdrawalReceiver_multiple(deploy):
    '''check if the receiver gets the exact value as agreed'''
    for _ in range(5):
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.getWithdrawalReceiver({'from': accounts[receiver]}) == 4*amount_sent

def test_getWithdrawalReceiver_not_on_time(deploy):
    '''check if receiver gets the deposit when transaction wasn't sent on time'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(605800)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.getWithdrawalReceiver({'from': accounts[receiver]}) == amount_sent

def test_getWithdrawalReceiver_wasContractBreached(deploy):
    '''check if receiver gets the deposit when transaction wasn't sent on time'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(605800)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.getWithdrawalReceiver({'from': accounts[receiver]}) == amount_sent

def test_getWithdrawalReceiver_wasContractBreached_2(deploy):
    '''check if receiver gets the deposit when transaction wasn't sent on time and its status is created'''
    chain = Chain()
    chain.sleep(6*60*60*24)
    deploy.wasContractBreached(agreements_number, {'from': accounts[receiver]})
    assert deploy.getWithdrawalReceiver({'from': accounts[receiver]}) == amount_sent


'''TEST GETWITHDRAWALSENDER'''



@pytest.mark.parametrize("not_sender", [2, 3, 4, 5, 6, 7, 8, 9])
def test_getWithdrawalSender_not_sender(deploy, not_sender):
    '''check if addresses that aren't agreements sender's, have nothing to withdraw'''
    assert deploy.getWithdrawalSender({'from': accounts[not_sender]}) == 0

def test_getWithdrawalSender_uninitialize_sender(deploy):
    '''check if the sender's address, is uninitialized'''
    assert deploy.getWithdrawalSender({'from': accounts[sender]}) == 0

def test_getWithdrawalSender_uninitialize_sender_2(deploy):
    '''check if the sender's address, is uninitialized'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.getWithdrawalSender({'from': accounts[sender]}) == 0

@pytest.mark.parametrize("amount", [10**2])
def test_getWithdrawalSender_return_excess_eth(deploy, amount):
    '''check if the sc returns the excess eth sent by sender'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount})
    assert deploy.getWithdrawalSender({'from': accounts[sender]}) == amount -  amount_sent

@pytest.mark.parametrize("amount", [10**2])
def test_getWithdrawalSender_return_excess_eth_2(deploy, amount):
    '''check if the sc returns the excess eth sent by sender'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount})
    assert deploy.getWithdrawalSender({'from': accounts[sender]}) == amount -  amount_sent

def test_getWithdrawal_sender_last_value_sent(deploy):
    '''check if the sender receives back the deposit, when the last payment is sent'''
    for _ in range(5):
        deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
        chain = Chain()
        chain.sleep(604750)
    assert deploy.getWithdrawalSender({'from': accounts[sender]}) == amount_sent

@pytest.mark.parametrize("amount", [9**1])
def test_getWithdrawalSender_to_small_value_sent(deploy, amount):
    '''check if the sc returns eth, when the value sent was to small'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': 10**1})
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount})
    assert deploy.getWithdrawalSender({'from': accounts[sender]}) == amount

def test_getWithdrawalSender_payment_not_on_time(deploy):
    '''check if the the sender gets back its amount sent, when payment is not on time'''
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    chain = Chain()
    chain.sleep(605000)
    deploy.sendPayment(agreements_number, {'from': accounts[sender], 'value': amount_sent})
    assert deploy.getWithdrawalSender({'from': accounts[sender]}) == amount_sent












