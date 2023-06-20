# project-1-web-application-design-education-pathways-group-7-waterfall

## Project Description

This application builds upon the existing education pathways codebase and adds new features to better help students plan their course selection.

## Tools

- Project Management: GitHub Projects
- Issue Tracking: GitHub Issues
- UI Planning: Whimsical

The original source code can be found [here](https://github.com/ECE444-2022Fall/Assignment_1_starter_template).

## Tech Stack
- React (Node.js)
- Flask (Python)

## Getting Started

### Running Locally

+ Enter the repo directory
+ Create a virtual environment if you haven't done this before. Activate it. 
```powershell
# Windows
py -3 -m venv venv
venv\Scripts\activate

# For Mac and Linux, please check the link: https://flask.palletsprojects.com/en/2.2.x/installation/
```
+ Install dependencies (if you haven't done this before).
```powershell
pip install -r requirements.txt
```
+ Enter the `Education_Pathways/` directory, run the backend
```powershell
flask --app index --debug run
```
+ Enter the `Education_Pathways/frontend/` directory
+ Make sure the `baseURL` is set as `localhost:5000`
```javascript
# Education_Pathways/frontend/src/api.js
export default axios.create({
   baseURL: "http://localhost:5000/"
});
```
+ Make sure the proxy link in package.json is set as "http://localhost:5000/"
```json
// Part of Education_Pathways\frontend\package.json
"private": true,
"proxy": "http://localhost:5000/",
```

+ Build and run the frontend:
```powershell
npm run build
npm start
```
+ Then you will see the application at `localhost:3000`

### Utilising Docker

For detailed instructions on Docker, please refer to the documents for Lab3 on Quercus.

+ Change the proxy link in package. Remember to change it back to "http://localhost:5000/"
```json
// Part of Education_Pathways/frontend/package.json
"private": true,
"proxy": "http://host.docker.internal:5000/",
```

```powershell
# Under the root directory
docker compose up --build
```

### Deployment

Please make sure everything works well before you run it with docker.

+ Make sure the baseURL is set as [URL to your deployed project]
```javascript
// Education_Pathways/frontend/src/api.js
export default axios.create({
   baseURL: "[URL to your deployed project]" -- baseURL for deployment
});
```
+ Re-build the frontend to update the baseURL
```powershell
# Under the frontend/ directory
npm run build
```
+ Deploy your changes to heroku
```powershell
git push heroku main
```

## Roadmap

GitHub Projects (see [here](https://github.com/orgs/ECE444-2022Fall/projects/8)) is used to track sprint work for the application.

## Contributing

Please see [CONTRIBUTION.md](CONTRIBUTION.md)

## Code Of Conduct

Please see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

