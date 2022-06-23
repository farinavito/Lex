// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

/** remove AddressProtector and its whitelisting
    remove id as the parameter in 2 functions
 */

/// @title Implementing a legal contract: Person A commits sending X amount to person B every Y time period for the duration of Z time starting at Q
/// @author Farina Vito

contract AgreementBetweenSubjects {

  /// @notice Defining the agreement 
  /// @param id A unique identifier of the agreement
  /// @param sender The person who commits sending the money to the receiver 
  /// @param receiver The person receiving the money
  /// @param amount The quantity of money that the sender commits sending to the receiver
  /// @param transactionCreated Unix timestamp when transaction was sent
  /// @param deposit The first transaction sent to the agreement. Initial state will be zero
  /// @param status Representation of different stages in the agreement: Created, Activated, Terminated
  /// @param agreementStartDate Unix timestamp of the agreement's starting date 
  /// @param everyTimeUnit The number of days till when the sender's transaction has to be created. First calculated by agreementStartDate + everyTimeUnit. Later just adding everyTimeUnit
  /// @param positionPeriod A pointer to the current everyTimeUnit parameter
  /// @param howLong The number of days till the agreement expires
  struct Agreement{
    uint256 id; 
    address sender;
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

  /// @notice Returning the total amount of ether that was commited
  uint256 public totalEtherCommited;

  /// @notice Returning the total amount of deposit that was sent to the receiver
  uint256 public totalDepositSent; 

  /// @notice Used to increase the id of the agreements in the "createAgreements" function
  uint numAgreement = 1;


  /// @notice Doesn't allow reentrance attack
  modifier noReentrant() {
    require(locked == 1, "No re-entrancy");
    locked = 2;
    _;
    locked = 1;
  }

  /// @notice Saving the money sent for the sender to withdraw it
  mapping(address => uint256) private withdraw_sender;

  /// @notice Saving the money sent for the receiver to withdraw it
  mapping(address => uint256) private withdraw_receiver;

  /// @notice A unique identifier of the agreement. The same as the id.
  mapping(uint256 => Agreement) public exactAgreement;

  /// @notice Storing the id's of the agreements that the sender has created
  mapping(address => uint[]) public mySenderAgreements;

  /// @notice Storing the id's of the agreements of the same receiver address
  mapping(address => uint[]) public myReceiverAgreements;  


  /// @notice Emitting agreement's info 
  event AgreementInfo(
    uint256 agreementId,
    address agreementsender, 
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
    require(exactAgreement[_id].sender == msg.sender, "Only the sender can pay the agreement's terms");
    if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Activated"))){
      //save the time of calling this function
      exactAgreement[_id].transactionCreated = block.timestamp;
      //if the transaction sent was on time and transaction was sent before the agreement's deadline
      if (timeNotBreached(_id)){
        //if the transaction was on time and it was enough
        if (exactAgreement[_id].amount <= msg.value){
          //send the transaction to the receiver
          withdraw_receiver[exactAgreement[_id].receiver] += msg.value;
          //change the total amount of ether sent
          totalEtherCommited += msg.value;
          //returning any excess ethers sent to the receiver
          withdraw_sender[exactAgreement[_id].sender] += msg.value - exactAgreement[_id].amount;
          //checking if this is the last payment
          if (isLastPayment(_id)){
            //sending deposit to the sender
            withdraw_sender[exactAgreement[_id].sender] += exactAgreement[_id].deposit;
            //increased the global counter of deposit sent
            totalDepositSent += exactAgreement[_id].deposit;
            //ensure that the deposit is reduced to 0
            exactAgreement[_id].deposit = 0;
            //terminate the contract
            exactAgreement[_id].status = "Terminated";
            emit NotifyUser("You have fullfilled all your obligations");
          } else {
            emit NotifyUser("Transaction was sent to the receiver");
          }
        //if the transaction was on time, but it wasn't enough
        } else {
            //return the transaction to the sender
            withdraw_sender[exactAgreement[_id].sender] += msg.value;
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
        //return the transaction to the sender
        withdraw_sender[exactAgreement[_id].sender] += msg.value;
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
          //return the transaction to the sender
          revert("The agreement is already terminated");
    } else {
          //return the transaction to the sender
          revert("There is no agreement with this id");
    }
  }  

  /// @notice The sender withdrawing the money that belongs to his/her address
  function withdrawAsThesender() external payable noReentrant {
    require(withdraw_sender[msg.sender] > 0, "There aren't any funds to withdraw");
	  (bool sent, ) = msg.sender.call{value:  withdraw_sender[msg.sender]}("");
    require(sent, "Failed to send Ether");
    withdraw_sender[msg.sender] = 0;
	  emit NotifyUser("Withdrawal has been transfered");
  }

  /// @notice The receiver withdrawing the money that belongs to his/her address
  function withdrawAsTheReceiver() external payable noReentrant {
    require(withdraw_receiver[msg.sender] > 0, "There aren't any funds to withdraw");
    (bool sent, ) = msg.sender.call{value: withdraw_receiver[msg.sender]}("");
    require(sent, "Failed to send Ether");
    withdraw_receiver[msg.sender] = 0;
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
        newAgreement.sender = msg.sender;
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
        //position of the end of the period in which the sender has to send the money (for example: ...every 3 weeks... - this period needs to update itself)
        newAgreement.positionPeriod = 0;
        //how long will the agreement last
        newAgreement.howLong = _howLong;
        //storing the ids of the agreements and connecting them to msg.sender's address so we can display them to the frontend
        mySenderAgreements[msg.sender].push(agreementId);
        //storing the ids of the agreements and connecting them to _receiver's address so we can display them to the frontend
        myReceiverAgreements[_receiver].push(agreementId);

        emit AgreementInfo(
          newAgreement.id, 
          newAgreement.sender, 
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

  /// @notice Return the withdrawal amount of the agreement's sender
  function getWithdrawalsender() external view returns(uint256){
    return withdraw_sender[msg.sender];
  }

  /// @notice Return the withdrawal amount of the agreement's receiver
  function getWithdrawalReceiver() external view returns(uint256){
    return withdraw_receiver[msg.sender];
  }
   

  fallback() external {}
  receive() external payable {}

}