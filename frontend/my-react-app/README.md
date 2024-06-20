# EncryptoDevs Final Project
## Private Messaging Web App

### Getting Started
<p>
<ol>
<li>
Clone repository from Github <a href="https://github.com/JoshS-21/encryptodevs.git"> here</a>.
</li>
<li>
Ensure you have <a href="https://www.python.org">Python</a> and <a href="https://nodejs.org/en">Node.js</a> installed on your machine.
</li>
<li> Ensure you have <a href="https://www.mongodb.com/docs/manual/administration/install-community/DB">MongoDB</a> and <a href="https://www.mongodb.com/docs/compass/current/install/">Compass</a> installed on your machine. 
<li>
Open project in your preferred IDE
</li>
<li>
Open your terminal, and navigate to the 'api' directory. Run `python3 -m pip install -r requirements.txt` to install the dependencies for the Flask backend app. 
</li>
<li>
While still in the 'api' directory, run `python3 mongodb_initialization.py` to initialise the database. Use Compass to verify the creation of the 'encryptodevs' database and a 'users' collection containing one test user called 'abdio'.
</li>
<li>
'cd' into the 'frontend/my-react-app' directory. Run `npm install` to install the dependencies for the React frontend app.
</li>
<li>
Whilst still in the 'frontend/my-react-app' directory, run `npm start` and click <a href="http://localhost:3000">http://localhost:3000</a> to launch the browser. The page will reload when you make changes.
You may also see any lint errors in the console.
</li>
<li>
Open a new terminal leaving the first open and cd to the 'api' directory. Run `python3 app.py` to start the backend server.
</li>
</ol>
</p>
<p>
You can now test the app running on your local server. You can use Compass to view items (users and messages) in the MongoDB database.
</p>











