import React from 'react';
import ErrorBar from '../components/ErrorBar';
import SuccessBar from '../components/SuccessBar';
import Box from '@mui/material/Box';
import MessageUser from '../components/MessageUser';
import makeRequest from '../helpers/Fetch';
import Button from 'react-bootstrap/Button';
import { Button as MuiButton } from '@mui/material';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import MessageFriendSend from '../components/MessageFriendSend';
import MessageUserSend from '../components/MessageUserSend';
import MessagePhotoFriendSend from '../components/MessagePhotoFriendSend';
import MessagePhotoUserSend from '../components/MessagePhotoUserSend';
import fileToDataUrl from '../helpers/fileToDataUrl';

const Message = () => {
  const [myId, ] = React.useState(parseInt(localStorage.getItem('luckyId')));
  const [errorOpen, setErrorOpen] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [successOpen, setSuccessOpen] = React.useState(false);
  const [successMessage, ] = React.useState('');
  const [friendList, setFriendList] = React.useState([]);
  const [selectUserId, setSelectUserId] = React.useState('');
  const [messageEnter, setMessageEnter] = React.useState('');
  const [messageList, setMessageList] = React.useState([]);
  const messageContainerRef = React.useRef(null);
  const [selectedFile, setSelectedFile] = React.useState(null);
  
  const getFriendListFromServer = async () => {
    const body = {
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    try {
      makeRequest(`/friendlist?token=${body.token}`, 'GET').then(data => {
        const areEqual = JSON.stringify(friendList) === JSON.stringify(data.friendlist);
        if (!areEqual) {
          setFriendList(data.friendlist);
        }
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }
  
  React.useEffect(() => {
    getFriendListFromServer();
  }, []);

  React.useEffect(() => {
    const intervalId = setInterval(() => {
      getFriendListFromServer();
    }, 2000);

    return () => clearInterval(intervalId);
  });

  React.useEffect(() => {
    if (selectUserId !== '') { 
      const container = messageContainerRef.current;
      container.scrollTop = container.scrollHeight;
    }
  });

  const getMessageFromServer = async () => {
    if (selectUserId !== '') {
      const body = {
        token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
        friend_id: selectUserId,
      }
      try {
        makeRequest(`/message/list?token=${body.token}&friend_id=${body.friend_id}`, 'GET').then(data => {
          const areEqual = JSON.stringify(messageList) === JSON.stringify(data.messages);
          if (!areEqual) {
            setMessageList(data.messages);
          }
        });
      } catch (error) {
        setErrorOpen(true);
        setErrorMessage(error);
      }
    }
  }

  React.useEffect(() => {
    getMessageFromServer();
  }, [selectUserId]);

  React.useEffect(() => {
    const intervalId = setInterval(() => {
      getMessageFromServer();
    }, 2000);

    return () => clearInterval(intervalId);
  });

  const handleSendMessage = async () => {
    const currentDate = new Date();
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
    const dateString = currentDate.toLocaleString('en-US', options).replace(/(\d+)\/(\d+)\/(\d+)/, '$3-$1-$2').replace(',', '');
    if (selectedFile != null) {
      const body = {
        token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
        friend_id: parseInt(selectUserId),
        message: selectedFile,
        time: dateString,
        type: 'image',
      }
      try {
        await makeRequest('/message/send', 'POST', body);
        setSelectedFile(null);
        getMessageFromServer();
      } catch (error) {
        setErrorOpen(true);
        setErrorMessage(error);
      } 
    } else if (messageEnter !== '') {
      const body = {
        token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
        friend_id: parseInt(selectUserId),
        message: messageEnter,
        time: dateString,
        type: 'text',
      }
      try {
        await makeRequest('/message/send', 'POST', body);
        setMessageEnter('');
        getMessageFromServer();
      } catch (error) {
        setErrorOpen(true);
        setErrorMessage(error);
      }
    } else {
      setErrorOpen(true);
      setErrorMessage('You did not enter text or photo');
    }
  }

  const sendPhoto = (event) => {
    fileToDataUrl(event.target.files[0]).then(imgUrl => {
      setSelectedFile(imgUrl);
    })
  };

  return (
    <>
      {errorOpen &&
        <ErrorBar errorMessage={errorMessage} errorOpen={errorOpen} setErrorOpen={setErrorOpen}></ErrorBar>
      }
      {successOpen &&
        <SuccessBar successMessage={successMessage} successOpen={successOpen} setSuccessOpen={setSuccessOpen}></SuccessBar>
      }
      <div className='row' style={{ width: '100%' }}>
        <div className='col-auto' style={{ padding: '0px', maxHeight: 'calc(100vh - 80px)', overflowY: 'scroll', overflowX: 'hidden' }}>
          {friendList.map((user, index) => {
            return  <div key={index} onClick={() => setSelectUserId(user.user_id)}>
                      <MessageUser userPhoto={user.user_profile_photo} userName={user.user_name} userUnReadMessageNUM={user.unread_num}></MessageUser>
                    </div>
          })}
        </div>
        <div className='col-auto' style={{ padding: '0px' }}>
          <Box sx={{ margin: '8px',float: 'left', width: 2, height: 'calc(100vh - 80px)', backgroundColor: 'primary.dark' }} />
        </div>
        <div className='col-auto'>
          {selectUserId !== '' && 
            <>
              <div
                ref={messageContainerRef}
                style={{ height: 'calc(100vh - 280px)', display: 'flex', flexDirection: 'column', maxHeight: 'calc(100vh - 80px)', overflowY: 'scroll', overflowX: 'hidden' }}
              >
                {messageList.map((message, index) => {
                  if (message.sender_id === myId) {
                    if (message.chat_image != null) {
                      return (
                        <div key={index}>
                          <MessagePhotoUserSend key={index} messageId={message.chat_id} getMessageFromServer={getMessageFromServer} setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage} messageSender={message.sender_name} messageContent={message.chat_image} messagePhoto={message.sender_photo}></MessagePhotoUserSend>
                        </div>
                      );
                    } else {
                      return (
                        <div key={index}>
                          <MessageUserSend key={index} messageId={message.chat_id} getMessageFromServer={getMessageFromServer} setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage} messageSender={message.sender_name} messageContent={message.chat_content} messagePhoto={message.sender_photo}></MessageUserSend>
                        </div>
                      );
                    }
                  } else {
                    if (message.chat_image != null) {
                      return <MessagePhotoFriendSend key={index} messageSender={message.sender_name} messageContent={message.chat_image} messagePhoto={message.sender_photo}></MessagePhotoFriendSend>
                    } else {
                      return <MessageFriendSend key={index} messageSender={message.sender_name} messageContent={message.chat_content} messagePhoto={message.sender_photo}></MessageFriendSend>
                    }
                  }
                })}
              </div>
              <InputGroup className="mb-3" style={{ height: '200px', width: 'calc(100vw - 260px)' }}>
                <Form.Control
                  as="textarea"
                  placeholder="Enter Your Message"
                  aria-label="Recipient's username"
                  aria-describedby="basic-addon2"
                  value={messageEnter}
                  onChange={(event) => setMessageEnter(event.target.value)}
                />
                <MuiButton size="small" variant="outlined" component="label">
                  choose photo
                  <input type="file" onChange={(event) => sendPhoto(event)} hidden/>
                </MuiButton>
                <Button variant="outline-secondary" id="button-addon2" onClick={handleSendMessage}>
                  Send
                </Button>
              </InputGroup>
            </>
          }
          {selectUserId === '' && 
            <></>
          }
        </div>
      </div>
    </>
  );
}

export default Message;
