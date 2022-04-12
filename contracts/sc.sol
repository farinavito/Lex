// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

/// @title Implementing a legal contract: Person A commits sending X amount to person B every Y time period for the duration of Z time starting at Q
/// @author Farina Vito

//import "https://github.com/farinavito/ProtectSmartContracts/blob/main/project/AddressProtector/contracts/protector.sol";
//import "farinavito/ProtectSmartContracts@1.0.0/project/AddressProtector/contracts/protector.sol";

//this contract is added only for testing purposes of AgreementBetweenSubjects
contract AddressProtector {

    /// @notice Adding votes for candidates by protectors
    mapping (address => mapping(address => bool)) public alreadyVoted;
    
    /// @notice Candidate for protectorWaitingToBeOwner
    mapping (address => uint256) public candidatesVotes;

    /// @notice Whitelisted accounts that can access withdrawal_amount_owner
    mapping(address => bool) public whitelist;
        
    /// @notice Storing the owner's address
    address public smartcontractOwner;

    /// @notice Storing the next in line to be an owner
    address public protectorWaitingToBeOwner;

    ///@notice Storing all protectors
    address[] internal allprotectorsaddresses;

    /// @notice Emit all the addresses of the protectors
    event showAllProtectors(address indexed _address);


    constructor (
        address _protectorOwner,
        address _protectorWaitingToBeOwner, 
        address _protector1, 
        address _protector2, 
        address _protector3, 
        address _protector4, 
        address _protector5 
        ){
        smartcontractOwner = _protectorOwner;
        protectorWaitingToBeOwner = _protectorWaitingToBeOwner;

        allprotectorsaddresses.push(_protector1);
        allprotectorsaddresses.push(_protector2);
        allprotectorsaddresses.push(_protector3);
        allprotectorsaddresses.push(_protector4);
        allprotectorsaddresses.push(_protector5);

        //initialize the protectors
        for (uint8 i = 1; i <= 5; i++){
            candidatesVotes[protectorWaitingToBeOwner] += 1;
            alreadyVoted[allprotectorsaddresses[i - 1]][protectorWaitingToBeOwner] = true;
        }
    }

    /// @notice Checking if the input address is the protector
    function checkWhichProtector(address _address) internal view returns(uint8 _i){
        for (uint8 i = 0; i < 5; i++){
            if (allprotectorsaddresses[i] == _address){
                return i;
            } else if (i != 4){
                continue;
            } else {
                revert("You don't have permissions");
            }
        }
    }

    /// @notice Returning all addresses of protectors
    function returnProtectors() public {
        for (uint8 i = 0; i < 5; i++){
            emit showAllProtectors(allprotectorsaddresses[i]);
        }
    }

    /// @notice Changing the owner and the waitingToBeOwner
    function changeOwner(address _nextInline) external {
        require(protectorWaitingToBeOwner == msg.sender, "You don't have permissions");
        require(candidatesVotes[_nextInline] >= 3, "Not all protectors agree with this address");
        //reinitializing to 0
        candidatesVotes[smartcontractOwner] = 0;
        for (uint8 i = 0; i < 5; i++){
            alreadyVoted[allprotectorsaddresses[i]][smartcontractOwner] = false;
        }

        smartcontractOwner = protectorWaitingToBeOwner;
        protectorWaitingToBeOwner = _nextInline;
    }
    
    /// @notice Voting for candidates by protectors
    function voteCandidate(address _nextInLine) external {
        checkWhichProtector(msg.sender);
        require(alreadyVoted[msg.sender][_nextInLine] == false, "You have entered your vote");
        alreadyVoted[msg.sender][_nextInLine] = true;
        candidatesVotes[_nextInLine] += 1;
    }

    /// @notice remove vote by the protector from previously voted protectorWaitingToBeOwner
    function removeVote(address _nextInLine) external {
        checkWhichProtector(msg.sender);
        require(alreadyVoted[msg.sender][_nextInLine] == true, "You haven't voted for this address");
        alreadyVoted[msg.sender][_nextInLine] = false;
        candidatesVotes[_nextInLine] -= 1;
    }

    /// @notice Only the protectorOwner can access
    modifier onlyprotectorOwner(){
        require(msg.sender == smartcontractOwner, "You are not the owner");
        _;
    }

    /// @notice Adding address to the whitelist
    function addToWhitelist(address _address) external onlyprotectorOwner {
        whitelist[_address] = true;
    }
    
    /// @notice Removing address from the whitelist
    function removedFromWhitelist(address _address) external onlyprotectorOwner {
        whitelist[_address] = false;
    }
    
}

