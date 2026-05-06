import React from 'react';
import PropTypes from 'prop-types';
import defaultPhoto from '../user_profile_default.png';

const MessageFriendSend = (props) => {
  return (
    <>
      <hr/>
      <div className='row' style={{ margin: '0px' }}>
        <img src={props.messagePhoto === null ? defaultPhoto : props.messagePhoto} style={{ width: '74px', height: '43px', paddingLeft: '0px', paddingRight: '24px' }} alt="user_photo" />
        {props.messageSender}
      </div>
      <div className='row' style={{ margin: '0px', marginBottom: '10px' }}>
        <img src={props.messageContent} style={{ width: '200px', height: '200px', padding:'12px 0'}} alt='message'/>
      </div>
    </>
  );
}

MessageFriendSend.propTypes = {
  messageSender: PropTypes.string,
}

export default MessageFriendSend;