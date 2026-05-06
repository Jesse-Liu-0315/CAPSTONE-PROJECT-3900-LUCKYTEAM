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
import SearchResultUser from '../components/SearchResultUser';
import SuccessBar from '../components/SuccessBar';

const SearchUser = () => {
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
      sortBy: sortSetting,
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken')
    }
    try {
      makeRequest('/search/user', 'POST', body).then(data => {
        setSearchResult(data.users);
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
      sortBy: sortSetting,
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken')
    }
    try {
      makeRequest('/search/user', 'POST', body).then(data => {
        setSearchResult(data.users);
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
      sortBy: sortSetting,
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken')
    }
    try {
      makeRequest('/search/user', 'POST', body).then(data => {
        setSearchResult(data.users);
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

  const directorButton = () => {
    window.location = `/search/director/${searchContent}`;
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
            <h3 style={{ cursor: 'pointer' }} onClick={directorButton}>Director</h3>
          </div>
          <div className="col">
            <Box sx={{ marginTop: '2px', marginRight: '5px', float: 'left', width: 3, height: 30, backgroundColor: 'primary.dark' }} />
            <h3 style={{ fontWeight: 'bold', cursor: 'default' }}>User</h3>
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
                <MenuItem value={'Views: More to Less'}>Views: More to Less</MenuItem>
                <MenuItem value={'Views: Less to More'}>Views: Less to More</MenuItem>
              </Select>
            </FormControl>
          </div>
        </div>
        <br/>
        {searchResult.map((result, index) => {
          return <SearchResultUser key={index} userId={result.user_id} userPhoto={result.user_profile_photo} userName={result.user_name} userTag={result.user_tag} userDescription={result.user_description === null ? '' : result.user_description} userViews={result.user_views}></SearchResultUser>
        })}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '10px' }}>
          <Pagination count={totalPage} color="primary" page={currentPage} onChange={(e, value) => setCurrentPage(value)} />
        </div>
      </div>
    </>
  );
}

export default SearchUser;
