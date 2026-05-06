import React from 'react';
import ErrorBar from '../components/ErrorBar';
import SuccessBar from '../components/SuccessBar';
import Box from '@mui/material/Box';
import BlackListUser from '../components/BlackListUser';
import makeRequest from '../helpers/Fetch';

const BlackList = () => {
  const [errorOpen, setErrorOpen] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [successOpen, setSuccessOpen] = React.useState(false);
  const [successMessage, setSuccessMessage] = React.useState('');
  const [blackResult, setBlackResult] = React.useState([]);
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
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    try {
      makeRequest(`/blacklist?token=${body.token}`, 'GET').then(data => {
        setBlackResult(data.blacklist);
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }, []);
  
  return (
    <>
      {errorOpen &&
        <ErrorBar errorMessage={errorMessage} errorOpen={errorOpen} setErrorOpen={setErrorOpen}></ErrorBar>
      }
      {successOpen &&
        <SuccessBar successMessage={successMessage} successOpen={successOpen} setSuccessOpen={setSuccessOpen}></SuccessBar>
      }
      <div>
        <Box sx={{ margin: '8px', float: 'left', width: 5, height: 35, backgroundColor: 'primary.dark' }} />
        <h1 style={{ color: '#1565c0' }}>Your Black List</h1>
      </div>
      {blackResult.map((result, index) => {
        return <BlackListUser key={index} userId={result.user_id} userPhoto={result.user_profile_photo} userName={result.user_name} userDescription={result.user_description} userView={result.user_views} userFriend={result.friend_num}
                setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage} setSuccessOpen={setSuccessOpen} setSuccessMessage={setSuccessMessage}
                blackResult={blackResult} setBlackResult={setBlackResult} ></BlackListUser>
      })}
    </>
  );
}
 
export default BlackList;
