import axios from 'axios';

export default axios.create({
  // baseURL: "https://lab3-docker.herokuapp.com/"
  //  baseURL: "http://localhost:5000/"
   baseURL: "https://education-pathways-waterfall.herokuapp.com/"
});