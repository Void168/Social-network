import axios from "axios";

const getUserInfo = async (id) => {
  const user = await axios
    .get(`/api/user-info/${id}`)
    .then((res) => {
      return res.data
    })
    .catch((error) => {
      console.log(error);
    });

  return user.user;
};

export default getUserInfo;
