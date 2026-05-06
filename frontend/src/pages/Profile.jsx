import React from 'react';
import ErrorBar from '../components/ErrorBar';
import SuccessBar from '../components/SuccessBar';
import Box from '@mui/material/Box';
import defaultPhoto from '../user_profile_default.png';
import Button from '@mui/material/Button';
import fileToDataUrl from '../helpers/fileToDataUrl';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import TextField from '@mui/material/TextField';
import makeRequest from "../helpers/Fetch";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Verification from '../components/Verification';
import Chip from '@mui/material/Chip';

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

const Profile = () => {
  const [errorOpen, setErrorOpen] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [successOpen, setSuccessOpen] = React.useState(false);
  const [successMessage, setSuccessMessage] = React.useState('');
  const [photo, setPhoto] = React.useState(defaultPhoto);
  const [passwordModalOpen, setPasswordModalOpen] = React.useState(false);
  const [password, setPassword] = React.useState('');
  const [reEnterPassword, setReEnterPassword] = React.useState('');
  const [firstName, setFirstName] = React.useState('');
  const [lastName, setLastName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [age, setAge] = React.useState('');
  const [sex, setSex] = React.useState('Undefined');
  const [occupation, setOccupation] = React.useState('');
  const [area, setArea] = React.useState('');
  const [description, setDescription] = React.useState('');
  const [verification, setVerification] = React.useState('');
  const [correctVerification, setCorrectVerification] = React.useState('');
  const [views, setViews] = React.useState(0);
  const [tag, setTag] = React.useState('');
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
      token: localStorage.luckyToken,
    }
    try {
      makeRequest(`/user_pofile/?token=${body.token}`, 'GET').then(data => {
        setFirstName(data.name_first === null ? '' : data.name_first);
        setLastName(data.name_last === null ? '' : data.name_last);
        setEmail(data.email === null ? '' : data.email);
        setAge(data.user_age === null ? '' : data.user_age);
        setSex(data.user_sex);
        setOccupation(data.user_occupation === null ? '' : data.user_occupation);
        setArea(data.user_area === null ? '' : data.user_area);
        setDescription(data.user_description === null ? '' : data.user_description);
        setPhoto(data.user_profile_photo === null ? defaultPhoto : data.user_profile_photo);
        setViews(data.user_views);
        setTag(data.user_tag === null ? '' : data.user_tag);
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }, []);

  const handlePasswordModalOpen = () => setPasswordModalOpen(true);
  const handlePasswordModalClose = () => setPasswordModalOpen(false);

  const handleAgeChange = (event) => {
    if (isNaN(event.target.value) || event.target.value.at(0) === '0') {
      event.target.value = '';
    } else {
      setAge(event.target.value);
    }
  }

  const showNewPhoto = (event) => {
    fileToDataUrl(event.target.files[0]).then(imgUrl => {
      setPhoto(imgUrl);
    })
  };

  const setNewPasswordButton = async () => {
    if (password !== reEnterPassword) {
      setErrorOpen(true);
      setErrorMessage('Please make sure enter the same password');
      return;
    }
    if (verification !== correctVerification) {
      setErrorOpen(true);
      setErrorMessage('Please enter the correct verification code');
      return;
    }
    const body = {
      email: localStorage.luckyEmail,
      password: password,
    }
    try {
      await makeRequest('/auth/resetpassword', 'POST', body);
      setSuccessOpen(true);
      setSuccessMessage('Set your new password success');
      setPasswordModalOpen(false);
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  };

  const submitButton = async () => {
    const body = {
      token: localStorage.luckyToken,
      name_first: firstName,
      name_last: lastName,
      email: email,
      user_age: age === '' ? 0 : parseInt(age),
      user_sex: sex,
      user_occupation: occupation,
      user_area: area,
      user_description: description,
      user_profile_photo: photo,
    }
    try {
      await makeRequest('/user_pofile/submit', 'POST', body);
      setSuccessOpen(true);
      setSuccessMessage('Update your profile success');
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  };

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
        <h1 style={{ color: '#1565c0' }}>Profile</h1>
      </div>
      <div className='container text-center' style={{ width: "100%" }}>
        <div className='row justify-content-md-center' style={{ marginBottom: '15px' }}>
          <div className="col"></div>
          <div className="col">
            <div> 
              <img src={photo} alt="User" style={{ height: '150px', width: '150px' }} />
            </div>
          </div>
          <div className="col" style={{ textAlign: 'center' }}>
            <Button size='small' variant="outlined" onClick={handlePasswordModalOpen} style={{ width: '200px', height: '30px' }}>Set the new Password</Button>
            <div className='row' style={{ color: 'grey', height: '18px', width: '100%', textAlign: 'center', marginBottom: '5px' }}>
              <div style={{ padding: '0px'}}>
                {views} Views
              </div>
            </div>
            {tag !== '' && 
              <div className='row' style={{ color: 'grey', height: '18px', width: '100%', textAlign: 'center' }}>
                <div style={{ padding: '0px'}}>
                    <Chip label={tag} variant="outlined" style={{ height: '24px' }} />
                </div>
              </div>
            }
            <Modal
              open={passwordModalOpen}
              onClose={handlePasswordModalClose}
              aria-labelledby="modal-modal-title"
              aria-describedby="modal-modal-description"
            >
              <Box sx={boxStyle}>
                <Typography id="modal-modal-title" variant="h6" component="h2">
                    Set the new password
                  </Typography>
                  <TextField sx={{ width: '100%', marginTop: '12px' }} label="Password"
                    variant="outlined" type='password'
                    onChange={(event) => setPassword(event.target.value)} />
                  <TextField sx={{ width: '100%', marginTop: '12px' }} label="Re-enter Password"
                    variant="outlined" type='password'
                    onChange={(event) => setReEnterPassword(event.target.value)} />
                  <Verification email={email} setVerification={setVerification} setCorrectVerification={setCorrectVerification}></Verification>
                  <div style={{ textAlign: 'end', marginTop: '10px' }}>
                    <Button size='small' variant="outlined" sx={{ marginRight: '5px' }}
                      onClick={handlePasswordModalClose}>Close</Button>
                    <Button size='small' variant="outlined" onClick={setNewPasswordButton}>Set the new Password</Button>
                  </div>
              </Box>
            </Modal>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <div className="d-flex justify-content-center">
              <Button size="small" variant="outlined" component="label">
                Upload Photo
                <input type="file" onChange={(event) => showNewPhoto(event)} hidden/>
              </Button>
            </div>         
          </div>
        </div>
        <br/>
        <div className="row">
          <div className="col">
            <div className="mb-3">
              <TextField size='small' label="First Name" value={firstName} variant="outlined" onChange={(event) => setFirstName(event.target.value)} />
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <div className="mb-3">
              <TextField size='small' label="Last Name" value={lastName} variant="outlined" onChange={(event) => setLastName(event.target.value)} />
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <div className="mb-3">
              <TextField size='small' label="Email" value={email} variant="outlined" onChange={(event) => setEmail(event.target.value)} />
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <div className="mb-3">
              <TextField size='small' label="Age" value={age} variant="outlined" onChange={handleAgeChange} />
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <div className="mb-3">
              <FormControl sx={{ width: '222px', height: '40px' }}>
                <InputLabel id="sexSelect">Sex</InputLabel>
                <Select
                  size='small'
                  labelId="sexSelect"
                  value={sex}
                  label="Sex"
                  onChange={(event) => setSex(event.target.value)}
                >
                  <MenuItem value={'Undefined'}>Undefined</MenuItem>
                  <MenuItem value={'Male'}>Male</MenuItem>
                  <MenuItem value={'Female'}>Female</MenuItem>
                </Select>
              </FormControl>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <div className="mb-3">
              <TextField size='small' label="Occupation" value={occupation} variant="outlined" onChange={(event) => setOccupation(event.target.value)} />
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <div className="mb-3">
              <TextField size='small' label="Area" value={area} variant="outlined" onChange={(event) => setArea(event.target.value)} />
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <div className="mb-3">
              <TextField multiline sx={{ width: '223px' }}  label="Description" value={description} variant="outlined" onChange={(event) => setDescription(event.target.value)} />
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <Button size='small' variant="outlined" onClick={submitButton}>Submit</Button>
          </div>
        </div>
      </div>
    </>
  );
}

export default Profile;
