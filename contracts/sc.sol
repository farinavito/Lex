// SPDX-License-Identifier: MIT
pragma solidity 0.8.1;

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
  /// @param agreementTimeCreation The unix timestamp of the agreement's creation. FRONTEND
  /// @param everyTimeUnit The number of days till when the signee's transaction has to be created. First calculated by agreementTimeCreation + everyTimeUnit. Later just adding everyTimeUnit
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
    uint256 agreementTimeCreation;
    uint256 everyTimeUnit;
    uint256 positionPeriod;
    uint256 howLong;
  }

  bool internal locked;

  //doesn't allow reentrance attack
  modifier noReentrant() {
        require(!locked, "No re-entrancy");
        locked = true;
        _;
        locked = false;
    }

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
    uint256 agreementTimeCreation,
    uint256 agreementTimePeriods,
    uint256 agreementPositionPeriod,
    uint256 agreementTimeDuration
  );

  /// @notice After the contract is terminated, emit an event with a message
  event Terminated(string message );
  /// @notice After other event than Terminated happens, emit it and send a message
  event NotifyUser(string message);

  /// @notice Createing a new agreement
  function createAgreement(
    address payable _receiver, 
    uint256 _amount,
    uint256 _everyTimeUnit,
    uint256 _howLong
    ) public {
        require(_howLong > _everyTimeUnit, "The period of the payment is greater than the duration of the contract");
        uint256 agreementId = numAgreement++;
        //creating a new agreement
        Agreement storage newAgreement = exactAgreement[agreementId];
        newAgreement.id = agreementId;
        newAgreement.signee = msg.sender;
        newAgreement.receiver = _receiver;
        newAgreement.amount = _amount;

        //the amount that is actually deposited to the agreement. We initialize it with 0
        newAgreement.deposit = 0;
        //the status of the agreement when its created
        newAgreement.status = "Created";
        //initialize the approved term
        newAgreement.approved = "Not Confirmed";
        //when was the agreement created
        newAgreement.agreementTimeCreation = block.timestamp;
        //period of the payment
        newAgreement.everyTimeUnit = _everyTimeUnit * (1 days);
        //position of the end of the period in which the signee has to send the money (for example: ...every 3 weeks... - this period needs to update itself)
        newAgreement.positionPeriod = 0;
        //how long will the agreement last
        newAgreement.howLong = _howLong * (1 days);
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
          newAgreement.agreementTimeCreation, 
          newAgreement.everyTimeUnit, 
          newAgreement.positionPeriod, 
          newAgreement.howLong
          );
          
  }

  /// @notice Emiting the info of all the signee's agreements from the address given 
  function MySenderAgreements(address _myAddress) public {
      require(msg.sender == _myAddress, "The address provided doesn't correspond with the one you're logged in");
      for (uint256 i = 0; i < mySenderAgreements[_myAddress].length; i++){
          Agreement storage newAgreement = exactAgreement[mySenderAgreements[_myAddress][i]];
          emit AgreementInfo(
            newAgreement.id, 
            newAgreement.signee, 
            newAgreement.receiver, 
            newAgreement.amount,
            newAgreement.transactionCreated,
            newAgreement.deposit, 
            newAgreement.status,
            newAgreement.approved,
            newAgreement.agreementTimeCreation, 
            newAgreement.everyTimeUnit, 
            newAgreement.positionPeriod, 
            newAgreement.howLong
            );
      }
  }


  /// @notice Emiting the info of all the signee's agreements from the address given 
  function MyReceiverAgreements(address _myAddress) public {
      require(msg.sender == _myAddress, "The address provided doesn't correspond with the one you're logged in");
      for (uint256 i = 0; i < myReceiverAgreements[_myAddress].length; i++){
          Agreement storage newAgreement = exactAgreement[myReceiverAgreements[_myAddress][i]];
          emit AgreementInfo(
            newAgreement.id, 
            newAgreement.signee, 
            newAgreement.receiver, 
            newAgreement.amount,
            newAgreement.transactionCreated,
            newAgreement.deposit, 
            newAgreement.status,
            newAgreement.approved,
            newAgreement.agreementTimeCreation, 
            newAgreement.everyTimeUnit, 
            newAgreement.positionPeriod, 
            newAgreement.howLong
            );  
      }
    }


  /// @notice Initializing the position from where the everyTimeUnit is added
  function initializingPositionPeriod(uint256 _id) private {
      exactAgreement[_id].positionPeriod = exactAgreement[_id].agreementTimeCreation + (exactAgreement[_id].everyTimeUnit);
    }

  /// @notice Verifying that the transaction created was sooner than its deadline 
  function timeNotBreached(uint256 _id) private returns(bool){
      //period till when we have to receive the transaction
      uint256 extendedPeriod = exactAgreement[_id].positionPeriod + (5 * days);
      //if the transaction sent was on time, transaction was received on time and transaction was sent before the agreement's deadline
	    if (exactAgreement[_id].positionPeriod  >= exactAgreement[_id].transactionCreated && extendedPeriod >= block.timestamp && exactAgreement[_id].howLong + exactAgreement[_id].agreementTimeCreation >= block.timestamp){ 
        exactAgreement[_id].positionPeriod += exactAgreement[_id].everyTimeUnit;
		    return true;
	    } else{
		    return false;
	    }
    }

  /// @notice Verifying that the transaction created was sooner than its deadline without incrementing positionPeriod
  function timeWasntBreached(uint256 _id) private view returns(bool){
      //period till when we have to receive the transaction
      uint256 extendedPeriod = exactAgreement[_id].positionPeriod + (5 * days);
      //if the transaction sent was on time, transaction was received on time and transaction was sent before the agreement's deadline
	    if (exactAgreement[_id].positionPeriod  >= exactAgreement[_id].transactionCreated && extendedPeriod >= block.timestamp && exactAgreement[_id].howLong + exactAgreement[_id].agreementTimeCreation >= block.timestamp){ 
		    return true;
	    } else{
		    return false;
	    }
    }

  /// @notice Sending the payment based on the status of the agreement
  function sendPayment(uint256 _id) public payable noReentrant{
    require(exactAgreement[_id].signee == msg.sender, "Only the owner can pay the agreement's terms");
    //the agreement has to be confirmed from the receiver of the agreement
    require(keccak256(bytes(exactAgreement[_id].approved)) == keccak256(bytes("Confirmed")), "The receiver has to confirm the contract");
    if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Activated"))){
      //save the time of calling this function
      exactAgreement[_id].transactionCreated = block.timestamp;
      //if the transaction sent was on time and transaction was sent before the agreement's deadline
      if (timeNotBreached(_id)){
        if (exactAgreement[_id].amount <= msg.value){
          //send the transaction to the receiver
          (bool sent, ) = exactAgreement[_id].receiver.call{value: msg.value}("");
          require(sent, "Failed to send Ether");
          emit NotifyUser("Transaction was sent to the receiver");
        //if the transaction was on time, but it wasn't enough
        } else {
            exactAgreement[_id].status = "Terminated"; 
            //sending the deposit to the receiver
            (bool sent, ) = exactAgreement[_id].receiver.call{value: exactAgreement[_id].deposit}("");
            require(sent, "Failed to send Ether");
            //ensure that the deposit is reduced to 0
            exactAgreement[_id].deposit = 0;
            //return the transaction to the signee
            (bool send, ) = exactAgreement[_id].signee.call{value: msg.value}("");
            require(send, "Failed to send Ether");
            emit Terminated("This agreement was terminated due to different payment than in the terms");      
        }
      //if the transaction wasn't sent on time
      } else {
        exactAgreement[_id].status = "Terminated";
        //sending the deposit to the receiver
        (bool sent, ) = exactAgreement[_id].receiver.call{value: exactAgreement[_id].deposit}("");
        require(sent, "Failed to send Ether");
        //ensure that the deposit is reduced to 0
        exactAgreement[_id].deposit = 0;
        //return the transaction to the signee
        (bool send, ) = exactAgreement[_id].signee.call{value: msg.value}("");
        require(send, "Failed to send Ether"); 
        emit Terminated("This agreement was terminated due to late payment");
      }
    } else if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Created"))){
        require(exactAgreement[_id].howLong + exactAgreement[_id].agreementTimeCreation > block.timestamp, "This agreement's deadline has ended");
        require(exactAgreement[_id].amount <= msg.value, "The deposit is not the same as the agreed in the terms");
        exactAgreement[_id].status = "Activated";
        //set the position period
        initializingPositionPeriod(_id);
        //deposit the amount
        exactAgreement[_id].deposit = msg.value;
        emit NotifyUser("We have activate the agreement"); 
    } else if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Terminated"))){
          //return the transaction to the signee
          revert("This agreement was already terminated");
    } else {
          //return the transaction to the signee
          revert("There is no agreement with this id");
    }
  }

  /// @notice Terminating the agreement by the signee
  function terminateContract(uint256 _id) public noReentrant{
    if (keccak256(bytes(exactAgreement[_id].status)) == keccak256(bytes("Terminated"))){
		  emit NotifyUser("This agreement is already terminated");
	  }else{
      require(exactAgreement[_id].signee == msg.sender, "Only the owner can terminate the agreement");
      exactAgreement[_id].status = "Terminated";
      //return the deposit to the signee
      (bool sent, ) = exactAgreement[_id].signee.call{value: exactAgreement[_id].deposit}("");
      require(sent, "Failed to send Ether");
      //ensure that the deposit is reduced to 0
      exactAgreement[_id].deposit = 0;
      //return the msg.value to the signee
      //payable(exactAgreement[_id].signee).send(msg.value);
      emit Terminated("This agreement has been terminated");
	  }
  }

  /// @notice Receiver checking if the contract has been breached
  function wasContractBreached(uint256 _id) public noReentrant{
    require(exactAgreement[_id].receiver == msg.sender, "The receiver in the agreement's id isn't the same as the address you're logged in");
    //checking if the deadline was breached
    if(timeWasntBreached(_id)){
      emit NotifyUser("The agreement wasn't breached");
    } else {
        //receiver has to wait 7 days after the breached date to withdraw the deposit
        require(exactAgreement[_id].positionPeriod + 7 days < block.timestamp, "You have to wait at least 7 days after breached deadline to withdraw the deposit");
        //terminate the agreement
        exactAgreement[_id].status = "Terminated";
        //return deposit to receiver
        (bool sent, ) = exactAgreement[_id].receiver.call{value: exactAgreement[_id].deposit}("");
        require(sent, "Failed to send Ether");
        //ensure that the deposit is reduced to 0
        exactAgreement[_id].deposit = 0;
        emit Terminated("This agreement has been terminated");
    }
  }

  //function for the receiver - wether he agrees with the terms or not, approves the contract or not. If he does, we are able to activate it, otherwise we can't
  function ConfirmAgreement(uint256 _id) public {
    if (keccak256(bytes(exactAgreement[_id].approved)) == keccak256(bytes("Confirmed"))){
		  emit NotifyUser("This agreement is already confirmed");
	  }else{
      require(exactAgreement[_id].receiver == msg.sender, "Only the receiver confirm the agreement");
      //cannot confirm an agreement that ends in the past
      require(exactAgreement[_id].howLong + exactAgreement[_id].agreementTimeCreation > block.timestamp, "This agreement's deadline has ended");
      //confirm the agreement
      exactAgreement[_id].approved = "Confirmed";
      //emit that the agreement was confirmed
      emit NotifyUser("The agreement was confirmed");
	  }
  }

  fallback() external {}
  receive() external payable {}

}