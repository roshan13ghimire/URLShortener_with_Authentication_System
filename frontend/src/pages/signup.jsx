import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Signup() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async () => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/signup",
        {
          name,
          password,
        }
      );

      alert(res.data.message);

      // go to login page
      navigate("/");
    } catch (error) {
      console.log(error);
      alert("Signup failed");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Signup</h1>

      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <br /><br />




      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <br /><br />

      <button onClick={handleSignup}>
        Signup
      </button>
    </div>
  );
}

export default Signup;