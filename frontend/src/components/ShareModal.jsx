import React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import makeRequest from "../helpers/Fetch";
import PropTypes from 'prop-types';
import MessageUser from '../components/MessageUser';

const modal = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  overflow: 'scroll',
  height: '100%',
  maxHeight: 300,
  display: 'block',
  bgcolor: 'background.paper',
  border: '1px solid #000',
  boxShadow: 24
}

const small_modal = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  height: '100%',
  maxHeight: 110,
  display: 'block',
  width: 340,
  bgcolor: 'background.paper',
  border: '1px solid #000',
  boxShadow: 24
}

const header = {
  padding:'12px 7px',
}

const content = {
  padding: 0
}

const ShareModal = (props) => {
  const [friendList, setFriendList] = React.useState([]);
  const [selectUserId, setSelectUserId] = React.useState('');
  const [confirmModalOpen, setConfirmModalOpen] = React.useState(false);

  const handleConfirmModalClose = () => setConfirmModalOpen(false);

  React.useEffect(() => {
    const body = {
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    if (body.token !== '') {
      try {
        makeRequest(`/friendlist?token=${body.token}`, 'GET').then(data => {
          setFriendList(data.friendlist);
        });
      } catch (error) {
        props.setErrorOpen(true);
        props.setErrorMessage(error);
      }
    }
  }, []);

  const shareButton = async () => {
    const currentDate = new Date();
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
    const dateString = currentDate.toLocaleString('en-US', options).replace(/(\d+)\/(\d+)\/(\d+)/, '$3-$1-$2').replace(',', '');
    const body = {
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
      friend_id: parseInt(selectUserId),
      url: window.location.href,
      cover: props.cover,
      time: dateString
    }
    try {
      await makeRequest(`/message/share/${props.location}`, 'POST', body);
      props.setSuccessOpen(true);
      props.setSuccessMessage('Share success');
      setConfirmModalOpen(true);
    } catch (error) {
      props.setErrorOpen(true);
      props.setErrorMessage("error");
    }
  };

  const jumpToMessage = () => {
    window.location = '/message';
  }

  const handleShareModalClose = () => {
    props.setShareModalOpen(false);
    setSelectUserId('');
  }

  return (
    <>
      <Modal
        open={props.shareModalOpen}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={modal}>
          <div style={header}>
            <h2>You want to share with</h2>
          </div>
          <div style={content}>
            <div className='row' style={{ width: '100%', margin: '0px' }}>
              {friendList.map((user, index) => {
                return  <div key={index} onClick={() => setSelectUserId(user.user_id)} style={{ backgroundColor: selectUserId === user.user_id ? 'grey' : 'white' }}>
                          <MessageUser userPhoto={user.user_profile_photo} userName={user.user_name}></MessageUser>
                        </div>
              })}
            </div>
            <br/>
            <div className='row'>
              <div className='col-9'>
                <Button size='small' color='primary' variant="outlined" onClick={shareButton} style={{ height: '30px', width: '10%', marginLeft: '40px'}}>Share</Button>
                <Modal
                  open={confirmModalOpen}
                  aria-labelledby="modal-modal-title"
                  aria-describedby="modal-modal-description"
                >
                  <Box sx={small_modal}>
                    <div style={header}>
                      <h4>Jump to the message page</h4>
                    </div>
                    <div className='row' style={content}>
                      <div className='col' style={{ textAlign: 'center' }}>
                        <Button size='small' color='primary' variant="outlined" onClick={jumpToMessage} style={{ height: '30px', width: '125px', marginBottom: '8px' }}>Yes</Button>
                      </div>
                      <div className='col' style={{ textAlign: 'center' }}>
                        <Button size='small' color='primary' variant="outlined" onClick={handleConfirmModalClose} style={{ height: '30px', width: '125px', marginBottom: '8px' }}>No</Button>
                      </div>                          
                    </div>
                  </Box>              
                </Modal>
              </div>
              <div className='col-3'>
                <Button size='small' color='primary' variant="outlined" onClick={handleShareModalClose} style={{ height: '30px', width: '10%'}}>Close</Button>
              </div>
            </div> 
          </div>
        </Box>              
      </Modal>
    </>
  );
}

ShareModal.propTypes = {
  location: PropTypes.string,
  cover: PropTypes.string,
  shareModalOpen: PropTypes.bool,
  setShareModalOpen: PropTypes.func,
  setErrorOpen: PropTypes.func,
  setErrorMessage: PropTypes.func,
  setSuccessOpen: PropTypes.func,
  setSuccessMessage: PropTypes.func,
}

export default ShareModal;
