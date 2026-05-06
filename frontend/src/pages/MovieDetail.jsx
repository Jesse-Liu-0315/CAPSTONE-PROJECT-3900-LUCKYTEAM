import React from 'react';
import ErrorBar from '../components/ErrorBar';
import { useParams } from 'react-router-dom';
import makeRequest from '../helpers/Fetch';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import "react-multi-carousel/lib/styles.css";
import RecentReview from '../components/RecentReview';
import MovieMayLike from '../components/MovieMayLike';
import MovieSimilar from '../components/MovieSimilar';
import Rating from '@mui/material/Rating';
import LoginModal from '../components/LoginModal';
import MovieDetailDirector from '../components/MovieDetailDirector';
import MovieDetailCast from '../components/MovieDetailCast';
import RateModal from '../components/RateModal';
import SuccessBar from '../components/SuccessBar';
import ShareModal from '../components/ShareModal';

const MovieDetail = () => {
  const movieName = useParams().movieName.toString();
  const movieNameWithSpace = movieName.replaceAll('_', ' ');
  const movieId = useParams().movieId.toString();
  const [errorOpen, setErrorOpen] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [cover, setCover] = React.useState('');
  const [releaseDate, setReleaseDate] = React.useState(0);
  const [genre, setGenre] = React.useState('');
  const [language, setLanguage] = React.useState('');
  const [views, setViews] = React.useState(0);
  const [added, setAdded] = React.useState(0);
  const [seen, setSeen] = React.useState(0);
  const [description, setDescription] = React.useState('');
  const [directors, setDirectors] = React.useState([]);
  const [casts, setCasts] = React.useState([]);
  const [reviews, setReviews] = React.useState([]);
  const [overallRatingNum, setOverallRatingNum] = React.useState(0);
  const [watchedStatus, setWatchedStatus] = React.useState(false);
  const [wishStatus, setWishStatus] = React.useState(false);
  const [loginModalOpen, setLoginModalOpen] = React.useState(false);
  const [rateModalOpen, setRateModalOpen] = React.useState(false);
  const [similarMovies, setSimilarMovies] = React.useState([]);
  const [youMayLikeMovies, setYouMayLikeMovies] = React.useState([]);
  const [shareModalOpen, setShareModalOpen] = React.useState(false);
  const [successOpen, setSuccessOpen] = React.useState(false);
  const [successMessage, setSuccessMessage] = React.useState('');
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
      name: movieNameWithSpace,
      movieID: movieId,
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    try {
      makeRequest(`/movie?movieID=${body.movieID}&token=${body.token}`, 'GET').then(data => {
        const movie_data = data.movie;
        setCover(movie_data.movie_cover);
        setReleaseDate(movie_data.movie_release_date);
        setGenre(movie_data.movie_tag);
        setLanguage(movie_data.movie_language);
        setViews(movie_data.movie_views);
        setAdded(data.numWish);
        setSeen(data.numWatched);
        setWatchedStatus(data.watched);
        setWishStatus(data.wish);
        setDescription(movie_data.movie_description);
        setDirectors(data.director);
        setCasts(data.star);
        setReviews(data.review);
        setOverallRatingNum(movie_data.movie_rating === null ? 0 : movie_data.movie_rating);
        setSimilarMovies(data.recommendation);
        setYouMayLikeMovies(data.movie_u_may_like);
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }, []);

  const addToWishListButton = async () => {
    if (localStorage.getItem('luckyToken') === null) {
      setLoginModalOpen(true);
      return;
    }
    const body = {
      movie_id: parseInt(movieId),
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    try {
      await makeRequest('/wishlist/add', 'POST', body);
      setWishStatus(true);
      setAdded(added + 1);
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }

  const removeFromWishListButton = async () => {
    const body = {
      movie_id: parseInt(movieId),
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    try {
      await makeRequest('/wishlist/remove', 'POST', body);
      setWishStatus(false);
      setAdded(added - 1);
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }

  const alreadySeenButton = async () => {
    if (localStorage.getItem('luckyToken') === null) {
      setLoginModalOpen(true);
      return;
    }
    const body = {
      movie_id: parseInt(movieId),
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    try {
      await makeRequest('/watchedlist/add', 'POST', body);
      setWatchedStatus(true);
      setSeen(seen + 1);
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }

  const notAlreadySeenButton = async () => {
    const body = {
      movie_id: parseInt(movieId),
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    try {
      await makeRequest('/watchedlist/remove', 'POST', body);
      setWatchedStatus(false);
      setSeen(seen - 1);
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }

  const rateAndReviewButton = () => {
    if (localStorage.getItem('luckyToken') === null) {
      setLoginModalOpen(true);
      return;
    }
    setRateModalOpen(true);
  }

  const handleShareModalOpen = () => {
    if (localStorage.getItem('luckyToken') === null) {
      setLoginModalOpen(true);
      return;
    }
    setShareModalOpen(true);
  }

  return (
    <>
      {errorOpen &&
        <ErrorBar errorMessage={errorMessage} errorOpen={errorOpen} setErrorOpen={setErrorOpen}></ErrorBar>
      }
      {successOpen &&
        <SuccessBar successMessage={successMessage} successOpen={successOpen} setSuccessOpen={setSuccessOpen}></SuccessBar>
      }
      <LoginModal loginModalOpen={loginModalOpen} setLoginModalOpen={setLoginModalOpen}
        setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage}></LoginModal>
      <RateModal rateModalOpen={rateModalOpen} setRateModalOpen={setRateModalOpen} movieId={movieId}
        setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage}
      ></RateModal>
      <ShareModal location={'movie'} cover={cover} shareModalOpen={shareModalOpen} setShareModalOpen={setShareModalOpen} 
        setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage} setSuccessOpen={setSuccessOpen} setSuccessMessage={setSuccessMessage}
      ></ShareModal>
      <div className="container-fluid">
        <div className="row">
          <div className="col-9">
            <div>
              <Box sx={{ marginTop: '5px', marginRight: '5px', float: 'left', width: 5, height: 35, backgroundColor: 'primary.dark' }} />
              <h1 style={{ color: '#1565c0' }}>{movieNameWithSpace}</h1>
            </div>
            <div className="card mb-3" style= {{ border: '0px' }}>
              <div className="row">
                <div className="col-auto" style={{ padding: '0px', marginLeft: '12px' }}>
                  <img src={cover} className="img-fluid" alt="Movie" 
                    style={{ width: '150px', height: '230px' }} 
                  />
                </div>
                <div className="col" style={{ padding: '0px', marginLeft: '5px' }}>
                  <div className="card-body" style={{ padding: '0px' }}>
                    <p className="card-text" style={{ margin: '0px' }}>Release date: {releaseDate}</p>
                    <p className="card-text" style={{ margin: '0px' }}>Genre: {genre}</p>
                    <p className="card-text" style={{ margin: '0px' }}>Language: {language}</p>
                    <p className="card-text" style={{ marginBottom: '10px' }}>Views: {views}</p>
                    <Button size='small' variant="outlined" onClick={handleShareModalOpen} style={{ marginBottom: '40px' }}>Share this movie</Button>
                    <div style={{ display:'flex', flexDirection: 'row' }}>
                      <div style={{ width: '195px', textAlign: 'center' }}>
                        {!wishStatus &&
                          <Button size='small' sx={{ width: '195px' }} variant="outlined" onClick={addToWishListButton}>Add to wishlist</Button>
                        }
                        {wishStatus &&
                          <Button size='small' sx={{ width: '195px' }} variant="outlined" onClick={removeFromWishListButton}>Remove from wishlist</Button>
                        }
                        <p style={{ fontSize: '13px', margin: '0px' }}>{added} added</p>
                      </div>
                      <div style={{ width: '195px', textAlign: 'center', marginLeft: '5px' }}>
                        {!watchedStatus && 
                          <Button size='small' sx={{ width: '195px' }} variant="outlined" onClick={alreadySeenButton}>Already seen</Button>
                        }
                        {watchedStatus && 
                          <Button size='small' sx={{ width: '195px' }} variant="outlined" onClick={notAlreadySeenButton}>Not already seen</Button>
                        }
                        <p style={{ fontSize: '13px', margin: '0px' }}>{seen} seen</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div>
              <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 5, height: 20, backgroundColor: 'primary.dark' }} />
              <h5 style={{ color: '#1565c0' }}>Description</h5>
            </div>
            <p>{description}</p>
            <div>
              <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 5, height: 20, backgroundColor: 'primary.dark' }} />
              <h5 style={ {color: '#1565c0' }}>Director</h5>
              <div className='row'>
                {directors.map((director, index) => {
                  return <MovieDetailDirector key={index} directorId={director.director_id} directorPicture={director.director_cover} directorName={director.director_name}></MovieDetailDirector>
                })}
              </div>
            </div>
            <br/>
            <div>
              <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 5, height: 20, backgroundColor: 'primary.dark' }} />
              <h5 style={{ color: '#1565c0' }}>Cast</h5>
              <div className='row'>
                {casts.map((cast, index) => {
                  return <MovieDetailCast key={index} castId={cast.star_id}  castPicture={cast.star_cover} castName={cast.star_name}></MovieDetailCast>
                })}
              </div>
            </div>
            <br/>
            <div className="row">
              <div className="col">
                <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 5, height: 20, backgroundColor: 'primary.dark' }} />
                <h5 style={{ color: '#1565c0' }}>Recent Reviews</h5>
              </div>  
              <div className="col">
                <Button size='small' variant="outlined" onClick={rateAndReviewButton}>Rate and Review</Button>
              </div> 
            </div>
            {reviews.map((review, index) => {
              return <RecentReview key={index} movieId={review.movie_id} reviewId={review.review_id} userId={review.user_id} userPhoto={review.user_profile_photo} userName={review.user_name} userTag={review.tag} 
                      reviewRating={review.rating_point} reviewComment={review.content} reviewDate={review.review_date}
                      reviewLike={review.review_like} reviewDisLike={review.review_dislike}
                      setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage}
                      deletePermission={review.permission}
                      overallRatingNum={overallRatingNum} setOverallRatingNum={setOverallRatingNum}
                      reviews={reviews} setReviews={setReviews}
                      ></RecentReview>
            })}
          </div>
          <div className="col-3">
            <Box sx={{ marginTop: '40px', float: 'left', width: 2, height: 200, backgroundColor: 'primary.dark' }} />
            <div className="d-flex flex-sm-column align-items-center bg-warning-subtle" style={{ marginTop: '30px' }}>
              <br/>
              <p>Lucky Average Rating</p>
              <h4>{overallRatingNum}</h4>
              <Rating value={overallRatingNum} precision={0.1} readOnly />
              <br/>
              <Button size='small' variant="outlined" onClick={rateAndReviewButton}>Rate and Review</Button>
              <br />
            </div>
            <br/>
            <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 2, height: 20, backgroundColor: 'primary.dark' }} />
            <h5 style={{ color: '#1565c0' }}>You may like these Movies...</h5>
            {youMayLikeMovies.map((movie, index) => {
              return <MovieMayLike key={index} movieId={movie.movie_id} moviePicture={movie.movie_cover} movieName= {movie.movie_name} movieRating={movie.movie_rating} movieReview={movie.numOfReviews}></MovieMayLike>
            })}
            <br/>
            <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 2, height: 20, backgroundColor: 'primary.dark' }} />
            <h5 style={{ color: '#1565c0' }}>Similar Movies...</h5>
            {similarMovies.map((movie, index) => {
              return <MovieSimilar key={index} movieId={movie.movie_id} moviePicture={movie.movie_cover} movieName= {movie.movie_name} movieRating={movie.movie_rating} movieReview={movie.numOfReviews}></MovieSimilar>
            })}
          </div>
        </div>
      </div>
    </>
  );
}

export default MovieDetail;
