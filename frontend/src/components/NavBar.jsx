import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import makeRequest from "../helpers/Fetch";
import ErrorBar from "./ErrorBar";
import LoginModal from './LoginModal';

const NavBar = () => {
  const [errorOpen, setErrorOpen] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [loginModalOpen, setLoginModalOpen] = React.useState(false);
  const [loginStatus, setLoginStatus] = React.useState(false);

  React.useEffect(() => {
    setLoginStatus(localStorage.getItem('luckyToken') === null ? false : true);
  }, []);

  const handleLoginModalOpen = () => setLoginModalOpen(true);

  const jumpToHome = () => {
    window.location = '/';
  }

  const jumpToProfile = () => {
    window.location = '/profile';
  }

  const jumpToWishList = () => {
    window.location = '/wishlist';
  }

  const jumpToWatchedList = () => {
    window.location = '/watchedlist';
  }

  const jumpToBlackList = () => {
    window.location = '/blacklist';
  }

  const jumpToMessage = () => {
    window.location = '/message';
  }

  const LogoutButton = async () => {
    const body = {
      token: localStorage.luckyToken,
    }
    try {
      await makeRequest('/auth/logout', 'POST', body);
      localStorage.removeItem('luckyToken');
      localStorage.removeItem('luckyId');
      localStorage.removeItem('luckyEmail');
      setLoginModalOpen(false);
      setLoginStatus(false);
      if (window.location.href === 'http://localhost:3000/profile' || 
          window.location.href === 'http://localhost:3000/wishlist' ||
          window.location.href === 'http://localhost:3000/watchedlist' ||
          window.location.href === 'http://localhost:3000/blacklist' ||
          window.location.href === 'http://localhost:3000/message'
        ) {
        jumpToHome();
      } else {
        window.location.reload();
      }
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }

  return (
    <>
      {errorOpen &&
        <ErrorBar errorMessage={errorMessage} errorOpen={errorOpen} setErrorOpen={setErrorOpen}></ErrorBar>
      }
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <IconButton
              size="small"
              edge="start"
              color="inherit"
              aria-label="menu"
              sx={{ mr: 2 }}
              onClick={jumpToHome}
            >
              LuckyMovie
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}></Typography>
            {!loginStatus &&
              <>
                <Button color="inherit" onClick={handleLoginModalOpen}>LOGIN/SIGNUP</Button>
                <LoginModal loginModalOpen={loginModalOpen} setLoginModalOpen={setLoginModalOpen} 
                  setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage}></LoginModal>
              </>
            }
            {loginStatus &&
              <>
                <Button color="inherit" onClick={jumpToProfile}>Profile</Button>
                <Button color="inherit" onClick={jumpToWishList}>Wishlist</Button>
                <Button color="inherit" onClick={jumpToWatchedList}>Watched</Button>
                <Button color="inherit" onClick={jumpToBlackList}>Blacklist</Button>
                <Button color="inherit" onClick={jumpToMessage}>Message</Button>
                <Button color="inherit" onClick={LogoutButton}>Logout</Button>
              </>
            }
          </Toolbar>
        </AppBar>
      </Box>
    </>
  );
}

export default NavBar;
