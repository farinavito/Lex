// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title Implementing a legal contract: Person A commits sending X amount to person B every Y time period for the duration of Z time starting at Q
/// @author Farina Vito

contract AgreementBetweenSubjects {

  /// @notice Defining the agreement 
  /// @param id A unique identifier of the agreement
  /// @param signee The person who commits sending the money to the receiver 
  /// @param receiver The person receiving the money
  /// @param amount The quantity of money that the signee commits sending to the receiver
  /// @param transactionCreated Unix timestamp when transaction was sent
  /// @param deposit The first transaction sent to the agreement. Initial state will be zero
  /// @param status Representation of different stages in the agreement: Created, Activated, Terminated
  /// @param approved Confirmation of the agreedDeposit by the receiver: Not Confirmed, Confirmed
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
    string approved;
    uint256 agreementStartDate;
    uint256 everyTimeUnit;
    uint256 positionPeriod;
    uint256 howLong;
  }

  
  /// @notice Storing the owner's address
  address public owner;

  /// @notice Using against re-entrancy
  uint16 internal locked = 1;

  /// @notice The commission we charge
  uint256 public commission = 1;

  /// @notice The commission collected
  uint256 private withdrawal_amount_owner;

  /// @notice Used to increase the id of the agreements in the "createAgreements" function
  uint numAgreement;
  
	constructor (){
		owner = msg.sender;
	}
  
  /// @notice Allows only the owner
	modifier onlyOwner(){
		require(msg.sender == owner, "You are not the owner");
		_;
	}

  /// @notice Doesn't allow reentrance attack
  modifier noReentrant() {
    require(locked == 1, "No re-entrancy");
    locked = 2;
    _;
    locked = 1;
  }

  /// @notice Allows only the whitelisted addresses
  modifier onlyWhitelisted() {
    require(isWhitelisted(msg.sender), "You aren't whitelisted");
    _;
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

  /// @notice Whitelisted accounts that can access withdrawal_amount_owner
  mapping(address => bool) private whitelist;
  
  /// @notice Blacklisted accounts that can't access the smart contract
  mapping(address => bool) private blacklist;


  /// @notice Emitting agreement's info 
  event AgreementInfo(
    uint256 agreementId,
    address agreementSignee, 
    address agreementReceiver, 
    uint256 agreementAmount,
    uint256 agreementTransactionCreated,
    uint256 agreementDeposit,
    string agreementStatus,
    string agreementApproved,
    uint256 agreementStartDate,
    uint256 agreementTimePeriods,
    uint256 agreementPositionPeriod,
    uint256 agreementTimeDuration
  );

  /// @notice After the contract is terminated, emit an event with a message
  event Terminated(string message);

  /// @notice After other event than Terminated happens, emit it and send a message
  event NotifyUser(string message);
 
  /// @notice When an account is white- or blacklisted
  event AddedToTheList(address account);
 
  /// @notice When an account is removed from white- or blacklist
  event RemovedFromTheList(address account);


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

  /// @notice Sending the payment based on the status of the agreement
  function sendPayment(uint256 _id) external payable {
    require(exactAgreement[_id].signee == msg.sender, "Only the owner can pay the agreement's terms");
    //the agreement has to be confirmed from the receiver of the agreement
    require(keccak256(bytes(exactAgreement[_id].approved)) == keccak256(bytes("Confirmed")), "The receiver has to confirm the contract");
    if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Activated"))){
      //save the time of calling this function
      exactAgreement[_id].transactionCreated = block.timestamp;
      //if the transaction sent was on time and transaction was sent before the agreement's deadline
      if (timeNotBreached(_id)){
        if (exactAgreement[_id].amount <= msg.value){
          //storing the amount sent subtracted by commission
          uint256 changedAmount;
          changedAmount = msg.value - commission;
          //adding the commission to a owner's withdrawal
          withdrawal_amount_owner += commission;
          //send the transaction to the receiver
          withdraw_receiver[exactAgreement[_id].receiver] += changedAmount;
          emit NotifyUser("Transaction was sent to the receiver");
        //if the transaction was on time, but it wasn't enough
        } else {
            exactAgreement[_id].status = "Terminated"; 
            //sending the deposit to the receiver
            withdraw_signee[exactAgreement[_id].signee] += exactAgreement[_id].deposit;
            //ensure that the deposit is reduced to 0
            exactAgreement[_id].deposit = 0;
            //return the transaction to the signee
            withdraw_signee[exactAgreement[_id].signee] += msg.value;
            emit Terminated("The agreement was terminated due to different amount sent than in the terms");      
        }
      //if the transaction wasn't sent on time
      } else {
        exactAgreement[_id].status = "Terminated";
        //sending the deposit to the receiver
        withdraw_receiver[exactAgreement[_id].receiver] += exactAgreement[_id].deposit;
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
	  uint256 current_amount = withdraw_signee[exactAgreement[_id].signee];
	  withdraw_signee[exactAgreement[_id].signee] = 0;
	  (bool sent, ) = exactAgreement[_id].signee.call{value: current_amount}("");
    require(sent, "Failed to send Ether");
	  emit NotifyUser("Withdrawal has been transfered");
  }

  /// @notice The receiver withdrawing the money that belongs to his/her address
  function withdrawAsTheReceiver(uint256 _id) external payable noReentrant {
    require(exactAgreement[_id].receiver == msg.sender, "Your logged in address isn't the same as the agreement's receiver");
    require(withdraw_receiver[exactAgreement[_id].receiver] > 0, "There aren't any funds to withdraw");
    uint256 current_amount = withdraw_receiver[exactAgreement[_id].receiver];
    withdraw_receiver[exactAgreement[_id].receiver] = 0;
    (bool sent, ) = exactAgreement[_id].receiver.call{value: current_amount}("");
    require(sent, "Failed to send Ether");
    emit NotifyUser("Withdrawal has been transfered");
  }
  
  /// @notice The owner withdrawing the money that belongs to his address
  function withdrawAsTheOwner() external payable noReentrant onlyWhitelisted{
		require(withdrawal_amount_owner > 0, "There aren't any funds to withdraw");
    uint256 current_amount = withdrawal_amount_owner; 
    withdrawal_amount_owner = 0;
    (bool sent, ) = msg.sender.call{value: current_amount}("");
    require(sent, "Failed to send Ether");
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
        //initialize the approved term
        newAgreement.approved = "Not Confirmed";
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
          newAgreement.approved,
          newAgreement.agreementStartDate, 
          newAgreement.everyTimeUnit, 
          newAgreement.positionPeriod, 
          newAgreement.howLong
          ); 
  }

  /// @notice Confirming the agreement by the receiver, thus enabling it to receive funds
  function confirmAgreement(uint256 _id) external {
    if (keccak256(bytes(exactAgreement[_id].approved)) == keccak256(bytes("Confirmed"))){
		  emit NotifyUser("The agreement is already confirmed");
	  } else if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Terminated"))){
      emit NotifyUser("The agreement is already terminated");
    } else {
      require(exactAgreement[_id].receiver == msg.sender, "Only the receiver can confirm the agreement");
      //cannot confirm an agreement that ends in the past
      require(exactAgreement[_id].howLong + exactAgreement[_id].agreementStartDate >= block.timestamp, "The agreement's deadline has ended");
      //confirm the agreement
      exactAgreement[_id].approved = "Confirmed";
      //emit that the agreement was confirmed
      emit NotifyUser("The agreement was confirmed");
	  }
  }

  /// @notice Terminating the agreement by the signee
  function terminateContract(uint256 _id) external {
    if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Terminated"))){
		  emit NotifyUser("The agreement is already terminated");
	  } else if (exactAgreement[_id].howLong + exactAgreement[_id].agreementStartDate< block.timestamp){
        require(exactAgreement[_id].signee == msg.sender, "Only the owner can terminate the agreement");
        exactAgreement[_id].status = "Terminated";
        //return the deposit to the signee
        withdraw_signee[exactAgreement[_id].signee] += exactAgreement[_id].deposit;
        //ensure that the deposit is reduced to 0
        exactAgreement[_id].deposit = 0;
        emit Terminated("The agreement has been terminated");
    } else {
        require(exactAgreement[_id].signee == msg.sender, "Only the owner can terminate the agreement");
        exactAgreement[_id].status = "Terminated";
        //return the deposit to the receiver
        withdraw_receiver[exactAgreement[_id].receiver] += exactAgreement[_id].deposit;
        //ensure that the deposit is reduced to 0
        exactAgreement[_id].deposit = 0;
        emit Terminated("The agreement has been terminated");
	  }
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
  function getWithdrawalOwner() external view onlyWhitelisted returns(uint256){
    return withdrawal_amount_owner;
  }
  
  /// @notice Changing the commission
  function changeCommission(uint256 _newCommission) external onlyOwner{
		require(_newCommission > 0 && _newCommission < 10*15 + 1, "Commission doesn't follow the rules");
		commission = _newCommission;
		emit NotifyUser("Commission changed");
	}
  
  /// @notice Adding address to the whitelist
  function addToWhitelist(address _address) external onlyOwner {
    whitelist[_address] = true;
    emit AddedToTheList(_address);
  }
  
  /// @notice Removing address from the whitelist
  function removedFromWhitelist(address _address) external onlyOwner {
    whitelist[_address] = false;
    emit RemovedFromTheList(_address);
  }
  
  /// @notice Checking if the address is whitelisted
  function isWhitelisted(address _address) public view returns(bool) {
    return whitelist[_address];
  }
  
  /// @notice Adding address to the blacklist
  function addToBlacklist(address _address) external onlyOwner {
    blacklist[_address] = true;
    emit AddedToTheList(_address);
  }
  
  /// @notice Removing address from the blacklist
  function removedFromBlacklist(address _address) external onlyOwner {
    blacklist[_address] = false;
    emit RemovedFromTheList(_address);
  }
  
  /// @notice Checking if the address is blacklisted
  function isBlacklisted(address _address) public view returns(bool) {
    return blacklist[_address];
  }

  fallback() external {}
  receive() external payable {}

}