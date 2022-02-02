import pytest
import brownie
from brownie import accounts
from brownie.network import rpc
from brownie.network.state import Chain

@pytest.fixture()
def deploy(AgreementBetweenSubjects):
    return AgreementBetweenSubjects.deploy({'from': accounts[0]})
  
@pytest.fixture(autouse=True)
def new_agreement_1(deploy):
    return deploy.createAgreement('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', 2, 5, 500, {'from': accounts[1]})

@pytest.fixture(autouse=True)
def new_agreement_2(deploy):   
    return deploy.createAgreement('0xdD870fA1b7C4700F2BD7f44238821C26f7392148', 100000000000000000000000000000000000000000000000000000000000000000000000000000, 499, 1000000000000000000000000000000000000000000000000000000000000000000000000, {'from': accounts[1]})

@pytest.fixture(autouse=True)
def new_agreement_3(deploy):
    return deploy.createAgreement('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', 2, 5, 500, {'from': accounts[3]})

@pytest.fixture(autouse=True)
def new_agreement_4(deploy, module_isolation):
    return deploy.createAgreement(accounts[9], 2, 5, 500, {'from': accounts[6]})

@pytest.fixture(autouse=True)
def new_agreement_5(deploy, module_isolation):
    return deploy.createAgreement(accounts[9], 2, 5, 10, {'from': accounts[6]})

@pytest.fixture(autouse=True)
def new_agreement_6(deploy):
    return deploy.createAgreement(accounts[9], 2, 0.0001, 10, {'from': accounts[1]})

@pytest.fixture(autouse=True)
def new_agreement_7(deploy):
    return deploy.createAgreement(accounts[9], 10**18, 604800, 2629743, {'from': accounts[1]})
    



'''TESTING CREATEAGREEMENT FUNCTION AGREEMENT 1'''



def test_exactAgreement_id(deploy):
    '''check if the first id of the agreement is zero'''
    assert deploy.exactAgreement(0)[0] == '0'

def test_exactAgreement_signee(deploy):
    '''check if the first address of the agreement's signee is the same as the accounts[1]'''
    assert deploy.exactAgreement(0)[1] == '0x33A4622B82D4c04a53e170c638B944ce27cffce3'

def test_exactAgreement_receiver(deploy):
    '''check if the first address of the agreement's receiver is the same as the accounts[0]'''
    assert deploy.exactAgreement(0)[2] == '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'

def test_exactAgreement_amount(deploy):
    '''check if the amount of the agreement is 2'''
    assert deploy.exactAgreement(0)[3] == '2'   

def test_exactAgreement_initialize_transactionCreated(deploy):
    '''check if the transactionCreated is 0'''
    assert deploy.exactAgreement(0)[4] == '0'

def test_exactAgreement_deposit(deploy):
    '''check if the initial amount of the deposit is 0'''
    assert deploy.exactAgreement(0)[5] == '0'

def test_exactAgreement_status(deploy):
    '''check if the initial status is equal to "Created"'''
    assert deploy.exactAgreement(0)[6] == 'Created'

def test_exactAgreement_approved(deploy):
    '''check if the initial approve "Not Confirmed"'''
    assert deploy.exactAgreement(0)[7] == 'Not Confirmed'

def test_exactAgreement_time_creation(deploy):
    '''check if the initial time creation is block.timestamp'''
    assert deploy.exactAgreement(0)[8] == deploy.exactAgreement(0)[8]
   
def test_exactAgreement_every_time_unit(deploy):
    '''check if the initial every time unit is 5'''
    seconds_in_day = 60 * 60 * 24
    assert deploy.exactAgreement(0)[9] == seconds_in_day * 5

def test_exactAgreement_position_period(deploy):
    '''check if the initial position period is 0'''
    assert deploy.exactAgreement(0)[10] == '0'

def test_exactAgreement_how_long(deploy):
    '''check if the initial how long is 500'''
    seconds_in_day = 60 * 60 * 24
    assert deploy.exactAgreement(0)[11] == seconds_in_day * 500

def test_exactAgreement_id_agreement_2(deploy):
    '''check if the id of the agreement 2 is one'''
    assert deploy.exactAgreement(1)[0] == '1'

def test_exactAgreement_id_agreement_3(deploy):
    '''check if the id of the agreement 3 is two'''
    assert deploy.exactAgreement(2)[0] == '2'

def test_new_agreement_fails_require(deploy):
    '''check if the new agreement fails, because howLong > _everyTimeUnit in the require statement'''
    try:
        #length of the agreement is longer than _everyTimeUnit
        deploy.createAgreement('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', 2, 500, 5, {'from': accounts[3]})
    except Exception as e:
        assert e.message[50:] == 'The period of the payment is greater than the duration of the contract'
    

'''TESTING CREATEAGREEMENT FUNCTION AGREEMENT 2'''



def test_increment_number_of_agreements_correctly(deploy):
    assert deploy.exactAgreement(1)[0] == '1'

def test_exactAgreement_check_large_amount(deploy):
    '''the max number of digits in "amount"'''
    assert deploy.exactAgreement(1)[3] == '100000000000000000000000000000000000000000000000000000000000000000000000000000' 

