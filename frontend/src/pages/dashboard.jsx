import { useEffect, useState } from "react";
import axios from "axios";

function Dashboard() {

  const [longUrl, setLongUrl] = useState("");
  const [urls, setUrls] = useState([]);

  // -------------------------
  // FETCH ALL URLS
  // -------------------------
  const fetchUrls = async () => {

    try {

      const res = await axios.get(
        "http://127.0.0.1:5000/my-urls"
      );

      setUrls(res.data);

    } catch (error) {

      console.log(error);
      alert("Failed to fetch URLs");

    }
  };

  // load URLs when page opens
  useEffect(() => {

    fetchUrls();

  }, []);

  // -------------------------
  // SHORTEN URL
  // -------------------------
  const handleShorten = async () => {

    try {

      await axios.post(
        "http://127.0.0.1:5000/shorten",
        {
          long_url: longUrl
        }
      );

      // clear input
      setLongUrl("");

      // refresh URL list
      fetchUrls();

    } catch (error) {

      console.log(error);
      alert("Failed to shorten URL");

    }
  };

  return (
    <div style={{ padding: "20px" }}>

      <h1>Dashboard</h1>

      {/* INPUT */}
      <input
        type="text"
        placeholder="Enter long URL"
        value={longUrl}
        onChange={(e) => setLongUrl(e.target.value)}
        style={{
          width: "300px",
          padding: "10px"
        }}
      />

      <button
        onClick={handleShorten}
        style={{
          marginLeft: "10px",
          padding: "10px"
        }}
      >
        Shorten
      </button>

      <hr />

      <h2>My URLs</h2>

      {/* URL LIST */}
      {urls.map((url) => (

        <div
          key={url.short_code}
          style={{
            border: "1px solid gray",
            padding: "15px",
            marginBottom: "15px"
          }}
        >

          <p>
            <strong>Long URL:</strong>
            <br />
            {url.long_url}
          </p>

          <p>
            <strong>Short URL:</strong>
            <br />

            <a
              href={url.short_url}
              target="_blank"
              rel="noreferrer"
            >
              {url.short_url}
            </a>

          </p>

        </div>

      ))}

    </div>
  );
}

export default Dashboard;