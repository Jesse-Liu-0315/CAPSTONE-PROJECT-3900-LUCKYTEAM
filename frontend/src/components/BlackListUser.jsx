import React from 'react';
import PropTypes from 'prop-types';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import makeRequest from '../helpers/Fetch';

const BlackListUser = (props) => {

  const jumpToUserProfile = () => {
    window.location = `/otherprofile/${props.userId}`;;
  }

  const deleteButton = async () => {
    const body = {
      black_id: parseInt(props.userId),
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    try {
      await makeRequest('/blacklist/remove', 'POST', body);
      props.setSuccessOpen(true);
      props.setSuccessMessage('Delete a black user success');
      const newBlackResult = props.blackResult.filter(value => value.user_id !== props.userId);
      props.setBlackResult(newBlackResult);
    } catch (error) {
      props.setErrorOpen(true);
      props.setErrorMessage(error);
    }
  }

  return (
    <>
      <div className="row" style={{ marginLeft: '20px' }}>
        <div className="col-auto" style={{ padding: '0px' }}>
          <img src={props.userPhoto} className="img-fluid rounded-start" alt="User" style={{ width: '105px', height: '150px', cursor: 'pointer' }} onClick={jumpToUserProfile}/>
        </div>
        <div className="col-auto" style={{ padding: '0px'}}>
          <div className="card-body" style={{ position: 'relative', height: '100%', width: '500px', padding: '0px', paddingLeft: '5px' }}>
            <h5 style={{ cursor: 'pointer' }} className="card-title">{props.userName}</h5>
            <p>{props.userDescription}</p>
            <p className="card-text" style={{ position: 'absolute', bottom: 20, marginBottom: '0px' }}><small className="text-muted">{props.userView} Views</small></p>
            <p className="card-text"><small className="text-muted" style={{ position: 'absolute', bottom: 0 }}>{props.userFriend} Friends</small></p>
          </div>
        </div>
        <div className="col justify-content-end" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginRight: '50px' }}>
          <IconButton size="large" aria-label="delete" onClick={deleteButton}>
            <DeleteIcon fontSize="large" />
          </IconButton>
        </div>
      </div>
      <hr/>
    </>
  );
}

BlackListUser.propTypes = {
  setErrorOpen: PropTypes.func,
  setErrorMessage: PropTypes.func,
  setSuccessOpen: PropTypes.func,
  setSuccessMessage: PropTypes.func,
  blackResult: PropTypes.array,
  setBlackResult: PropTypes.func,
  userId: PropTypes.number,
  userPhoto: PropTypes.string,
  userName: PropTypes.string,
  userDescription: PropTypes.string,
  userFriend: PropTypes.number,
}

export default BlackListUser;
