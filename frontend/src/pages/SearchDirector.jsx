import React from 'react';
import ErrorBar from '../components/ErrorBar';
import { useParams } from 'react-router-dom';
import makeRequest from '../helpers/Fetch';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Pagination from '@mui/material/Pagination';
import SearchResultDirector from '../components/SearchResultDirector';
import SuccessBar from '../components/SuccessBar';
const SearchDirector = () => {
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
      makeRequest('/search/director', 'POST', body).then(data => {
        setSearchResult(data.directors);
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
      makeRequest('/search/director', 'POST', body).then(data => {
        setSearchResult(data.directors);
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
      makeRequest('/search/director', 'POST', body).then(data => {
        setSearchResult(data.directors);
        setCurrentPage(1);
        setTotalPage(data.numPages);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    } catch (error) {
      setErrorOpen(true);
      setErrorMessage(error);
    }
  }, [sortSetting]);

  const movieButton = () => {
    window.location = `/search/movie/${searchContent}`;
  }

  const castButton = () => {
    window.location = `/search/cast/${searchContent}`;
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
            <h3 style={{ cursor: 'pointer' }} onClick={movieButton}>Movie</h3>
          </div>
          <div className="col">
            <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 3, height: 30, backgroundColor: 'primary.dark' }} />
            <h3 style={{ cursor: 'pointer' }} onClick={castButton}>Cast</h3>
          </div>
          <div className="col">
            <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 3, height: 30, backgroundColor: 'primary.dark' }} />
            <h3 style={{ fontWeight: 'bold', cursor: 'default' }}>Director</h3>
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
                <MenuItem value={'Name: A to Z'}>Name: A to Z</MenuItem>
                <MenuItem value={'Name: Z to A'}>Name: Z to A</MenuItem>
                <MenuItem value={'Performances: More to Less'}>Performances: More to Less</MenuItem>
                <MenuItem value={'Performances: Less to More'}>Performances: Less to More</MenuItem>
                <MenuItem value={'Views: More to Less'}>Views: More to Less</MenuItem>
                <MenuItem value={'Views: Less to More'}>Views: Less to More</MenuItem>
                <MenuItem value={'Age: Old to Young'}>Age: Old to Young</MenuItem>
                <MenuItem value={'Age: Young to Old'}>Age: Young to Old</MenuItem>
              </Select>
            </FormControl>
          </div>
        </div>
        <br/>
        {searchResult.map((result, index) => {
          return <SearchResultDirector key={index} directorId={result.director_id} directorPhoto={result.director_cover} directorName={result.director_name} directorDescription={result.director_description} directorViews={result.director_views} directorPerformance={result.numOfPerformances}></SearchResultDirector>
        })}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '10px' }}>
          <Pagination count={totalPage} color="primary" page={currentPage} onChange={(e, value) => setCurrentPage(value)} />
        </div>
      </div>
    </>
  );
}

export default SearchDirector;
