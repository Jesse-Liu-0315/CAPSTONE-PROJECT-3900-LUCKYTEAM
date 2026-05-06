import React from 'react';
import PropTypes from 'prop-types';
import defaultPhoto from '../user_profile_default.png';
import Button from '@mui/material/Button';
import makeRequest from '../helpers/Fetch';

const MessageUserSend = (props) => {

  const handleDeleteMessages = async () => {
    const body = {
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
      message_id: parseInt(props.messageId),
    }
    try {
      await makeRequest('/message/delete', 'POST', body);
      props.getMessageFromServer();
    } catch (error) {
      props.setErrorOpen(true);
      props.setErrorMessage(error);
    } 
  }

  return (
    <>
      <hr/>
      <div className='row' style={{ display:'flex', justifyContent: 'flex-end', margin: '0px' }}>
        <img src={props.messagePhoto === null ? defaultPhoto : props.messagePhoto} style={{ width: '74px', height: '43px' }} alt="user_photo" />
        {props.messageSender}
      </div>
      <div className='row' style={{ margin: '0px', marginBottom: '10px' }}>
        <img src={props.messageContent} style={{ width: '200px', height: '200px',padding:'12px 0' }} alt='message'/>
      </div>
      <div>
        <Button variant="outlined" size='small' sx={{ padding: '0px' }} onClick={handleDeleteMessages}>&#128465;</Button>
      </div>
    </>
  );
}

MessageUserSend.propTypes = {
  getMessageFromServer: PropTypes.func,
  setErrorOpen: PropTypes.func,
  setErrorMessage: PropTypes.func,
  messageId: PropTypes.number,
  messageSender: PropTypes.string,
  messageContent: PropTypes.string,
}

export default MessageUserSend;