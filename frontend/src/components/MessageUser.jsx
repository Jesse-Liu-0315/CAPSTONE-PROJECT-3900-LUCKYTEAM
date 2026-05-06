import React from 'react';
import defaultPhoto from '../user_profile_default.png';
import PropTypes from 'prop-types';

const MessageUser = (props) => {
  return (
    <>
      <div className='row' style={{ marginTop: '10px', marginLeft: '10px', width: '220px' }}>
        <div className='col-auto'>
            <img src={props.userPhoto === null ? defaultPhoto : props.userPhoto} style={{ width: '50px' }} alt="user_photo" />
        </div>
        <div className='col-auto'>
            {props.userName}
        </div>
        <div className='col-auto' style={{color:'red'}}>
            {props.userUnReadMessageNUM}
        </div>
      </div>
      <hr style={{ marginTop: '10px', marginLeft: '20px' }}/>
    </>
  );
}

MessageUser.propTypes = {
    userPhoto: PropTypes.string,
    userName: PropTypes.string,
    userUnReadMessageNUM: PropTypes.number,
}

export default MessageUser;
