import { useNavigate } from "react-router-dom";

function Navbar() {

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("userid");
    navigate("/");
  };

  return (
    <div style={styles.nav}>

      <h2 style={styles.logo}>URL Shortener</h2>

      <button onClick={handleLogout} style={styles.button}>
        Logout
      </button>

    </div>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    padding: "15px",
    backgroundColor: "#222",
    color: "white",
    alignItems: "center"
  },

  logo: {
    margin: 0
  },

  button: {
    padding: "8px 12px",
    cursor: "pointer"
  }
};

export default Navbar;