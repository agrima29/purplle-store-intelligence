import axios from "axios";

const API = axios.create({
  baseURL: "https://purplle-store-intelligence-dlca.onrender.com/api/v1",
});

export default API;