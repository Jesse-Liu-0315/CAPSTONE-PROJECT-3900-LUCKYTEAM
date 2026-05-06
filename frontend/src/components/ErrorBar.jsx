import React from 'react';
import PropTypes from 'prop-types';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

// To render alert component
const Alert = React.forwardRef(function Alert (props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

// Error tips bar
const ErrorBar = (props) => {
  // Close the error bar
  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    props.setErrorOpen(false);
  };

  return (
    <div>
      <Snackbar open={props.errorOpen} autoHideDuration={2000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
          {props.errorMessage}
        </Alert>
      </Snackbar>
    </div>
  );
}

ErrorBar.propTypes = {
  errorMessage: PropTypes.string,
  errorOpen: PropTypes.bool,
  setErrorOpen: PropTypes.func
}

export default ErrorBar;
