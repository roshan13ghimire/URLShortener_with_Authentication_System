import { useState } from "react";
import API from "../services/api";
import { useNavigate } from "react-router-dom";

function Signup() {

  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async () => {
    try {

      const res = await API.post("/signup", {
        name,
        password
      });

      alert(res.data.message);

      navigate("/");

    } catch (error) {
      alert("Signup failed");
    }
  };

  return (
    <div style={styles.container}>

      <div style={styles.card}>

        <h2 style={styles.title}>Signup</h2>

        <input
          style={styles.input}
          placeholder="Username"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <input
          style={styles.input}
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button style={styles.button} onClick={handleSignup}>
          Signup
        </button>

        <p style={styles.link} onClick={() => navigate("/")}>
          Already have an account? Login
        </p>

      </div>

    </div>
  );
}

const styles = {

  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#f4f6f8"
  },

  card: {
    width: "320px",
    padding: "25px",
    borderRadius: "12px",
    backgroundColor: "white",
    boxShadow: "0 6px 20px rgba(0,0,0,0.1)",
    textAlign: "center"
  },

  title: {
    marginBottom: "20px"
  },

  input: {
    width: "100%",
    padding: "12px",
    marginBottom: "12px",
    borderRadius: "8px",
    border: "1px solid #ddd",
    outline: "none"
  },

  button: {
    width: "100%",
    padding: "12px",
    border: "none",
    borderRadius: "8px",
    backgroundColor: "#4f46e5",
    color: "white",
    cursor: "pointer"
  },

  link: {
    marginTop: "10px",
    fontSize: "13px",
    color: "#4f46e5",
    cursor: "pointer"
  }
};

export default Signup;