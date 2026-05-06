import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import TextField from '@mui/material/TextField';
import makeRequest from "../helpers/Fetch";
import Verification from './Verification';
import PropTypes from 'prop-types';

const boxStyle = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '1px solid #000',
  boxShadow: 24,
  p: 4,
};

const LoginModal = (props) => {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [reEnterPassword, setReEnterPassword] = React.useState('');
  const [login, setLogin] = React.useState(true);
  const [register, setRegister] = React.useState(false);
  const [forgotPassword, setForgotPassword] = React.useState(false);
  const [verification, setVerification] = React.useState('');
  const [correctVerification, setCorrectVerification] = React.useState('');

  const handleLoginModalClose = () => {
    props.setLoginModalOpen(false);
    setLogin(true);
    setRegister(false);
    setForgotPassword(false);
  }

  const ForgotPasswordButton = () => {
    setLogin(false);
    setRegister(false);
    setForgotPassword(true);
  }

  const GoBackToLoginButton = () => {
    setLogin(true);
    setRegister(false);
    setForgotPassword(false);
  }

  const RegisterButton = () => {
    setLogin(false);
    setRegister(true);
    setForgotPassword(false);
  }

  const LoginButton = async () => {
    if (email.indexOf('@') === -1 || email.indexOf('.') === -1) {
      props.setErrorOpen(true);
      props.setErrorMessage('Invalid email');
      return;
    }
    if (password.length < 6) {
      props.setErrorOpen(true);
      props.setErrorMessage('Invalid password');
      return;
    }
    const body = {
      email: email,
      password: password,
    }
    try {
      const response = await makeRequest('/auth/login', 'POST', body);
      localStorage.setItem('luckyToken', response.token);
      // localStorage.luckyToken = response.token;
      localStorage.luckyId = parseInt(response.auth_user_id);
      localStorage.luckyEmail = email;
      setLogin(true);
      setForgotPassword(false);
      setRegister(false);
      props.setLoginModalOpen(false);
      window.location.reload();
    } catch (error) {
      props.setErrorOpen(true);
      props.setErrorMessage(error);
    }
  }

  const SetNewPasswordButton = async () => {
    if (email.indexOf('@') === -1 || email.indexOf('.') === -1) {
      props.setErrorOpen(true);
      props.setErrorMessage('Invalid email');
      return;
    }
    if (password.length < 6) {
      props.setErrorOpen(true);
      props.setErrorMessage('Invalid password');
      return;
    }
    if (password !== reEnterPassword) {
      props.setErrorOpen(true);
      props.setErrorMessage('Please make sure enter the same password');
      return;
    }
    if (verification !== correctVerification) {
      props.setErrorOpen(true);
      props.setErrorMessage('Please enter the correct verification code');
      return;
    }
    const body = {
      email: email,
      password: password,
    }
    try {
      await makeRequest('/auth/resetpassword', 'POST', body);
      setLogin(true);
      setForgotPassword(false);
      setRegister(false);
    } catch (error) {
      props.setErrorOpen(true);
      props.setErrorMessage(error);
    }
  }

  const SignUpButton = async () => {
    if (email.indexOf('@') === -1 || email.indexOf('.') === -1) {
      props.setErrorOpen(true);
      props.setErrorMessage('Invalid email');
      return;
    }
    if (password.length < 6) {
      props.setErrorOpen(true);
      props.setErrorMessage('Invalid password');
      return;
    }
    if (password !== reEnterPassword) {
      props.setErrorOpen(true);
      props.setErrorMessage('Please make sure enter the same password');
      return;
    }
    if (verification !== correctVerification) {
      props.setErrorOpen(true);
      props.setErrorMessage('Please enter the correct verification code');
      return;
    }
    const body = {
      email: email,
      password: password,
    }
    try {
      const response = await makeRequest('/auth/register', 'POST', body);
      localStorage.setItem('luckyToken', response.token);
      // localStorage.luckyToken = response.token;
      localStorage.luckyId = parseInt(response.auth_user_id);
      localStorage.luckyEmail = email;
      setLogin(true);
      setRegister(false);
      setForgotPassword(false);
      props.setLoginModalOpen(false);
      window.location.reload();
    } catch (error) {
      props.setErrorOpen(true);
      props.setErrorMessage(error);
    }
  }

  return (
    <>
      <Modal
        open={props.loginModalOpen}
        onClose={handleLoginModalClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={boxStyle}>
          {login &&
            <>
              <Typography name="modal-modal-title" variant="h6" component="h2">
                Login
              </Typography>
              <TextField sx={{ width: '100%', marginTop: '12px' }} name="outlined-basic" label="Email"
                          variant="outlined"
                          onChange={(event) => setEmail(event.target.value)} />
              <TextField sx={{ width: '100%', marginTop: '12px' }} name="outlined-basic" label="Password"
                          variant="outlined" type='password'
                          onChange={(event) => setPassword(event.target.value)} />
              <Button sx={{ marginTop: '12px' }} size='small' variant="outlined" onClick={ForgotPasswordButton}>Forgot the Password</Button>
              <br/>
              <Button sx={{ marginTop: '12px' }} size='small' variant="outlined" onClick={RegisterButton}>Register</Button>
              <div style={{ textAlign: 'end', marginTop: '10px' }}>
                <Button size='small' variant="outlined" sx={{ marginRight: '5px' }} onClick={handleLoginModalClose}>Close</Button>
                <Button size='small' variant="outlined" onClick={LoginButton}>Login</Button>
              </div>
            </>
          }
          {forgotPassword &&
          <>
            <Typography name="modal-modal-title_2" variant="h6" component="h2">
              Set the new password
            </Typography>
            <TextField sx={{ width: '100%', marginTop: '12px' }} name="outlined-basic" label="Email"
                        variant="outlined"
                        onChange={(event) => setEmail(event.target.value)} />
            <TextField sx={{ width: '100%', marginTop: '12px' }} name="outlined-basic" label="New Password"
                        variant="outlined" type='password'
                        onChange={(event) => setPassword(event.target.value)} />
            <TextField sx={{ width: '100%', marginTop: '12px' }} name="outlined-basic" label="Re-enter New Password"
                        variant="outlined" type='password'
                        onChange={(event) => setReEnterPassword(event.target.value)} />
            <Verification email={email} setVerification={setVerification} setCorrectVerification={setCorrectVerification}></Verification>
            <Button sx={{ marginTop: '12px' }} size='small' variant="outlined" onClick={GoBackToLoginButton}>Go back to login</Button>
            <div style={{ textAlign: 'end', marginTop: '10px' }}>
              <Button size='small' variant="outlined" sx={{ marginRight: '5px' }}
                      onClick={handleLoginModalClose}>Close</Button>
              <Button size='small' variant="outlined" onClick={SetNewPasswordButton}>Set the new Password</Button>
            </div>
          </>
        }
        {register &&
          <>
            <Typography name="modal-modal-title" variant="h6" component="h2">
              Sign Up
            </Typography>
            <TextField sx={{ width: '100%', marginTop: '12px' }} name="outlined-basic" label="Email"
                        variant="outlined"
                        onChange={(event) => setEmail(event.target.value)} />
            <TextField sx={{ width: '100%', marginTop: '12px' }} name="outlined-basic" label="Password"
                        variant="outlined" type='password'
                        onChange={(event) => setPassword(event.target.value)} />
            <TextField sx={{ width: '100%', marginTop: '12px' }} name="outlined-basic" label="Re-enter Password"
                        variant="outlined" type='password'
                        onChange={(event) => setReEnterPassword(event.target.value)} />
            <Verification email={email} setVerification={setVerification} setCorrectVerification={setCorrectVerification}></Verification>
            <Button sx={{ marginTop: '12px' }} size='small' variant="outlined" onClick={GoBackToLoginButton}>Go back to login</Button>
            <div style={{ textAlign: 'end', marginTop: '10px' }}>
              <Button size='small' variant="outlined" sx={{ marginRight: '5px' }}
                      onClick={handleLoginModalClose}>Close</Button>
              <Button size='small' variant="outlined" onClick={SignUpButton}>Sign Up</Button>
            </div>
          </>
        }
        </Box>
      </Modal>
    </>
  );
}

LoginModal.propTypes = {
  loginModalOpen: PropTypes.bool,
  setLoginModalOpen: PropTypes.func,
  setErrorOpen: PropTypes.func,
  setErrorMessage: PropTypes.func,
}
 
export default LoginModal;
