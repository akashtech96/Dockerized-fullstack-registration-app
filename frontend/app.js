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

        res.status(response.status).json(response.data);

    } catch (err) {

        res
            .status(err.response?.status || 500)
            .json(err.response?.data || {
                success: false,
                error: "Internal Server Error"
            });

    }

});