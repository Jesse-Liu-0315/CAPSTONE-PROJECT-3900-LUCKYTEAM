import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import makeRequest from "../helpers/Fetch";
import ErrorBar from "./ErrorBar";

const Verification = (props) => {
  const [errorOpen, setErrorOpen] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [minutes, setMinutes] = React.useState(0);
  const [seconds, setSeconds] = React.useState(0);
  const [resendStatus, setResendStatus] = React.useState(false);

  React.useEffect(() => {
    const interval = setInterval(() => {
      if (seconds > 0) {
        setSeconds(seconds - 1);
      }

      if (seconds === 0) {
        if (minutes === 0) {
          clearInterval(interval);
        } else {
          setSeconds(59);
          setMinutes(minutes - 1);
        }
      }
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  });

  const sendCodeButton = async () => {
    try {
      const response = await makeRequest(`/auth/verify?email=${props.email}`, 'GET');
      props.setCorrectVerification(response.reset_code);
      setSeconds(15);
      setResendStatus(true);
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }

  const resendCodeButton = async () => {
    try {
      const response = await makeRequest(`/auth/verify?email=${props.email}`, 'GET');
      props.setCorrectVerification(response.reset_code);
      setSeconds(15);
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
      <div className="row">
        <div className='col-8'>
          <TextField sx={{ width: '100%', marginTop: '12px' }} name="outlined-basic" label="Verification Code"
                    variant="outlined"
                    onChange={(event) => props.setVerification(event.target.value)} />
        </div>
        {!resendStatus &&
          <div className='col'>
            <Button sx={{ marginTop: '12px' }} size='small' variant="outlined" onClick={sendCodeButton}>Send Code</Button>  
          </div>
        }
        {resendStatus &&
          <>
            {seconds > 0 && 
              <div className='col'>
                <Button sx={{ marginTop: '12px', width: '95px', height: '51px' }} size='small' variant="outlined" disabled={true}>{seconds}</Button>  
              </div>
            }
            {seconds === 0 && 
              <div className='col'>
                <Button sx={{ marginTop: '12px' }} size='small' variant="outlined" onClick={resendCodeButton}>Resend Code</Button>  
              </div>
            }
          </>
        }
      </div>
    </>
  );
}

Verification.propTypes = {
  email: PropTypes.string,
  setVerification: PropTypes.func,
  setCorrectVerification: PropTypes.func,
}

export default Verification;
