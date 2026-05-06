import React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import PropTypes from 'prop-types';
import TextField from '@mui/material/TextField';
import ReactStars from 'react-rating-stars-component';
import makeRequest from '../helpers/Fetch';
import Typography from '@mui/material/Typography';

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

const RateModal = (props) => {
  const [score, setScore] = React.useState(0);
  const [comment, setComment] = React.useState('');

  const handleClose = () => props.setRateModalOpen(false);

  const ratingChanged = (newRating) => {
    setScore(newRating);
  };

  React.useEffect(() => {
    setScore(0);
    setComment('');
  }, [props.rateModalOpen]);

  const handleSubmitButton = async () => {
    const currentDate = new Date();
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
    const dateString = currentDate.toLocaleString('en-US', options).replace(/(\d+)\/(\d+)\/(\d+)/, '$3-$1-$2').replace(',', '');
    const body = {
      movie_id: parseInt(props.movieId),
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
      content: comment,
      rating: score,
      time: dateString,
    }
    try {
      await makeRequest('/review/add', 'POST', body);
      props.setRateModalOpen(false);
      window.location.reload();
    } catch (error) {
      props.setErrorOpen(true);
      props.setErrorMessage(error);
    }
  }

  return (
    <>
      <Modal
        open={props.rateModalOpen}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={boxStyle}>
          <Typography name="modal-modal-title" variant="h6" component="h2">
            Rate and Review
          </Typography>
          <ReactStars
            count={5}
            onChange={ratingChanged}
            size={24}
            activeColor="#ffd700"
          />
          <TextField sx={{ width: '100%', marginTop: '10px' }} multiline label="Add a review" variant="outlined" onChange={(event) => setComment(event.target.value)} />
          <div style={{ textAlign: 'end', marginTop: '10px' }}>
            <Button size='small' variant="outlined" sx={{ marginRight: '5px' }} onClick={handleClose}>Close</Button>
            <Button size='small' variant="outlined" onClick={handleSubmitButton}>Submit</Button>
          </div>
        </Box>
      </Modal>
    </>
  );
}

RateModal.propTypes = {
  setRateModalOpen: PropTypes.func,
  rateModalOpen: PropTypes.bool,
  movieId: PropTypes.string,
  setErrorOpen: PropTypes.func,
  setErrorMessage: PropTypes.func,
}

export default RateModal;
