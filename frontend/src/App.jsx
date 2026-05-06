import './App.css';
import NavBar from "./components/NavBar";
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import  'bootstrap/dist/css/bootstrap.min.css' ;
import SearchMovie from './pages/SearchMovie';
import SearchCast from './pages/SearchCast';
import SearchDirector from './pages/SearchDirector';
import SearchUser from './pages/SearchUser';
import Profile from './pages/Profile';
import MovieDetail from './pages/MovieDetail';
import WishList from './pages/WishList';
import WatchedList from './pages/WatchedList';
import BlackList from './pages/BlackList';
import Message from './pages/Message';
import DirectorDetail from './pages/Director';
import CastDetail from './pages/Cast';
import OtherProfile from './pages/OtherPeopleProfile';
import OtherWishList from './pages/OtherWishList';
import OtherWatchedList from './pages/OtherWatchedList';


function App() {
  return (
    <>
      <NavBar></NavBar>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Home/>} />
          <Route path='/search/movie/:searchContent' element={<SearchMovie/>} />
          <Route path='/search/cast/:searchContent' element={<SearchCast/>} />
          <Route path='/search/director/:searchContent' element={<SearchDirector/>} />
          <Route path='/search/user/:searchContent' element={<SearchUser/>} />
          <Route path='/profile' element={<Profile/>} />
          <Route path='/wishlist' element={<WishList/>} />
          <Route path='/watchedlist' element={<WatchedList/>} />
          <Route path='/blacklist' element={<BlackList/>} />
          <Route path='/movie/:movieId/:movieName' element={<MovieDetail/>} />
          <Route path='/message' element={<Message/>} />
          <Route path='/director/:directorId/:directorName' element={<DirectorDetail/>} />
          <Route path='/cast/:castId/:castName' element={<CastDetail/>} />
          <Route path='/otherprofile/:userId' element={<OtherProfile/>} />
          <Route path='/OtherPeopleWishList/:userId/:userName' element={<OtherWishList/>} />
          <Route path='/OtherPeopleWatchedList/:userId/:userName' element={<OtherWatchedList/>} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
