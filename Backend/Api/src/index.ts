import express from 'express';
import bodyParser from 'body-parser';
import dotenv from 'dotenv';
import router from './route';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

// Middleware to parse JSON bodies
app.use(bodyParser.json());

app.use("/", router);

// Run the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

export default app;