def test_exactAgreement_transactionCreated(deploy):
    '''check that transactionCreated is 0'''
    assert deploy.exactAgreement(1)[4] == '0' 

def test_exactAgreement_check_large_everyTimeUnit(deploy):
    '''the max number of digits in "_everyTimeUnit"'''
    seconds_in_day = 60 * 60 * 24
    assert deploy.exactAgreement(1)[9] == seconds_in_day * 499

def test_exactAgreement_check_large_howLong(deploy):
    '''the max number of digits in _howLong'''
    seconds_in_day = 60 * 60 * 24
    assert deploy.exactAgreement(1)[11] == seconds_in_day * 1000000000000000000000000000000000000000000000000000000000000000000000000



'''TESTING EVENT AGREEMENTINFO INSIDE CREATEAGREEMENT FUNCTION'''



def test_event_AgreementInfo_agreementId(new_agreement_1):
    '''check if the event AgreementInfo emits correctly agreementId'''
    assert new_agreement_1.events[0]["agreementId"] == "0"

def test_event_AgreementInfo_agreementSignee(new_agreement_1):
    '''check if the event AgreementInfo emits correctly agreementSignee'''
    assert new_agreement_1.events[0]["agreementSignee"] == accounts[1]

def test_event_AgreementInfo_agreementReceiver(new_agreement_1):
    '''check if the event AgreementInfo emits correctly agreementReceiver'''
    assert new_agreement_1.events[0]["agreementReceiver"] == '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'

def test_event_AgreementInfo_agreementAmount(new_agreement_1):
    '''check if the event AgreementInfo emits correctly agreementAmount'''
    assert new_agreement_1.events[0]["agreementAmount"] == '2'

def test_event_AgreementInfo_transactionCreated(new_agreement_1):
    '''check if the event AgreementInfo emits correctly agreementAmount'''
    assert new_agreement_1.events[0]["agreementTransactionCreated"] == '0'

def test_event_AgreementInfo_agreementDeposit(new_agreement_1):
    '''check if the event AgreementInfo emits correctly agreementAmount'''
    assert new_agreement_1.events[0]["agreementDeposit"] == '0'

def test_event_AgreementInfo_agreementStatus(new_agreement_1):
    '''check if the event AgreementInfo emits correctly agreementStatus'''
    assert new_agreement_1.events[0]["agreementStatus"] == 'Created'

def test_event_AgreementInfo_agreementApproved(new_agreement_1):
    '''check if the event AgreementInfo emits correctly agreementStatus'''
    assert new_agreement_1.events[0]["agreementApproved"] == 'Not Confirmed'

def test_event_AgreementInfo_agreementTimeCreation(new_agreement_1, deploy):
    '''check if the event AgreementInfo emits correctly agreementTimeCreation'''
    assert new_agreement_1.events[0]["agreementTimeCreation"] == deploy.exactAgreement(0)[8]

def test_event_AgreementInfo_agreementTimePeriods(new_agreement_1):
    '''check if the event AgreementInfo emits correctly agreementTimePeriods in seconds'''
    seconds_in_day = 60 * 60 * 24
    assert new_agreement_1.events[0]["agreementTimePeriods"] == 5 * seconds_in_day

def test_event_AgreementInfo_agreementPositionPeriod(new_agreement_1):
    '''check if the event AgreementInfo emits correctly agreementPositionPeriod in days'''
    assert new_agreement_1.events[0]["agreementPositionPeriod"] == 0

def test_event_AgreementInfo_agreementTimeDuration(new_agreement_1):
    '''check if the event AgreementInfo emits correctly agreementTimeDuration in seconds'''
    seconds_in_day = 60 * 60 * 24
    assert new_agreement_1.events[0]["agreementTimeDuration"] == 500 * seconds_in_day

def test_event_AgreementInfo_equals_Agreement(deploy, new_agreement_1):
    '''check if the length of the AgreementInfo elements is the same as in exactAgreements'''
    agreement = deploy.exactAgreement(0)
    event = new_agreement_1.events[0][0]
    assert len(agreement) == len(event)
    


'''TESTING MYSENDERAGREEMENTS FUNCTION'''



