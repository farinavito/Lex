// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/// @title Implementing a legal contract: Person A commits sending X amount of ether to person B every Y days for Z days
/// @author Farina Vito
contract AgreementBetweenSubjects {

  /// @notice Defining the agreement 
  /// @param id A unique identifier of the agreement
  /// @param signee The person who commits sending the the money to the receiver 
  /// @param receiver The person receiving the money
  /// @param amount The quantity of money that the signee commits sending to the receiver
  /// @param transactionCreated Unix timestamp when transaction was sent
  /// @param deposit The agreed amount of the deposit by both sides for the contract. Initial state will be zero
  /// @param status Representation of different stages in the agreement: Created, Activated, Terminated
  /// @param approved Confirmation of the agreedDeposit by the receiver. Stages: Not Confirmed, Confirmed
  /// @param agreementStartDateThe unix timestamp of the agreement's creation. FRONTEND
  /// @param everyTimeUnit The number of days till when the signee's transaction has to be created. First calculated by agreementStartDate+ everyTimeUnit. Later just adding everyTimeUnit
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
  //NEW
  //storing the owner's address
  address public owner;
  //NEW
	constructor (){
		owner = msg.sender;
	}
  //NEW
  //allows only the owner
	modifier onlyOwner(){
		require(msg.sender == owner, "You are not the owner");
		_;
	}

  uint16 internal locked = 1;

  //doesn't allow reentrance attack
  modifier noReentrant() {
        require(locked == 1, "No re-entrancy");
        locked = 2;
        _;
        locked = 1;
    }
  //NEW
  /// @dev The commission we charge
  uint256 public commission = 1;

  //NEW
  uint256 public withdrawal_amount_owner;

   /// @dev Saving the money sent for the signee to withdraw it
  mapping(address => uint256) private withdraw_signee;

  /// @dev Saving the money sent for the receiver to withdraw it
  mapping(address => uint256) private withdraw_receiver;

  /// @dev A unique identifier of theagreement. The same as the id.
  mapping(uint256 => Agreement) public exactAgreement;
  /// @dev Used to increase the id of the agreements in the "createAgreements" function
  uint numAgreement;

  /// @dev Storing the id's of the agreements that the signee has created
  mapping(address => uint[]) public mySenderAgreements;

  /// @dev Storing the id's of the agreements of the same receiver address
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
  

  /// @notice Initializing the position from where the everyTimeUnit is added
  function initializingPositionPeriod(uint256 _id) private {
      exactAgreement[_id].positionPeriod = exactAgreement[_id].agreementStartDate+ (exactAgreement[_id].everyTimeUnit);
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
          //NEW
          //storing the amount sent subtracted by commission
          uint256 changedAmount;
          //NEW
          changedAmount = msg.value - commission;
          //NEW
          //adding the commission to a owner's withdrawal
          withdrawal_amount_owner += commission;
          //NEW
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
        require(exactAgreement[_id].agreementStartDate<= block.timestamp, "The agreement hasn't started yet");
        require(exactAgreement[_id].howLong + exactAgreement[_id].agreementStartDate> block.timestamp, "The agreement's deadline has ended");
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

  function withdrawAsTheSignee(uint256 _id) external payable noReentrant{
	  require(exactAgreement[_id].signee == msg.sender, "Your logged in address isn't the same as the agreement's signee");
    require(withdraw_signee[exactAgreement[_id].signee] > 0, "There aren't any funds to withdraw");
	  uint256 current_amount = withdraw_signee[exactAgreement[_id].signee];
	  withdraw_signee[exactAgreement[_id].signee] = 0;
	  (bool sent, ) = exactAgreement[_id].signee.call{value: current_amount}("");
    require(sent, "Failed to send Ether");
	  emit NotifyUser("Withdrawal has been transfered");
  }

  function withdrawAsTheReceiver(uint256 _id) external payable noReentrant{
    require(exactAgreement[_id].receiver == msg.sender, "Your logged in address isn't the same as the agreement's receiver");
    require(withdraw_receiver[exactAgreement[_id].receiver] > 0, "There aren't any funds to withdraw");
    uint256 current_amount = withdraw_receiver[exactAgreement[_id].receiver];
    withdraw_receiver[exactAgreement[_id].receiver] = 0;
    (bool sent, ) = exactAgreement[_id].receiver.call{value: current_amount}("");
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

  //function for the receiver - wether he agrees with the terms or not, approves the contract or not. If he does, we are able to activate it, otherwise we can't
  function confirmAgreement(uint256 _id) external {
    if (keccak256(bytes(exactAgreement[_id].approved)) == keccak256(bytes("Confirmed"))){
		  emit NotifyUser("The agreement is already confirmed");
	  }else if(keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Terminated"))){
      emit NotifyUser("The agreement is already terminated");
    }else{
      require(exactAgreement[_id].receiver == msg.sender, "Only the receiver can confirm the agreement");
      //cannot confirm an agreement that ends in the past
      require(exactAgreement[_id].howLong + exactAgreement[_id].agreementStartDate>= block.timestamp, "The agreement's deadline has ended");
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
      if(timeWasntBreached(_id)){
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
    }else if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Created"))){
      if(exactAgreement[_id].agreementStartDate+ (6*60*60*24) > block.timestamp){
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

  function getWithdrawalSignee(uint256 _id) external view returns(uint256){
    require(exactAgreement[_id].signee == msg.sender, "Your logged in address isn't the same as the agreement's signee");
    return withdraw_signee[exactAgreement[_id].signee];
  }

  function getWithdrawalReceiver(uint256 _id) external view returns(uint256){
    require(exactAgreement[_id].receiver == msg.sender, "Your logged in address isn't the same as the agreement's receiver");
    return withdraw_receiver[exactAgreement[_id].receiver];
  }
  //NEW
  function changeCommission(uint256 _newCommission) external onlyOwner{
		require(commission > 0 && commission < 10*15 + 1, "Commission doesn't followed the rules");
		commission = _newCommission;
		emit NotifyUser("Commission changed");
	}

  fallback() external {}
  receive() external payable {}

}