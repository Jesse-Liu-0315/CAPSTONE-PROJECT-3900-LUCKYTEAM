import React from 'react';
import ErrorBar from '../components/ErrorBar';
import SuccessBar from '../components/SuccessBar';
import Box from '@mui/material/Box';
import defaultPhoto from '../user_profile_default.png';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import makeRequest from "../helpers/Fetch";
import { useParams } from 'react-router-dom';
import LoginModal from '../components/LoginModal';
import ShareModal from '../components/ShareModal';

const OtherProfile = () => {
  const userID = useParams().userId.toString();
  const [errorOpen, setErrorOpen] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [successOpen, setSuccessOpen] = React.useState(false);
  const [successMessage, setSuccessMessage] = React.useState('');
  const [photo, setPhoto] = React.useState(defaultPhoto);
  const [firstName, setFirstName] = React.useState('');
  const [lastName, setLastName] = React.useState('');
  const [FullName, setFullName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [age, setAge] = React.useState('');
  const [sex, setSex] = React.useState('Undefined');
  const [occupation, setOccupation] = React.useState('');
  const [area, setArea] = React.useState('');
  const [description, setDescription] = React.useState('');
  const [block, setBlock] = React.useState(false);
  const [friend, setFriend] = React.useState(false);
  const [views, setViews] = React.useState(0);
  const [friends, setFriends] = React.useState(0);
  const [admin, setAdmin] = React.useState(false);
  const [tag, setTag] = React.useState('');
  const [shareModalOpen, setShareModalOpen] = React.useState(false);
  const [loginModalOpen, setLoginModalOpen] = React.useState(false);
  const [hasNewMessage, setHasNewMessage] = React.useState('');

  React.useEffect(() => {
    if (localStorage.getItem('luckyToken') != null) {
      const intervalId = setInterval(async () => {
        const body = {
          token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken')
        };
        const response = await makeRequest(`/message/unread?token=${body.token}`, 'GET');
        setHasNewMessage(response.unread_messages);
      }, 10000);
      return () => clearInterval(intervalId);
    }
  }, []);

  React.useEffect(() => {
    if (localStorage.getItem('luckyToken') != null) {
      if (hasNewMessage > 0) {
        setSuccessOpen(true);
        setSuccessMessage('You have ' + hasNewMessage + ' new messages!');
      }
    }
  }, [hasNewMessage]);

  React.useEffect(() => {
    const body = {
      userID: parseInt(userID),
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken')
    }
    try {
      makeRequest(`/user?userID=${body.userID}&token=${body.token}`, 'GET').then(data => {
        setFriend(data.friends);
        setBlock(data.blacklist);
        setFirstName(data.user['user_firstname'] === null ? '' : data.user['user_firstname']);
        setLastName(data.user['user_lastname'] === null ? '' : data.user['user_lastname']);
        setFullName(data.user['user_name'] === null ? '' : data.user['user_name']);
        setEmail(data.user['user_email'] === null ? '' : data.user['user_email']);
        setAge(data.user['user_age'] === null ? '' : data.user['user_age']);
        setSex(data.user['user_sex']);
        setOccupation(data.user['user_occupation'] === null ? '' : data.user['user_occupation']);
        setArea(data.user['user_area'] === null ? '' : data.user['user_area']);
        setDescription(data.user['user_description'] === null ? '' : data.user['user_description']);
        setPhoto(data.user['user_profile_photo'] === null ? defaultPhoto : data.user['user_profile_photo']);
        setViews(data.user['user_views']);
        setFriends(data.numFriends);
        setAdmin(data.permission);
        setTag(data.user['user_tag'] === null ? '' : data.user['user_tag']);
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }, []);

  const jumpToWatchedList = () => {
    window.location = `/OtherPeopleWatchedList/${userID}/${FullName}`;
  }

  const jumpToWishList = () => {
    window.location = `/OtherPeopleWishList/${userID}/${FullName}`;
  }

  const blockButton = async () => {
    if (userID === localStorage.getItem('luckyId')) {
      setErrorOpen(true);
      setErrorMessage('You can not block yourself');
      return;
    }
    const body = {
      black_id:parseInt(userID),
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken')
    }
    if (block === false && body.token !== '') {
      await makeRequest('/blacklist/add', 'POST', body);
      setBlock(true);
      setSuccessOpen(true);
      setSuccessMessage('block user success');
    } else if (block === true && body.token !== '') {
      await makeRequest('/blacklist/remove', 'POST', body);
      setBlock(false);
      setSuccessOpen(true);
      setSuccessMessage('remove block user success');
    } else {
      setErrorOpen(true);
      setErrorMessage('You need login first');
    }
  }
    
  const friendButton = async () => {
    if (userID === localStorage.getItem('luckyId')) {
      setErrorOpen(true);
      setErrorMessage('You can not make friend with yourself');
      return;
    }
    const currentDate = new Date();
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
    const dateString = currentDate.toLocaleString('en-US', options).replace(/(\d+)\/(\d+)\/(\d+)/, '$3-$1-$2').replace(',', '');
    const body = {
      friend_id:parseInt(userID),
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
      time: dateString
    }
    if (friend === false && body.token !== '') {
      await makeRequest('/friendlist/add', 'POST', body);
      setFriend(true);
      setSuccessOpen(true);
      setSuccessMessage('add friend success');
    } else if (friend === true && body.token !== '') {
      await makeRequest('/friendlist/remove', 'POST', body);
      setFriend(false);
      setSuccessOpen(true);
      setSuccessMessage('remove friend success');
    } else {
      setErrorOpen(true);
      setErrorMessage('You need login first');
    }
  }

  const modifyTagButton = async () => {
    const body = {
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
      user_id: parseInt(userID),
      tag: tag
    }
    try {
      await makeRequest('/user/addtag', 'POST', body);
      setSuccessOpen(true);
      setSuccessMessage('Modifty Tag success');
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }

  const handleShareModalOpen = () => {
    if (localStorage.getItem('luckyToken') === null) {
      setLoginModalOpen(true);
      return;
    }
    setShareModalOpen(true);
  }

  return (
    <>
      {errorOpen &&
        <ErrorBar errorMessage={errorMessage} errorOpen={errorOpen} setErrorOpen={setErrorOpen}></ErrorBar>
      }
      {successOpen &&
        <SuccessBar successMessage={successMessage} successOpen={successOpen} setSuccessOpen={setSuccessOpen}></SuccessBar>
      }
      <LoginModal loginModalOpen={loginModalOpen} setLoginModalOpen={setLoginModalOpen}
        setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage}></LoginModal>
      <ShareModal location={'user'} cover={photo} shareModalOpen={shareModalOpen} setShareModalOpen={setShareModalOpen} 
        setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage} setSuccessOpen={setSuccessOpen} setSuccessMessage={setSuccessMessage}
      ></ShareModal>
      <div>
        <Box sx={{ margin: '8px', float: 'left', width: 5, height: 35, backgroundColor: 'primary.dark' }} />
        <h1 style={{ color: '#1565c0' }}>Other User Profile</h1>
      </div>
      <div className='container text-center' style={{ width: "100%" }}>
        <div className='row justify-content-md-center' style={{ marginBottom: '15px' }}>
          <div className="col"></div>
          <div className="col">
            <div> 
              <img src={photo} alt="User" style={{ height: '150px', width: '150px' }} />
            </div>
          </div>
          <div className="col">
            <div className='row'>
              <Button size='small' variant="outlined" onClick={jumpToWishList} style={{ height: '30px', width: '140px', marginBottom: '8px' }}>Wish List</Button>
            </div>
            <div className='row'>
              <Button size='small' variant="outlined" onClick={jumpToWatchedList} style={{ height: '30px', width: '140px', marginBottom: '8px' }}>Watched List</Button>
            </div>
            <div className='row'>
              {friend === false ? 
                (<Button size='small' variant="outlined" onClick={friendButton} style={{ height: '30px', width: '140px', marginBottom: '8px' }}>Make a friend</Button>
                ) : (
                <Button size='small' variant="outlined" onClick={friendButton} style={{ height: '30px', width: '140px', marginBottom: '8px' }}>Remove friend</Button>
              )}
            </div>
            <div className='row'>
              {block === false ?
                (<Button size='small' variant="outlined" onClick={blockButton} style={{ height: '30px', width: '140px' }}>BLOCK</Button>
                ) : (
                  <Button size='small' variant="outlined" onClick={blockButton} style={{ height: '30px', width: '140px' }}>UNBLOCK</Button>
              )}
            </div>
            <div className='row' style={{ color: 'grey', height: '18px', width: '140px', textAlign: 'center' }}>
              <div style={{ padding: '0px'}}>
                {views} Views
              </div>
            </div>
            <div className='row' style={{ color: 'grey', height: '18px', width: '140px', textAlign: 'center' }}>
              <div style={{ padding: '0px'}}>
                {friends} Friends
              </div>
            </div>
            <div className='row'style={{ padding:'10px 0px'}}>
              <Button size='small' variant="outlined" onClick={handleShareModalOpen} style={{ eight: '30px', width: '140px' }}>Share user</Button>
            </div>
          </div>
        </div>
        <div className="row mb-3">
          {admin &&
            <>
            <div className='col'></div>
            <div className='col'>
              <TextField size='small' label="Tag" defaultValue={tag}  onChange={(event) => setTag(event.target.value)} variant="outlined"/>
            </div>
            <div className='col' style={{ textAlign:'start' }}>
              <div className='row'>
                <Button size='small' variant="outlined" style={{ height: '30px', width: '140px' }} onClick={modifyTagButton}>Modify Tag</Button>
              </div>
            </div>
            </>
          }
          {!admin &&
            <>
              <div className='col'></div>
              <div className='col'>
                <TextField size='small' label="Tag" value={tag} variant="outlined" InputProps={{readOnly: true}}/>
              </div>
              <div className='col'></div>
            </>
          }
        </div>
        <div className="row">
          <div className="mb-3">
            <TextField size='small' label="First Name" value={firstName} variant="outlined" InputProps={{readOnly: true}} />
          </div>
        </div>
        <div className="row">
          <div className="mb-3">
            <TextField size='small' label="Last Name" value={lastName} variant="outlined" InputProps={{readOnly: true}} />
          </div>
        </div>
        <div className="row">
          <div className="mb-3">
            <TextField size='small' label="Email" value={email} variant="outlined" InputProps={{readOnly: true}} />
          </div>
        </div>
        <div className="row">
          <div className="mb-3">
            <TextField size='small' label="Age" value={age} variant="outlined" InputProps={{readOnly: true}} />
          </div>
        </div>
        <div className="row">
          <div className="mb-3">
            <TextField size='small' label="Sex" value={sex} variant="outlined" InputProps={{readOnly: true}} />
          </div>
        </div>
        <div className="row">
          <div className="mb-3">
            <TextField size='small' label="Occupation" value={occupation} variant="outlined" InputProps={{readOnly: true}} />
          </div>
        </div>
        <div className="row">
          <div className="mb-3">
            <TextField size='small' label="Area" value={area} variant="outlined" InputProps={{readOnly: true}} />
        </div>
        </div>
        <div className="row">
          <div className="mb-3">
            <TextField multiline sx={{ width: '223px' }} size='small' label="Description" value={description} variant="outlined" InputProps={{readOnly: true}} />
          </div>
        </div>
      </div>
    </>
  );
}

export default OtherProfile;
