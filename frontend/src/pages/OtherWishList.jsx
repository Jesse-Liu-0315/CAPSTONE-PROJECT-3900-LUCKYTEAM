import React from 'react';
import ErrorBar from '../components/ErrorBar';
import SuccessBar from '../components/SuccessBar';
import Box from '@mui/material/Box';
import OtherPeopleWishListMovie from '../components/OtherPeopleWishListMovie';
import makeRequest from '../helpers/Fetch';
import { useParams } from 'react-router-dom';
import Button from '@mui/material/Button';

const OtherWishList = () => {
  const userID = useParams().userId.toString();
  const userName = useParams().userName.toString();
  const [errorOpen, setErrorOpen] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [successOpen, setSuccessOpen] = React.useState(false);
  const [successMessage, setSuccessMessage] = React.useState('');
  const [wishResult, setWishResult] = React.useState([]);
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
      user_id: parseInt(userID)
    }
    try {
      makeRequest(`/wishlist/other?user_id=${body.user_id}`, 'GET').then(data => {
        setWishResult(data.wishlist);
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }, []);

  const jumpBackProfile = () => {
    window.location = `/otherprofile/${userID}`;
  }
  
  return (
    <>
      {errorOpen &&
        <ErrorBar errorMessage={errorMessage} errorOpen={errorOpen} setErrorOpen={setErrorOpen}></ErrorBar>
      }
      {successOpen &&
        <SuccessBar successMessage={successMessage} successOpen={successOpen} setSuccessOpen={setSuccessOpen}></SuccessBar>
      }
      <div className='row'>
        <div className='col'>
            <Box sx={{ margin: '8px', float: 'left', width: 5, height: 35, backgroundColor: 'primary.dark' }} />
            <h1 style={{ color: '#1565c0' }}>Wish list of {userName}</h1>
        </div>
        <div className='col'>
            <Button size='big' variant="outlined" onClick={jumpBackProfile} style={{ height: '40px', width: '200px', float:'right', color: 'white', backgroundColor:"#1565c0", marginTop: '10px', marginRight: '15px'}}>Back to {userName} profile</Button>
        </div>
      </div>
      {wishResult.map((result, index) => {
        return <OtherPeopleWishListMovie key={index} 
                movieId={result.movie_id} moviePicture={result.movie_cover} movieName={result.movie_name} movieDescription={result.movie_description} movieRating={result.movie_rating} movieReview={result.review_num}></OtherPeopleWishListMovie>
      })}
    </>
  );
}
 
export default OtherWishList;
