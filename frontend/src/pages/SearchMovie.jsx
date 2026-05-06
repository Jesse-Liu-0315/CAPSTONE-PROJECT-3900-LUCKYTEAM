import React from 'react';
import ErrorBar from '../components/ErrorBar';
import { useParams } from 'react-router-dom';
import makeRequest from '../helpers/Fetch';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import SearchResultMovie from '../components/SearchResultMovie';
import Pagination from '@mui/material/Pagination';
import SuccessBar from '../components/SuccessBar';

const SearchMovie = () => {
  const searchContent = useParams().searchContent.toString();
  const [currentPage, setCurrentPage] = React.useState(1);
  const [errorOpen, setErrorOpen] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [sortSetting, setSortSetting] = React.useState('Relevance');
  const [searchResult, setSearchResult] = React.useState([]);
  const [totalPage, setTotalPage] = React.useState(1);
  const [hasNewMessage, setHasNewMessage] = React.useState('');
  const [successOpen, setSuccessOpen] = React.useState(false);
  const [successMessage, setSuccessMessage] = React.useState('');

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
      keyword: searchContent,
      page: parseInt(currentPage),
      sortBy: sortSetting
    }
    try {
      makeRequest('/search/movie', 'POST', body).then(data => {
        setSearchResult(data.movies);
        setTotalPage(data.numPages);
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }, []);

  React.useEffect(() => {
    const body = {
      keyword: searchContent,
      page: parseInt(currentPage),
      sortBy: sortSetting
    }
    try {
      makeRequest('/search/movie', 'POST', body).then(data => {
        setSearchResult(data.movies);
        setTotalPage(data.numPages);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }, [currentPage]);

  React.useEffect(() => {
    const body = {
      keyword: searchContent,
      page: 1,
      sortBy: sortSetting
    }
    try {
      makeRequest('/search/movie', 'POST', body).then(data => {
        setSearchResult(data.movies);
        setCurrentPage(1);
        setTotalPage(data.numPages);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }, [sortSetting]);

  const castButton = () => {
    window.location = `/search/cast/${searchContent}`;
  }

  const directorButton = () => {
    window.location = `/search/director/${searchContent}`;
  }

  const userButton = () => {
    window.location = `/search/user/${searchContent}`;
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
        <div className='row'>
          <h3 style={{ marginLeft: '5px', marginTop: '10px' ,color: '#0d6efd' }}>
            Search results for : "{searchContent}", Sorted by {sortSetting}
          </h3>
        </div>
        <br/>
        <div className='row'>
          <div className="col">
            <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 3, height: 30, backgroundColor: 'primary.dark' }} />
            <h3 style={{ fontWeight: 'bold', cursor: 'default' }}>Movie</h3>
          </div>
          <div className="col">
            <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 3, height: 30, backgroundColor: 'primary.dark' }} />
            <h3 style={{ cursor: 'pointer' }} onClick={castButton}>Cast</h3>
          </div>
          <div className="col">
            <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 3, height: 30, backgroundColor: 'primary.dark' }} />
            <h3 style={{ cursor: 'pointer' }} onClick={directorButton}>Director</h3>
          </div>
          <div className="col">
            <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 3, height: 30, backgroundColor: 'primary.dark' }} />
            <h3 style={{ cursor: 'pointer' }} onClick={userButton}>User</h3>
          </div>
          <div className="col">
            <FormControl sx={{ width: '222px', height: '40px' }}>
              <InputLabel id="sortSelect">Sort By</InputLabel>
              <Select
                size='small'
                labelId="sortSelect"
                value={sortSetting}
                label="Sort by"
                onChange={(event) => setSortSetting(event.target.value)}
              >
                <MenuItem value={'Relevance'}>Relevance</MenuItem>
                <MenuItem value={'Rating: High to Low'}>Rating: High to Low</MenuItem>
                <MenuItem value={'Rating: Low to High'}>Rating: Low to High</MenuItem>
                <MenuItem value={'Review: More to Less'}>Review: More to Less</MenuItem>
                <MenuItem value={'Review: Less to More'}>Review: Less to More</MenuItem>
                <MenuItem value={'Release: New to Old'}>Release: New to Old</MenuItem>
                <MenuItem value={'Release: Old to New'}>Release: Old to New</MenuItem>
                <MenuItem value={'Name: A to Z'}>Name: A to Z</MenuItem>
                <MenuItem value={'Name: Z to A'}>Name: Z to A</MenuItem>
                <MenuItem value={'Views: More to Less'}>Views: More to Less</MenuItem>
                <MenuItem value={'Views: Less to More'}>Views: Less to More</MenuItem>
              </Select>
            </FormControl>
          </div>
        </div>
        <br/>
        {searchResult.map((result, index) => {
          return <SearchResultMovie key={index} movieId={result.movie_id} moviePicture={result.movie_cover} movieName={result.movie_name} movieDescription={result.movie_description} movieRating={result.movie_rating} movieReview={result.numReview}></SearchResultMovie>
        })}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '10px' }}>
          <Pagination count={totalPage} color="primary" page={currentPage} onChange={(e, value) => setCurrentPage(value)} />
        </div>
      </div>
    </>
  );
}

export default SearchMovie;
