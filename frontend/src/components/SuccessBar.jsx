import React from 'react';
import PropTypes from 'prop-types';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

// To render alert component
const Alert = React.forwardRef(function Alert (props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

// Success tips bar
const SuccessBar = (props) => {
  // Close the success bar
  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    props.setSuccessOpen(false);
  };

  return (
    <div>
      <Snackbar open={props.successOpen} autoHideDuration={2000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
          {props.successMessage}
        </Alert>
      </Snackbar>
    </div>
  );
}

SuccessBar.propTypes = {
  successMessage: PropTypes.string,
  successOpen: PropTypes.bool,
  setSuccessOpen: PropTypes.func
}

export default SuccessBar;
