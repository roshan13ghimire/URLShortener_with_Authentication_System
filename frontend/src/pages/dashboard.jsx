import { useEffect, useState } from "react";
import API from "../services/api";
import Navbar from "../components/Navbar";

function Dashboard() {

  const [urls, setUrls] = useState([]);
  const [longUrl, setLongUrl] = useState("");

  const userid = localStorage.getItem("userid");

  // fetch urls
  const fetchUrls = async () => {
    try {
      const res = await API.get(`/my-urls/${userid}`);
      setUrls(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchUrls();
  }, []);

  // shorten url
  const handleShorten = async () => {
    try {

      if (!longUrl) {
        alert("Please enter a URL");
        return;
      }

      await API.post("/shorten", {
        long_url: longUrl,
        user_id: userid
      });

      setLongUrl("");
      fetchUrls();

    } catch (error) {
      console.log(error);
      alert("Failed to shorten URL");
    }
  };

  // copy to clipboard
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert("Copied!");
  };

  return (
    <div>

      <Navbar />

      <div style={styles.container}>

        <h1 style={styles.title}>My URL Dashboard</h1>

        {/* SHORTEN FORM */}
        <div style={styles.form}>

          <input
            type="text"
            placeholder="Enter long URL"
            value={longUrl}
            onChange={(e) => setLongUrl(e.target.value)}
            style={styles.input}
          />

          <button onClick={handleShorten} style={styles.button}>
            Shorten
          </button>

        </div>

        {/* URL LIST */}
        <div style={styles.grid}>

          {urls.length === 0 ? (
            <p>No URLs found</p>
          ) : (
            urls.map((url) => (
              <div
                key={url.id || url.short_code}
                style={styles.card}
              >

                <p><b>Long URL:</b></p>
                <p style={styles.text}>{url.long_url}</p>

                <p><b>Short URL:</b></p>
                <a href={url.short_url} target="_blank">
                  {url.short_url}
                </a>

                <br /><br />

                <button
                  onClick={() => copyToClipboard(url.short_url)}
                  style={styles.button}
                >
                  Copy
                </button>

              </div>
            ))
          )}

        </div>

      </div>
    </div>
  );
}

const styles = {

  container: {
    padding: "20px",
    fontFamily: "Arial"
  },

  title: {
    textAlign: "center"
  },

  form: {
    display: "flex",
    gap: "10px",
    justifyContent: "center",
    marginTop: "20px"
  },

  input: {
    padding: "10px",
    width: "300px"
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
    gap: "15px",
    marginTop: "30px"
  },

  card: {
    border: "1px solid #ddd",
    borderRadius: "10px",
    padding: "15px",
    boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
  },

  text: {
    wordBreak: "break-word"
  },

  button: {
    padding: "8px 12px",
    cursor: "pointer"
  }
};

export default Dashboard;