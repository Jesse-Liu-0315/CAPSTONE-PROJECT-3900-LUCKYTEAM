import React from 'react';
import ErrorBar from '../components/ErrorBar';
import { useParams } from 'react-router-dom';
import makeRequest from '../helpers/Fetch';
import Box from '@mui/material/Box';
import "react-multi-carousel/lib/styles.css";
import LoginModal from '../components/LoginModal';
import Filmography from '../components/Filmography';
import { Button } from '@mui/material';
import SuccessBar from '../components/SuccessBar';
import ShareModal from '../components/ShareModal';

const CastDetail = () => {
  const castName = useParams().castName.toString();
  const castNameWithSpace = castName.replaceAll('_', ' ');
  const castId = useParams().castId.toString();
  const [errorOpen, setErrorOpen] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [cover, setCover] = React.useState('');
  const [description, setDescription] = React.useState('');
  const [birth, setBirth] = React.useState('');
  const [nation, setNation] = React.useState('');
  const [movies, setMovies] = React.useState([]);
  const [views, setViews] = React.useState(0);
  const [loginModalOpen, setLoginModalOpen] = React.useState(false);
  const [moreStatus, setMoreStatus] = React.useState(false);
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
      castID: castId
    }
    try {
      makeRequest(`/cast?castID=${body.castID}`, 'GET').then(data => {
        setCover(data.cast['star_cover']);
        setDescription(data.cast['star_description']);
        setBirth(data.cast['star_birth']);
        setNation(data.cast['star_nationality']);
        setViews(data.cast['star_views']);
        setMovies(data.movie);
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }, []);

  const moreButton = () => {
    setMoreStatus(!moreStatus);
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
      <ShareModal location={'cast'} cover={cover} shareModalOpen={shareModalOpen} setShareModalOpen={setShareModalOpen} 
        setErrorOpen={setErrorOpen} setErrorMessage={setErrorMessage} setSuccessOpen={setSuccessOpen} setSuccessMessage={setSuccessMessage}
      ></ShareModal>
      <div className="container-fluid">
        <div>
          <Box sx={{ marginTop: '5px', marginRight: '5px', float: 'left', width: 5, height: 35, backgroundColor: 'primary.dark' }} />
          <h1 style={{ color: '#1565c0' }}>{castNameWithSpace}</h1>
        </div>
        <div className="row">
          <div className="card mb-3" style={{ maxWidth: '100vw', border: '0px' }}>
            <div className="row g-0">
              <div className="col-auto">
                <img src={cover} className="img-fluid" alt="Cast" style={{ height: '235px' }} />
              </div>
              <div className="col">
                <div className="card-body" style={{ position:'relative', height: '100%', padding: '0px', paddingLeft: '5px' }}>
                  {moreStatus && 
                    <p style={{ margin: '0px', marginBottom: '30px' }}><b>Description:</b> {description}</p>
                  }
                  {!moreStatus && 
                    <p style={{ margin: '0px' }}><b>Description:</b> {description.substring(0, 360)}</p>
                  }
                  {(description.length > 360 ? true : false) && 
                    <>
                    {moreStatus && 
                      <div style={{ textAlign: 'end' }}>
                        <Button onClick={moreButton}>Less</Button>
                      </div>
                    }
                    {!moreStatus &&
                      <div style={{ textAlign: 'end' }}>
                        <Button onClick={moreButton}>More</Button>
                      </div>
                    }
                    </>
                  }
                  <p className="card-text" style={{ margin: '0px', position: 'absolute', bottom: 40 }}><b>Birth:</b> {birth}</p>
                  <p className="card-text" style={{ margin: '0px', position: 'absolute', bottom: 20 }}><b>Nation:</b> {nation}</p>
                  <p className="card-text" style={{ margin: '0px', position: 'absolute', bottom: 0 }}><b>Views:</b> {views}</p>
                  <Button size='small' variant="outlined" onClick={handleShareModalOpen} style={{ margin: '0px', position: 'absolute', bottom: 0, left: 350 }}>Share this cast</Button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="col">
          <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 5, height: 20, backgroundColor: 'primary.dark' }} />
          <h5 style={{ color: '#1565c0' }}>Filmography</h5>
        </div>
        {movies.map((movie, index) => {
          return <Filmography key={index} movieId={movie.movie_id} moviePicture={movie.movie_cover} movieName= {movie.movie_name} movieDescription={movie.movie_description} movieRating={movie.movie_rating} movieReview={movie.numOfReviews}></Filmography>
        })}
      </div>
    </>
  );
}

export default CastDetail;