contract AgreementBetweenSubjects {
  //5. if the last transaction in sentPayment is ok, return the deposit to the signee

  /// @notice Defining the agreement 
  /// @param id A unique identifier of the agreement
  /// @param signee The person who commits sending the money to the receiver 
  /// @param receiver The person receiving the money
  /// @param amount The quantity of money that the signee commits sending to the receiver
  /// @param transactionCreated Unix timestamp when transaction was sent
  /// @param deposit The first transaction sent to the agreement. Initial state will be zero
  /// @param status Representation of different stages in the agreement: Created, Activated, Terminated
  /// @param agreementStartDate Unix timestamp of the agreement's starting date 
  /// @param everyTimeUnit The number of days till when the signee's transaction has to be created. First calculated by agreementStartDate + everyTimeUnit. Later just adding everyTimeUnit
  /// @param positionPeriod A pointer to the current everyTimeUnit parameter
  /// @param howLong The number of days till the agreement expires
  struct Agreement{
    uint256 id; 
    address signee;
    address payable receiver; 
    uint256 amount;
    uint256 transactionCreated;
    uint256 deposit;
    string status;
    uint256 agreementStartDate;
    uint256 everyTimeUnit;
    uint256 positionPeriod;
    uint256 howLong;
  }

  /// @notice Using against re-entrancy
  uint16 internal locked = 1;

  /// @notice The commission we charge
  uint256 public commission = 1;

  /// @notice The commission collected
  uint256 private withdrawal_amount_owner;

  /// @notice Returning the total amount of ether that was commited
  uint256 public totalEtherCommited;

  /// @notice Returning the total amount of deposit that was sent to the receiver
  uint256 public totalDepositSent; 

  /// @notice Used to increase the id of the agreements in the "createAgreements" function
  uint numAgreement;


  /// @notice Doesn't allow reentrance attack
  modifier noReentrant() {
    require(locked == 1, "No re-entrancy");
    locked = 2;
    _;
    locked = 1;
  }

  /// @notice Saving the money sent for the signee to withdraw it
  mapping(address => uint256) private withdraw_signee;

  /// @notice Saving the money sent for the receiver to withdraw it
  mapping(address => uint256) private withdraw_receiver;

  /// @notice A unique identifier of the agreement. The same as the id.
  mapping(uint256 => Agreement) public exactAgreement;

  /// @notice Storing the id's of the agreements that the signee has created
  mapping(address => uint[]) public mySenderAgreements;

  /// @notice Storing the id's of the agreements of the same receiver address
  mapping(address => uint[]) public myReceiverAgreements;  


  /// @notice Emitting agreement's info 
  event AgreementInfo(
    uint256 agreementId,
    address agreementSignee, 
    address agreementReceiver, 
    uint256 agreementAmount,
    uint256 agreementTransactionCreated,
    uint256 agreementDeposit,
    string agreementStatus,
    uint256 agreementStartDate,
    uint256 agreementTimePeriods,
    uint256 agreementPositionPeriod,
    uint256 agreementTimeDuration
  );

  /// @notice After the contract is terminated, emit an event with a message
  event Terminated(string message);

  /// @notice After other event than Terminated happens, emit it and send a message
  event NotifyUser(string message);


  AddressProtector public accessingProtectors;

  constructor(address _address) {
    accessingProtectors = AddressProtector(_address);
  }

  /// @notice Initializing the position from where the everyTimeUnit is added
  function initializingPositionPeriod(uint256 _id) private {
    exactAgreement[_id].positionPeriod = exactAgreement[_id].agreementStartDate + exactAgreement[_id].everyTimeUnit;
  }

  /// @notice Verifying that the transaction created was sooner than its deadline 
  function timeNotBreached(uint256 _id) private returns(bool){
    //period till when we have to receive the transaction
    uint256 extendedPeriod = exactAgreement[_id].positionPeriod + (6*60*60*24);
    //if the transaction sent was on time, transaction was received on time and transaction was sent before the agreement's deadline
    if (exactAgreement[_id].positionPeriod  >= exactAgreement[_id].transactionCreated && extendedPeriod >= block.timestamp && exactAgreement[_id].howLong + exactAgreement[_id].agreementStartDate>= block.timestamp){ 
      exactAgreement[_id].positionPeriod += exactAgreement[_id].everyTimeUnit;
      return true;
    } else{
      return false;
    }
  }

  /// @notice Verifying that the transaction created was sooner than its deadline without incrementing positionPeriod
  function timeWasntBreached(uint256 _id) private view returns(bool){
    //period till when we have to receive the transaction
    uint256 extendedPeriod = exactAgreement[_id].positionPeriod + (6*60*60*24);
    //if the transaction sent was on time, transaction was received on time and transaction was sent before the agreement's deadline
    if (exactAgreement[_id].positionPeriod  >= exactAgreement[_id].transactionCreated && extendedPeriod >= block.timestamp && exactAgreement[_id].howLong + exactAgreement[_id].agreementStartDate>= block.timestamp){ 
      return true;
    } else{
      return false;
    }
  }

  /// @notice Checking if the payment sent is the last payment of the agreement
  function isLastPayment(uint256 _id) private view returns(bool){
    if (exactAgreement[_id].howLong + exactAgreement[_id].agreementStartDate < exactAgreement[_id].positionPeriod){
      return true;
    } else {
      return false;
    }
  }

  /// @notice Sending the payment based on the status of the agreement
  function sendPayment(uint256 _id) external payable {
    require(exactAgreement[_id].signee == msg.sender, "Only the signee can pay the agreement's terms");
    if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Activated"))){
      //save the time of calling this function
      exactAgreement[_id].transactionCreated = block.timestamp;
      //if the transaction sent was on time and transaction was sent before the agreement's deadline
      if (timeNotBreached(_id)){
        //if the transaction was on time and it was enough
        if (exactAgreement[_id].amount <= msg.value){
          //storing the amount sent subtracted by commission
          uint256 changedAmount;
          changedAmount = msg.value - commission;
          //adding the commission to a owner's withdrawal
          withdrawal_amount_owner += commission;
          //send the transaction to the receiver
          withdraw_receiver[exactAgreement[_id].receiver] += changedAmount;
          //change the total amount of ether sent
          totalEtherCommited += changedAmount;
          //returning any access ethers sent to the receiver
          withdraw_signee[exactAgreement[_id].signee] += msg.value - exactAgreement[_id].amount;
          emit NotifyUser("Transaction was sent to the receiver");
        //if the transaction was on time, but it wasn't enough
        } else {
            //return the transaction to the signee
            withdraw_signee[exactAgreement[_id].signee] += msg.value;
            emit NotifyUser("The amount sent is lower than in the agreement");      
        }
      //if the transaction wasn't sent on time
      } else {
        exactAgreement[_id].status = "Terminated";
        //sending the deposit to the receiver
        withdraw_receiver[exactAgreement[_id].receiver] += exactAgreement[_id].deposit;
        //change the total amount of deposit sent to the receiver
        totalDepositSent += exactAgreement[_id].deposit;
        //ensure that the deposit is reduced to 0
        exactAgreement[_id].deposit = 0;
        //return the transaction to the signee
        withdraw_signee[exactAgreement[_id].signee] += msg.value;
        emit Terminated("The agreement was terminated due to late payment");
      }
    } else if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Created"))){
        require(exactAgreement[_id].agreementStartDate <= block.timestamp, "The agreement hasn't started yet");
        require(exactAgreement[_id].howLong + exactAgreement[_id].agreementStartDate > block.timestamp, "The agreement's deadline has ended");
        require(exactAgreement[_id].amount <= msg.value, "The deposit is not the same as agreed in the terms");
        exactAgreement[_id].status = "Activated";
        //set the position period
        initializingPositionPeriod(_id);
        emit NotifyUser("The agreement has been activated"); 
    } else if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Terminated"))){
          //return the transaction to the signee
          revert("The agreement is already terminated");
    } else {
          //return the transaction to the signee
          revert("There is no agreement with this id");
    }
  }  

  /// @notice The signee withdrawing the money that belongs to his/her address
  function withdrawAsTheSignee(uint256 _id) external payable noReentrant {
	  require(exactAgreement[_id].signee == msg.sender, "Your logged in address isn't the same as the agreement's signee");
    require(withdraw_signee[exactAgreement[_id].signee] > 0, "There aren't any funds to withdraw");
	  (bool sent, ) = exactAgreement[_id].signee.call{value:  withdraw_signee[exactAgreement[_id].signee]}("");
    require(sent, "Failed to send Ether");
    withdraw_signee[exactAgreement[_id].signee] = 0;
	  emit NotifyUser("Withdrawal has been transfered");
  }

  /// @notice The receiver withdrawing the money that belongs to his/her address
  function withdrawAsTheReceiver(uint256 _id) external payable noReentrant {
    require(exactAgreement[_id].receiver == msg.sender, "Your logged in address isn't the same as the agreement's receiver");
    require(withdraw_receiver[exactAgreement[_id].receiver] > 0, "There aren't any funds to withdraw");
    (bool sent, ) = exactAgreement[_id].receiver.call{value: withdraw_receiver[exactAgreement[_id].receiver]}("");
    require(sent, "Failed to send Ether");
    withdraw_receiver[exactAgreement[_id].receiver] = 0;
    emit NotifyUser("Withdrawal has been transfered");
  }
  
  /// @notice The owner withdrawing the money that belongs to his address
  function withdrawAsTheOwner() external payable noReentrant {
    require(accessingProtectors.whitelist(msg.sender), "You aren't whitelisted");
		require(withdrawal_amount_owner > 0, "There aren't any funds to withdraw");
    (bool sent, ) = msg.sender.call{value: withdrawal_amount_owner}("");
    require(sent, "Failed to send Ether");
    withdrawal_amount_owner = 0;
    emit NotifyUser("Withdrawal has been transfered");
  }

  /// @notice Creating a new agreement
  function createAgreement(
    address payable _receiver, 
    uint256 _amount,
    uint256 _everyTimeUnit,
    uint256 _howLong,
    uint256 _startOfTheAgreement
    ) external payable {
        require(_amount > 0 && _everyTimeUnit > 0 && _howLong > 0, "All input data must be larger than 0");
        require(_howLong > _everyTimeUnit, "The period of the payment is greater than the duration of the contract");
        require(msg.value >= _amount, "Deposit has to be at least the size of the amount");
        require(_startOfTheAgreement >= block.timestamp, "The agreement can't be created in the past");

        uint256 agreementId = numAgreement++;

        //creating a new agreement
        Agreement storage newAgreement = exactAgreement[agreementId];
        newAgreement.id = agreementId;
        newAgreement.signee = msg.sender;
        newAgreement.receiver = _receiver;
        newAgreement.amount = _amount;

        //the amount that is actually deposited to the agreement. We initialize it with 0
        newAgreement.deposit = msg.value;
        //the status of the agreement when its created
        newAgreement.status = "Created";
        //when was the agreement created
        newAgreement.agreementStartDate= _startOfTheAgreement;
        //period of the payment
        newAgreement.everyTimeUnit = _everyTimeUnit;
        //position of the end of the period in which the signee has to send the money (for example: ...every 3 weeks... - this period needs to update itself)
        newAgreement.positionPeriod = 0;
        //how long will the agreement last
        newAgreement.howLong = _howLong;
        //storing the ids of the agreements and connecting them to msg.sender's address so we can display them to the frontend
        mySenderAgreements[msg.sender].push(agreementId);
        //storing the ids of the agreements and connecting them to _receiver's address so we can display them to the frontend
        myReceiverAgreements[_receiver].push(agreementId);

        emit AgreementInfo(
          newAgreement.id, 
          newAgreement.signee, 
          newAgreement.receiver, 
          newAgreement.amount,
          newAgreement.transactionCreated,
          newAgreement.deposit, 
          newAgreement.status,
          newAgreement.agreementStartDate, 
          newAgreement.everyTimeUnit, 
          newAgreement.positionPeriod, 
          newAgreement.howLong
          ); 
  }

  /// @notice Receiver checking if the contract has been breached
  function wasContractBreached(uint256 _id) external {
    require(exactAgreement[_id].receiver == msg.sender, "Your logged in address isn't the same as the agreement's receiver");
    //checking if the agreement was Activated
    if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Activated"))){
      //checking if the deadline was breached
      if (timeWasntBreached(_id)){
        emit NotifyUser("The agreement wasn't breached");
      } else {
        //receiver has to wait 7 days after the breached date to withdraw the deposit
        require(exactAgreement[_id].positionPeriod + (60*60*24*7) < block.timestamp, "You can't withdraw the deposit before 7 days after breached deadline");
        //terminate the agreement
        exactAgreement[_id].status = "Terminated";
        //return deposit to receiver
        withdraw_receiver[exactAgreement[_id].receiver] += exactAgreement[_id].deposit;
        //ensure that the deposit is reduced to 0
        exactAgreement[_id].deposit = 0;
        //change the total amount of deposit sent to the receiver
        totalDepositSent += exactAgreement[_id].deposit;
        emit Terminated("The agreement has been terminated");
      } 
    } else if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Created"))){
      if (exactAgreement[_id].agreementStartDate + (6*60*60*24) > block.timestamp){
        emit NotifyUser("The agreement wasn't breached");
      } else {
        //receiver has to wait 7 days after the breached date to withdraw the deposit
        require(exactAgreement[_id].positionPeriod + (60*60*24*7) < block.timestamp, "You can't withdraw the deposit before 7 days after breached deadline");
        //terminate the agreement
        exactAgreement[_id].status = "Terminated";
        //return deposit to receiver
        withdraw_receiver[exactAgreement[_id].receiver] += exactAgreement[_id].deposit;
        //ensure that the deposit is reduced to 0
        exactAgreement[_id].deposit = 0;
        //change the total amount of deposit sent to the receiver
        totalDepositSent += exactAgreement[_id].deposit;
        emit Terminated("The agreement has been terminated");
      }
    } else {
        emit NotifyUser("The agreement is already terminated");
    }
  } 

  /// @notice Return the withdrawal amount of the agreement's signee
  function getWithdrawalSignee(uint256 _id) external view returns(uint256){
    require(exactAgreement[_id].signee == msg.sender, "Your logged in address isn't the same as the agreement's signee");
    return withdraw_signee[exactAgreement[_id].signee];
  }

  /// @notice Return the withdrawal amount of the agreement's receiver
  function getWithdrawalReceiver(uint256 _id) external view returns(uint256){
    require(exactAgreement[_id].receiver == msg.sender, "Your logged in address isn't the same as the agreement's receiver");
    return withdraw_receiver[exactAgreement[_id].receiver];
  }

  /// @notice Return the withdrawal amount of the owner
  function getWithdrawalOwner() external view returns(uint256){
    require(accessingProtectors.whitelist(msg.sender), "You aren't whitelisted");
    return withdrawal_amount_owner;
  }
  
  /// @notice Changing the commission
  function changeCommission(uint256 _newCommission) external {
    require(accessingProtectors.whitelist(msg.sender), "You aren't whitelisted");
		require(_newCommission > 0 && _newCommission < 10**15 + 1, "Commission doesn't follow the rules");
		commission = _newCommission;
		emit NotifyUser("Commission changed");
	}
   

  fallback() external {}
  receive() external payable {}

}