import React from 'react';
import makeRequest from '../helpers/Fetch';
import ErrorBar from '../components/ErrorBar';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import NewUpcomingMovies from '../components/NewUpcomingMovies';
import Box from '@mui/material/Box';
import TopRatedMovies from '../components/TopRatedMovies';
import MostReviewedMovies from '../components/MostReviewedMovies';
import SuccessBar from '../components/SuccessBar';

const Home = () => {
  const [errorOpen, setErrorOpen] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [searchContent, setSearchContent] = React.useState('');
  const [topRated, setTopRated] = React.useState([]);
  const [mostReviewed, setMostReviewed] = React.useState([]);
  const [mostRecent, setMostRecent] = React.useState([]);
  const [hasNewMessage, setHasNewMessage] = React.useState('');
  const [successOpen, setSuccessOpen] = React.useState(false);
  const [successMessage, setSuccessMessage] = React.useState('');

  React.useEffect(() => {
    if (localStorage.getItem('luckyToken') != null) {
      const intervalId = setInterval(async () => {
        const body = {
          token: localStorage.getItem('luckyToken')
        };
        console.log(body.token);
        const response = await makeRequest(`/message/unread?token=${body.token}`, 'GET');
        console.log(response.unread_messages);
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
    try {
      makeRequest('/index', 'GET').then(data => {
        setTopRated(data.TopRated);
        setMostReviewed(data.MostReviewed);
        setMostRecent(data.MostRecent);
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }, []);

  const searchButton = () => {
    const isAllSpaces = searchContent.trim().length === 0;
    if (isAllSpaces) {
      return;
    }
    window.location = `/search/movie/${searchContent}`;
  }


  return (
    <>
      {errorOpen &&
        <ErrorBar errorMessage={errorMessage} errorOpen={errorOpen} setErrorOpen={setErrorOpen}></ErrorBar>
      }
      {successOpen &&
        <SuccessBar successMessage={successMessage} successOpen={successOpen} setSuccessOpen={setSuccessOpen}></SuccessBar>
      }
      <div className="container-fluid">
        <div style={{ textAlign: 'center', marginBottom: '130px'}}>
          <h1 style={{ marginTop: '150px', marginBottom: '20px', color: '#1565c0', cursor: 'default' }}>LuckyMovie</h1>
          <TextField sx={{ width: '600px', marginRight: '5px' }} id="outlined-search" size='small' 
            type="search" placeholder='Search' onChange={(event) => setSearchContent(event.target.value)}/>
          <Button variant="contained" onClick={searchButton}>Search</Button>
        </div>
        <div>
          <Box sx={{ marginRight: '5px', float: 'left', width: 5, height: 30, backgroundColor: 'primary.dark' }} />
          <h4 style={{ color: '#1565c0', cursor: 'default' }}>New & Upcoming Movies</h4>
          <div className='row' style={{margin: '0px', marginBottom:'70px', display: 'flex', justifyContent: 'space-around'}}>
            {mostRecent.map((movie, index) => {
              return <NewUpcomingMovies key={index} moviePicture={movie.movie_cover} movieName={movie.movie_name} movieId={movie.movie_id}></NewUpcomingMovies>
            })}
          </div>
        </div>
        <div className="row" >
          <div className="col" style={{width: '50%' }}>
            <div className="col">
              <Box sx={{ marginRight: '5px', float: 'left', width: 5, height: 30, backgroundColor: 'primary.dark' }} />
              <h4 style={{ color: '#1565c0', cursor: 'default' }}>Top Rated Movies</h4>
            </div>
            {topRated.map((movie, index) => {
              return <TopRatedMovies key={index} movieId={movie.movie_id} moviePicture={movie.movie_cover} movieName= {movie.movie_name} movieDescription={movie.movie_description} movieRating={movie.movie_rating}></TopRatedMovies>
            })}
          </div>
          <div className="col" style={{width: '50%' }}>
            <div className="col">
              <Box sx={{ marginRight: '5px', float: 'left', width: 5, height: 30, backgroundColor: 'primary.dark' }} />
              <h4 style={{ color: '#1565c0', cursor: 'default' }}>Most Reviewed Movies</h4>
            </div>
            {mostReviewed.map((movie, index) => {
              return <MostReviewedMovies key={index} movieId={movie.movie_id} moviePicture={movie.movie_cover} movieName= {movie.movie_name} movieDescription={movie.movie_description} movieReview={movie.numOfReviews}></MostReviewedMovies>
            })}
          </div>
        </div>
      </div>
    </>
  );
}
 
export default Home;
