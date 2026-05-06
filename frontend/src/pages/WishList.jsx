import React from 'react';
import ErrorBar from '../components/ErrorBar';
import SuccessBar from '../components/SuccessBar';
import Box from '@mui/material/Box';
import WishListMovie from '../components/WishListMovie';
import makeRequest from '../helpers/Fetch';

const WishList = () => {
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
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    try {
      makeRequest(`/wishlist?token=${body.token}`, 'GET').then(data => {
        setWishResult(data.wishlist);
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
        <h1 style={{ color: '#1565c0' }}>Your Wish List</h1>
      </div>
      {wishResult.map((result, index) => {
        return <WishListMovie key={index} 
                setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage} setSuccessOpen={setSuccessOpen} setSuccessMessage={setSuccessMessage}
                wishResult={wishResult} setWishResult={setWishResult} movieId={result.movie_id} moviePicture={result.movie_cover} movieName={result.movie_name} movieDescription={result.movie_description} movieRating={result.movie_rating} movieReview={result.review_num}></WishListMovie>
      })}
    </>
  );
}
 
export default WishList;