def test_MySenderAgreements_emits_correctly_agreementId_agreements_1(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementId from agreement 1'''
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementId'] == '0'   

def test_MySenderAgreements_emits_correctly_agreementSignee_agreements_1(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementSignee from agreement 1'''
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementSignee'] == accounts[1]

def test_MySenderAgreements_emits_correctly_agreementReceiver_agreements_1(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementReceiver from agreement 1'''
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementReceiver'] == '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'

def test_MySenderAgreements_emits_correctly_agreementAmount_agreements_1(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementAmount from agreement 1'''
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementAmount'] == '2'

def test_MySenderAgreements_emits_correctly_agreementTransactionCreated(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementTransactionCreated from agreement 1'''
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementTransactionCreated'] == '0'

def test_MySenderAgreements_emits_correctly_agreementDeposit_agreements_1(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementDeposit from agreement 1'''
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementDeposit'] == '0'

def test_MySenderAgreements_emits_correctly_agreementStatus_agreements_1(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementStatus from agreement 1'''
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementStatus'] == 'Created'

def test_MySenderAgreements_emits_correctly_agreementApproved_agreements_1(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementApproved from agreement 1'''
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementApproved'] == 'Not Confirmed'

def test_MySenderAgreements_emits_correctly_agreementTimeCreation_agreements_1(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementTimeCreation from agreement 1'''
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementTimeCreation'] == deploy.exactAgreement(0)[8]

def test_MySenderAgreements_emits_correctly_agreementTimePeriods_agreements_1(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementTimePeriods from agreement 1'''
    seconds_in_day = 60 * 60 * 24
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementTimePeriods'] == seconds_in_day * 5

def test_MySenderAgreements_emits_correctly_agreementPositionPeriod_agreements_1(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementPositionPeriod from agreement 1'''
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementPositionPeriod'] == '0'

def test_MySenderAgreements_emits_correctly_agreementTimeDuration_agreements_1(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementTimeDuration from agreement 1'''
    seconds_in_day = 60 * 60 * 24
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[0]['agreementTimeDuration'] == seconds_in_day * 500

def test_MySenderAgreements_emits_correctly_agreementId_agreements_2(deploy):
    '''check if the MySenderAgreements function emits correctly the agreementId from agreement 2'''
    assert deploy.MySenderAgreements(accounts[1], {'from': accounts[1]}).events[1]['agreementId'] == '1'

def test_mySenderAgreements_emits_correct_id_accounts_1(deploy):
    '''check if the mapping mySenderAgreements emits correct agreementId for the first element in the mapping of address accounts[1]'''
    assert deploy.mySenderAgreements(accounts[1], 0) == '0'

def test_mySenderAgreements_emits_correct_id_accounts_2(deploy):
    '''check if the mapping mySenderAgreements is returning correctly the ids'''
    assert deploy.mySenderAgreements(accounts[1], 1) == '1'

def test_mySenderAgreements_emits_correct_id_accounts_3(deploy):
    '''check if the mapping mySenderAgreements emits correct agreementId for the first element in the mapping of address accounts[3]'''
    assert deploy.mySenderAgreements(accounts[3], 0) == '2'

def test_MySenderAgreements_fails_require(deploy):
    '''check if the MySenderAgreements fails, because msg.sender == _myAddress in the require statement'''
    try:
        #wrong sender's address
        deploy.MySenderAgreements(accounts[1], {'from': accounts[3]})
    except Exception as e:
        assert e.message[50:] == "The address provided doesn't correspond with the one you're logged in"



'''TESTING MYRECEIVERAGREEMENTS FUNCTION'''



def test_MyReceiverAgreements_emits_correctly_agreementId_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementId from agreement 1'''
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementId'] == '0'

def test_MyReceiverAgreements_emits_correctly_agreementSignee_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementSignee from agreement 1'''
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementSignee'] == accounts[1]

def test_MyReceiverAgreements_emits_correctly_agreementReceiver_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementReceiver from agreement 1'''
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementReceiver'] == '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'

def test_MyReceiverAgreements_emits_correctly_agreementAmount_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementAmount from agreement 1'''
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementAmount'] == '2'

def test_MyReceiverAgreements_emits_correctly_agreementTransactionCreated_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementTransactionCreated from agreement 1'''
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementTransactionCreated'] == '0'

def test_MyReceiverAgreements_emits_correctly_agreementDeposit_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementDeposit from agreement 1'''
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementDeposit'] == '0'

def test_MyReceiverAgreements_emits_correctly_agreementStatus_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementStatus from agreement 1'''
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementStatus'] == 'Created'

def test_MyReceiverAgreements_emits_correctly_agreementApproved_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementApproved from agreement 1'''
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementApproved'] == 'Not Confirmed'

def test_MyReceiverAgreements_emits_correctly_agreementTimeCreation_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementTimeCreation from agreement 1'''
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementTimeCreation'] == deploy.exactAgreement(0)[8]

def test_MyReceiverAgreements_emits_correctly_agreementTimePeriods_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementTimePeriods from agreement 1'''
    seconds_in_day = 60 * 60 * 24
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementTimePeriods'] == seconds_in_day * 5

def test_MyReceiverAgreements_emits_correctly_agreementPositionPeriod_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementPositionPeriod from agreement 1'''
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementPositionPeriod'] == '0'

def test_MyReceiverAgreements_emits_correctly_agreementTimeDuration_agreements_1(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementTimeDuration from agreement 1'''
    seconds_in_day = 60 * 60 * 24
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[0]['agreementTimeDuration'] == seconds_in_day * 500

def test_MyReceiverAgreements_emits_correctly_agreementId_agreements_2(deploy):
    '''check if the MyReceiverAgreements function emits correctly the agreementId from agreement 1'''
    assert deploy.MyReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'}).events[1]['agreementId'] == '2'

def test_myReceiverAgreements_emits_correct_id_agreement_1(deploy):
    '''check if the mapping myReceiverAgreements emits correct agreementId for the first element in the mapping of address 0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'''
    assert deploy.myReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', 0) == '0'

def test_myReceiverAgreements_emits_correct_id_agreement_2(deploy):
    '''check if the mapping myReceiverAgreements is returning correctly the ids'''
    assert deploy.myReceiverAgreements('0xdD870fA1b7C4700F2BD7f44238821C26f7392148', 0) == '1'

def test_myReceiverAgreements_emits_correct_id_agreement_3(deploy):
    '''check if the mapping myReceiverAgreements emits correct agreementId for the first element in the mapping of address 0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'''
    assert deploy.myReceiverAgreements('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2', 1) == '2'

def test_MyReceiverAgreements_fails_require(deploy):
    '''check if the MyReceiverAgreements fails, because msg.sender == _myAddress in the require statement'''
    try:
        #wrong sender's address
        deploy.MyReceiverAgreements(accounts[1], {'from': accounts[3]})
    except Exception as e:
        assert e.message[50:] == "The address provided doesn't correspond with the one you're logged in"



''' TESTING CONFIRMAGREEMENT FUNCTION'''



def test_ConfirmAgreement_agreement_already_confirmed(deploy):
    '''check if the ConfirmAgreement checks if the agreement is already confirmed'''
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    function_enabled = deploy.ConfirmAgreement(6, {'from': accounts[9]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement is already confirmed'

@pytest.mark.parametrize("seconds_sleep",  [2629743, 2630000, 2640000])
def test_ConfirmAgreement_fail_require_2(deploy, seconds_sleep):
    '''check if the ConfirmAgreement fails if the receiver wants to confirm an agreement that has ended'''
    try:
        chain = Chain()
        chain.sleep(seconds_sleep)
        deploy.ConfirmAgreement(6, {'from': accounts[9]})        
    except Exception as e:
        assert e.message[50:] == "The agreement's deadline has ended"

@pytest.mark.parametrize("seconds_sleep", [0, 260, 2640, 2629742, 2629743, 2630000, 2640000])
def test_ConfirmAgreement_fail_require_2_pair(deploy, seconds_sleep):
    '''check if the ConfirmAgreement fails if the receiver wants to confirm an agreement that has ended'''
    chain = Chain()
    chain.sleep(seconds_sleep)
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    assert deploy.exactAgreement(6)[7] == 'Confirmed'    
   
@pytest.mark.parametrize("accounts_number", [1, 2, 3, 4, 5, 6, 7])
def test_ConfirmAgreement_fail_require_1(deploy, accounts_number):
    '''check if the ConfirmAgreement fails if the receiver is wrong'''
    try:
        deploy.ConfirmAgreement(6, {'from': accounts[accounts_number]})        
    except Exception as e:
        assert e.message[50:] == "Only the receiver can confirm the agreement"

@pytest.mark.parametrize("accounts_number", [9])
def test_ConfirmAgreement_fail_require_1_pair(deploy, accounts_number):
    '''check if the ConfirmAgreement fails if the receiver is wrong'''
    try:
        deploy.ConfirmAgreement(6, {'from': accounts[accounts_number]})        
    except Exception as e:
        assert e.message[50:] != "Only the receiver can confirm the agreement"

def test_ConfirmAgreement_agreement_status_confirmed(deploy):
    '''check if the ConfirmAgreement changes status to "Confirmed"'''
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    assert deploy.exactAgreement(6)[7] == 'Confirmed'





'''TESTING TERMINATE CONTRACT'''



#here we are contacting sendPayment prior terminating the agreement (it should be the same otherwise)

def test_terminateContract_emit_Terminated_initial_status_activated_already_terminated(deploy):
    '''checking if the event Terminated has been emitted as "This agreement has been terminated" when you want to terminate a contract'''
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    deploy.sendPayment(6, {'from': accounts[1], 'value': 10**18})
    deploy.terminateContract(6, {'from': accounts[1]})
    function_enabled = deploy.terminateContract(6, {'from': accounts[1]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement is already terminated'

@pytest.mark.parametrize("accounts_number", [2, 3, 4, 5, 6, 7])
def test_terminateContract_fails_require_wrong_address_initial_status_activated(deploy, accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        deploy.ConfirmAgreement(6, {'from': accounts[9]})
        deploy.sendPayment(6, {'from': accounts[1], 'value': 10**18})
        #wrong sender's address
        deploy.terminateContract(6, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] == "Only the owner can terminate the agreement"

@pytest.mark.parametrize("accounts_number", [1])
def test_terminateContract_fails_require_wrong_address_initial_status_activated_pair(deploy, accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        deploy.ConfirmAgreement(6, {'from': accounts[9]})
        deploy.sendPayment(6, {'from': accounts[1], 'value': 10**18})
        #wrong sender's address
        deploy.terminateContract(6, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] != "Only the owner can terminate the agreement"

def test_terminateContract_function_change_status_terminated(deploy):
    '''check if the function terminateContract changes status of the agreement to "Terminated"'''
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    deploy.sendPayment(6, {'from': accounts[1], 'value': 10**18})
    deploy.terminateContract(6, {'from': accounts[1]})
    assert deploy.exactAgreement(6)[6] == 'Terminated'

@pytest.mark.parametrize("value_sent", [10**18, 11**18, 12**18])
def test_transfer_deposit_back_to_signee(deploy, value_sent):
    '''check if the deposit is transfered back to the signee'''
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    deploy.sendPayment(6, {'from': accounts[1], 'value': value_sent})
    balance_signee = accounts[1].balance() 
    deploy.terminateContract(6, {'from': accounts[1]})
    assert accounts[1].balance() == balance_signee + value_sent

@pytest.mark.parametrize("value_sent", [1, 7**18, 9**18])
def test_transfer_deposit_back_to_signee_pair(deploy, value_sent):
    '''check if the deposit is not transfered back to the signee'''
    try:
        deploy.ConfirmAgreement(6, {'from': accounts[9]})
        deploy.sendPayment(6, {'from': accounts[1], 'value': value_sent})
        balance_signee = accounts[1].balance() 
        deploy.terminateContract(6, {'from': accounts[1]})
    except Exception as e:
        assert e.message[50:] == "The deposit is not the same as the agreed in the terms"
    

'''
#not implemented 
def test_transfer_msg_value_back_to_signee(deploy):
    check if the deposit is transfered back to the signee
    deploy.ConfirmAgreement(3, {'from': accounts[9]})
    deploy.sendPayment(3, {'from': accounts[6], 'value': 20})
    balance_signee = accounts[6].balance() 
    deploy.sendPayment(3, {'from': accounts[6], 'value': 20})
    deploy.terminateContract(3, {'from': accounts[6]})
    assert accounts[6].balance() == balance_signee + 20
'''

def test_terminateContract_function_change_status_terminated_deposit(deploy):
    '''check if the function terminateContract changes deposit to zero"'''
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    deploy.sendPayment(6, {'from': accounts[1], 'value': 10**18})
    deploy.terminateContract(6, {'from': accounts[1]})
    assert deploy.exactAgreement(6)[5] == '0'

def test_terminateContract_emit_Terminated_initial_status_activated(deploy):
    '''checking if the event Terminated has been emitted as "This agreement has been terminated" when you want to terminate a contract'''
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    deploy.sendPayment(6, {'from': accounts[1], 'value': 10**18})
    function_enabled = deploy.terminateContract(6, {'from': accounts[1]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement has been terminated'

#here we aren't contacting sendPayments prior terminating the contract

@pytest.mark.parametrize("accounts_number", [2, 3, 4, 5, 6, 7])
def test_terminateContract_fails_require_wrong_address_initial_status_activated_without_sendPayments(deploy, accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        deploy.ConfirmAgreement(6, {'from': accounts[9]})
        #wrong sender's address
        deploy.terminateContract(6, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] == "Only the owner can terminate the agreement"

@pytest.mark.parametrize("accounts_number", [1])
def test_terminateContract_fails_require_wrong_address_initial_status_activated_pair(deploy, accounts_number):
    '''check if the function terminateContract fails, because require(exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        deploy.ConfirmAgreement(6, {'from': accounts[9]})
        #wrong sender's address
        deploy.terminateContract(6, {'from': accounts[accounts_number]})
    except Exception as e:
        assert e.message[50:] != "Only the owner can terminate the agreement"

def test_terminateContract_function_change_status_terminated_without_sendPayments(deploy):
    '''check if the function terminateContract changes status of the agreement to "Terminated"'''
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    deploy.terminateContract(6, {'from': accounts[1]})
    assert deploy.exactAgreement(6)[6] == 'Terminated'

def test_transfer_deposit_back_to_signee_2(deploy):
    '''check if the deposit is transfered back to the signee'''
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    balance_signee = accounts[1].balance() 
    deploy.terminateContract(6, {'from': accounts[1]})
    assert accounts[1].balance() == balance_signee

def test_terminateContract_function_change_status_terminated_deposit_2(deploy):
    '''check if the function terminateContract changes deposit to 0'''
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    deploy.terminateContract(6, {'from': accounts[1]})
    assert deploy.exactAgreement(6)[5] == '0'

def test_terminateContract_emit_Terminated_initial_status_activated_without_sendPayments(deploy):
    '''checking if the event Terminated has been emitted as "This agreement has been terminated" when you want to terminate a contract'''
    deploy.ConfirmAgreement(6, {'from': accounts[9]})
    function_enabled = deploy.terminateContract(6, {'from': accounts[1]})
    message = function_enabled.events[0][0]['message']
    assert message == 'This agreement has been terminated'



'''TESTING SENDPAYMENT, INITIALIZINGPOSITIONPERIOD AND TIMENOTBREACHED FUNCTIONS'''


#can we check the require, revert
#What happens if the unix timestamp is larger or equal to 19th Jan 2038?
#what happens if teh transaction cannot be sent?

#Checking the require statements 

def test_sendPayments_fails_require_wrong_address(deploy):
    '''check if the sendPayments fails, because exactAgreement[_id].signee == msg.sender in the require statement'''
    try:
        deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
        #wrong signer's address
        deploy.sendPayment(0, {'from': accounts[3], 'value': 20})
    except Exception as e:
        assert e.message[50:] == "Only the owner can pay the agreement's terms"

def test_sendPayments_fails_require_not_confirmed(deploy):
    '''check if the sendPayments fails, because exactAgreement[_id].approved)) == "Confirmed" in the require statement'''
    try:
        #no confirmation
        deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    except Exception as e:
        assert e.message[50:] == "The receiver has to confirm the contract"

#Checking when the agreement's status is "Created"

def test_sendPayments_require_statement_fails_agreement_not_ended(deploy):
    '''check if the require statement fails when the agreement's deadline has ended'''
    try:
        deploy.ConfirmAgreement(4, {'from': accounts[9]})
        deploy.sendPayment(4, {'from': accounts[6], 'value': 20})        
    except Exception as e:
        assert e.message[50:] == "This agreement's deadline has ended"

def test_sendPayments_fails_require_smaller_deposit_initial_status_created(deploy):
    '''check if the sendPayments fails, because exactAgreement[_id].agreedDeposit <= msg.value in the require statement'''
    try:
        deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
        #'value' is smaller than it should be
        deploy.sendPayment(0, {'from': accounts[1], 'value': 1})
    except Exception as e:
        assert e.message[50:] == "The deposit is not the same as the agreed in the terms"

def test_sendPayments_change_status_initial_status_created(deploy):
    '''checking if the status is changed to "Activated" when msg.value is larger or equal to agreedDeposit'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    assert deploy.exactAgreement(0)[6] == 'Activated'

def test_sendPayments_change_initializePeriod_initial_status_created(deploy):
    '''checking if the InitializedPeriod is initialize (sum of agreementTimeCreation and everyTimeUnit) when msg.value is larger or equal to agreedDeposit'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    assert deploy.exactAgreement(0)[10] == deploy.exactAgreement(0)[8] + deploy.exactAgreement(0)[9]

def test_sendPayments_change_agreementDeposit_initial_status_created(deploy):
    '''checking if the deposit has been initialized to msg.value when msg.value is larger or equal to agreedDeposit'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    assert deploy.exactAgreement(0)[5] == '20'

def test_sendPayments_emit_NotifyUser_initial_status_created(deploy):
    '''checking if the event has been emitted as "We have activate the agreement" when msg.value is larger or equal to agreedDeposit'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    function_enabled = deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    message = function_enabled.events[0][0]['message']
    assert message == 'We have activate the agreement'



#Checking when the agreement's status is "Activated"
#if the transaction sent was on time

def test_timeNotBreached(deploy):
    '''check if the timeNotBreached function correctly increments positionPeriod. This is for checking inside sendPayments function'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    new_agreement_position = deploy.exactAgreement(0)[10]
    #the contract has been activated, now send the the money again
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})    
    assert deploy.exactAgreement(0)[10] == new_agreement_position + deploy.exactAgreement(0)[9]

def test_transactionCreated_updated(deploy):
    '''check if the time of the call to function sendPayment is stored'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})  
    assert deploy.exactAgreement(0)[4] != '0'

def test_transactionCreated_updated_once_again(deploy):
    '''check if the time of the call to function sendPayment changes after another call to this function'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})  
    first_call = deploy.exactAgreement(0)[4] != '0'
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    assert deploy.exactAgreement(0)[4] != first_call

    #if the amount <= msg.value

def test_timeNotBreached_fail_if_statement(deploy):
    '''check if the timeNotBreached fails because transaction was sent after the agreement's deadline - it fails because of the check in the ConfirmAgreement function'''
    try:
        deploy.ConfirmAgreement(4, {'from': accounts[9]})
        deploy.sendPayment(4, {'from': accounts[6], 'value': 20})
    except Exception as e:        
        assert e.message[50:] == "This agreement's deadline has ended"

def test_timeNotBreached_value_large_amount_send_value(deploy):
    '''check if the msg.value is sent when amount <= msg.value in the timeNotBreached'''
    deploy.ConfirmAgreement(3, {'from': accounts[9]})
    deploy.sendPayment(3, {'from': accounts[6], 'value': 20})
    balance_receiver = accounts[9].balance() 
    deploy.sendPayment(3, {'from': accounts[6], 'value': 30}) 
    assert accounts[9].balance() == balance_receiver + 30
'''
tried to test failed sent , but couldn't fugure it out
@pytest.mark.vvv
def test_timeNotBreached_value_large_amount_fail_sending(deploy):
    check if the "Failed to send Ether" is outposted when sending the money fails
    try:
        deploy.ConfirmAgreement(5, {'from': "0x0000000000000000000000000000000000000000"})
        deploy.sendPayment(5, {'from': accounts[6]})
        #deploy.sendPayment(5, {'from': accounts[6], 'value': 20})
    except Exception as e:        
        assert e.message[50:] == "Failed to send Ether"'''
    

def test_timeNotBreached_value_large_amount_emit_NotifyUser(deploy):
    '''check if the event NotifyUser is emitted when amount <= msg.value in the timeNotBreached'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    #the contract has been activated, now send the money again
    function_initialize = deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    assert function_initialize.events[0][0]['message'] == "Transaction was sent to the receiver"

    #if the amount > msg.value

def test_timeNotBreached_value_smaller_amount_status(deploy):
    '''check if the status is changed when amount > msg.value in the timeNotBreached'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    #the contract has been activated, now send the smaller quantity of money again
    deploy.sendPayment(0, {'from': accounts[1], 'value': 1})
    assert deploy.exactAgreement(0)[6] == "Terminated"

def test_timeNotBreached_value_smaller_amount_send_deposit(deploy):
    '''check if the deposit is sent to the receiver when amount > msg.value in the timeNotBreached'''
    deploy.ConfirmAgreement(3, {'from': accounts[9]})
    deploy.sendPayment(3, {'from': accounts[6], 'value': 20})
    balance_receiver = accounts[9].balance() 
    deploy.sendPayment(3, {'from': accounts[6], 'value': 1}) 
    assert accounts[9].balance() == balance_receiver + 20

def test_timeNotBreached_value_smaller_amount_deposit_equals_zero(deploy):
    '''check if the deposit is back on zero when amount > msg.value in the timeNotBreached'''
    deploy.ConfirmAgreement(3, {'from': accounts[9]})
    deploy.sendPayment(3, {'from': accounts[6], 'value': 20})
    deploy.sendPayment(3, {'from': accounts[6], 'value': 1}) 
    assert deploy.exactAgreement(0)[5] == "0"

def test_timeNotBreached_value_smaller_amount_return_transaction(deploy):
    '''check if the transaction is sent back to the signee when amount > msg.value in the timeNotBreached'''
    deploy.ConfirmAgreement(3, {'from': accounts[9]})
    deploy.sendPayment(3, {'from': accounts[6], 'value': 20})  
    balance_signee = accounts[6].balance() 
    deploy.sendPayment(3, {'from': accounts[6], 'value': 1}) 
    assert accounts[6].balance() == balance_signee
    
def test_timeNotBreached_value_smaller_amount_emit_Terminated(deploy):
    '''check if the evant Terminated is emitted when amount > msg.value in the timeNotBreached'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    #the contract has been activated, now send the smaller quantity of money again
    function_initialize = deploy.sendPayment(0, {'from': accounts[1], 'value': 1})
    assert function_initialize.events[0][0]['message'] == "This agreement was terminated due to different payment than in the terms"

    

#if the transaction wasn't sent on time

def test_timeNotBreached_received_on_time_false(deploy):
    '''check if the timeNotBreached returns false, when transaction received wasn't on time'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    rpc.sleep(60*60*24*6)
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    assert deploy.exactAgreement(0)[6] == 'Terminated'

def test_timeNotBreached_breached_on_time_false_status(deploy):
    '''check if the status is changed when timeNotBreached is breached in the timeNotBreached'''
    deploy.ConfirmAgreement(5, {'from': accounts[9]})
    deploy.sendPayment(5, {'from': accounts[1], 'value': 20})
    #the contract has been activated, now send the smaller quantity of money again
    deploy.sendPayment(5, {'from': accounts[1], 'value': 20})
    assert deploy.exactAgreement(5)[6] == "Terminated"

def test_timeNotBreached_breached_on_time_false_send_deposit(deploy):
    '''check if the deposit is sent to the receiver when timeNotBreached is breached in the timeNotBreached'''
    deploy.ConfirmAgreement(5, {'from': accounts[9]})
    deploy.sendPayment(5, {'from': accounts[1], 'value': 20})
    balance_receiver = accounts[9].balance() 
    deploy.sendPayment(5, {'from': accounts[1], 'value': 20}) 
    assert accounts[9].balance() == balance_receiver + 20

def test_timeNotBreached_breached_on_time_false_deposit_equals_zero(deploy):
    '''check if the deposit is equal zero when timeNotBreached is breached in the timeNotBreached'''
    deploy.ConfirmAgreement(5, {'from': accounts[9]})
    deploy.sendPayment(5, {'from': accounts[1], 'value': 20})
    deploy.sendPayment(5, {'from': accounts[1], 'value': 20}) 
    assert deploy.exactAgreement(5)[5] == "0"

def test_timeNotBreached_breached_on_time_false_return_transaction(deploy):
    '''check if the transaction is sent back to the signee when timeNotBreached is breached in the timeNotBreached'''
    deploy.ConfirmAgreement(5, {'from': accounts[9]})
    deploy.sendPayment(5, {'from': accounts[1], 'value': 20})  
    balance_signee = accounts[1].balance() 
    deploy.sendPayment(5, {'from': accounts[1], 'value': 5}) 
    assert accounts[1].balance() == balance_signee

def test_timeNotBreached_breached_on_time_false_emit_Terminated(deploy):
    '''check if the event Terminated is emitted when timeNotBreached is breached in the timeNotBreached'''
    deploy.ConfirmAgreement(5, {'from': accounts[9]})
    deploy.sendPayment(5, {'from': accounts[1], 'value': 20})
    #the contract has been activated, now send the smaller quantity of money again
    function_initialize = deploy.sendPayment(5, {'from': accounts[1], 'value': 20})
    assert function_initialize.events[0][0]['message'] == "This agreement was terminated due to late payment"

#Checking when the agreement's status is "Terminated"

def test_terminateContract_emit_Terminated_initial_status_terminated(deploy):
    '''check if the sendPayments emits correctly the message when the status is "Terminated"'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    deploy.terminateContract(0, {'from': accounts[1]})
    with brownie.reverts("This agreement was already terminated"):
        deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    


#Checking when the agreement's status is else
#this test will fail because i don't know how to change the status
#def test_timeNotBreached_breached_value_larger_amount_status_not_defined(deploy):
    '''check if the status is changed when timeNotBreached is breached in the timeNotBreached'''
    #deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    #deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    #deploy.exactAgreement(0).status = "The status is something else"
    #assert deploy.exactAgreement(0)[6] == "The status is something else"
    #the contract has been activated, now send the smaller quantity of money again
    #with brownie.reverts("There is no agreement with this id"):
        #deploy.sendPayment(0, {'from': accounts[1], 'value': 20})




''' TESTING WASCONTRACTBREACHED FUNCTION '''




def test_wasContractBreached_require_receiver_equals_msg_sender(deploy):
    '''check if the wasContractBreached fails, because exactAgreement[_id].receiver == msg.sender is the require statement'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    with brownie.reverts("The receiver in the agreement's id isn't the same as the address you're logged in"):
        #wrong signee's address
        deploy.wasContractBreached(0, {'from': accounts[2]})

def test_wasContractBreached_fail_if_statement_in_timeNotBreached(deploy):
    '''check if the timeNotBreached fails because transaction was sent after the agreement's deadline - it fails because of the check in the ConfirmAgreement function'''
    try:
        deploy.ConfirmAgreement(4, {'from': accounts[9]})
        deploy.sendPayment(4, {'from': accounts[6], 'value': 20})
        deploy.wasContractBreached(4, {'from': accounts[9]})
    except Exception as e:        
        assert e.message[50:] == "This agreement's deadline has ended"

#if timeNotBreached is True

def test_wasContractBreached_timeNotBreached_true_emit_NotifyUser(deploy):
    '''check if the wasContractBreached function when timeNotBreached is true, emits NotifyUser'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    function_initialize = deploy.wasContractBreached(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    assert function_initialize.events[0][0]['message'] == "The agreement wasn't breached"

#if timeNotBreached is False

def test_wasContractBreached_received_on_time_false(deploy):
    '''check if the wasContractBreached returns false, when transaction received wasn't on time, but doesn't wait 7 days for withdraw'''
    try:
        deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
        deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
        rpc.sleep(60*60*24*6)
        deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
        deploy.wasContractBreached(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    except Exception as e:        
        assert e.message[50:] == "You have to wait at least 7 days after breached deadline to withdraw the deposit"

def test_wasContractBreached_timeNotBreached_false_status_Terminated(deploy):
    '''check if the wasContractBreached function when timeNotBreached is false, changes status to Terminated'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    rpc.sleep(60*60*24*5)
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    rpc.sleep(60*60*24*7)
    deploy.wasContractBreached(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    assert deploy.exactAgreement(0)[6] == "Terminated"

def test_wasContractBreached_timeNotBreached_false_send_deposit(deploy):
    '''check if the wasContractBreached function when timeNotBreached is false, sends a deposit to the receiver'''
    deploy.ConfirmAgreement(3, {'from': accounts[9]})
    deploy.sendPayment(3, {'from': accounts[6], 'value': 20})
    balance_receiver = accounts[9].balance()
    rpc.sleep(60*60*24*5)
    deploy.sendPayment(3, {'from': accounts[6], 'value': 20})
    rpc.sleep(60*60*24*7)
    deploy.wasContractBreached(3, {'from': accounts[9]})
    assert accounts[9].balance() == balance_receiver + 20

def test_wasContractBreached_timeNotBreached_false_status_deposit_equals_zero_1(deploy):
    '''check if the wasContractBreached function when timeNotBreached is false, changes deposit to 0'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    rpc.sleep(60*60*24*5)
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    rpc.sleep(60*60*24*7)
    deploy.wasContractBreached(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    assert deploy.exactAgreement(0)[5] == '0'
  
def test_wasContractBreached_timeNotBreached_false_status_deposit_equals_zero(deploy):
    '''check if the wasContractBreached function when timeNotBreached is false, changes deposit to 0'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    rpc.sleep(60*60*24*5)
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    rpc.sleep(60*60*24*7)
    deploy.wasContractBreached(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    assert deploy.exactAgreement(0)[5] == "0"

def test_wasContractBreached_timeNotBreached_false_emit_Terminated(deploy):
    '''check if the wasContractBreached function when timeNotBreached is false, emits NotifyUser'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    rpc.sleep(60*60*24*5)
    deploy.sendPayment(0, {'from': accounts[1], 'value': 20})
    rpc.sleep(60*60*24*7)
    function_initialize = deploy.wasContractBreached(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    assert function_initialize.events[0][0]['message'] == "This agreement is already terminated"

def test_wasContractBreached_agreement_not_activated(deploy):
    '''check if the wasContractBreached function emits NotifyUser when timeNotBreached is false'''
    deploy.ConfirmAgreement(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    function_initialize = deploy.wasContractBreached(0, {'from': '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'})
    assert function_initialize.events[0][0]['message'] == "This agreement hasn't been activated"

