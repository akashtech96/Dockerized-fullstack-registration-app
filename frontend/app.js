const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");
const path = require("path");

const app = express();

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.render("index");
});

app.post("/submit", async (req, res) => {
    try {
        const response = await axios.post(
            "http://backend:5000/submit",
            req.body
        );

        res.send(response.data);

    } catch (err) {
        console.error(err.response?.data || err.message);

        res.send(err.response?.data || err.message);
    }
});

const PORT = 3000;

app.listen(PORT, () => {

  console.log(`Frontend running on http://localhost:${PORT}`);

});