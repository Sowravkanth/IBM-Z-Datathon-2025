CareerSight AI

**CareerSight AI** is an intelligent, end-to-end career intelligence platform designed for Indian job seekers and professionals. It leverages real Naukri.com job data, AI-powered skills analysis, and Google Gemini-driven learning guidance to offer tailored job recommendations, skills-gap analysis, market insights, and a comprehensive career development experience—all in a beautiful, modern web interface.

## Features

- **AI-Powered Job Recommendations:** Personalized job matches ranked by skill compatibility and preferences.
- **Comprehensive Skills Gap Analysis:** Identifies missing or in-demand skills from the Indian job market and every relevant job description.
- **Personalized AI Learning Roadmaps:** Google Gemini and fallback algorithms generate week-by-week upskilling plans targeting your dream roles.
- **Interactive Career Coach:** Chat-like experience for resume, skill, and career guidance—with real AI.
- **Resume Builder:** Step-by-step career profile builder with automatic sectioning (skills, experience, projects, certifications).
- **Market Intelligence Dashboards:** Top companies, salaries, high-demand locations, trending skills, and category trends.
- **Professional UI/UX:** Intuitive, mobile-responsive web frontend served by a Flask backend, ready for deployment.
- **Jupyter/Python Native:** Fully reproducible as a Jupyter multi-cell or single-cell notebook, supporting research, customization, and live demos.
- **Easy Data Integration:** Works with both real Naukri.com LDJSON datasets or generates realistic synthetic job listings for demo/testing.


## Quickstart

1. **Requirements:**
   - Python 3.8+
   - Jupyter / Jupyter Lab (recommended)
   - Access to Naukri.com LDJSON exported dataset (or fallback: synthetic data)
   - Internet access for Google Gemini API (or runs in fallback mode)

2. **Install Dependencies:**

   ```sh
   pip install flask scikit-learn pandas numpy google-generativeai jinja2 requests
   ```

3. **Run in Jupyter:**
   - **Option 1:** Use the multi-cell Jupyter notebook version (recommended for learning/customization).
   - **Option 2:** Use the single-cell “all-in-one” Jupyter code for rapid end-to-end deployment.

4. **Access the Web UI:**
   - Open [http://localhost:5000](http://localhost:5000) in your browser.
   - Try the “Job Recommendations,” “Skills Gap,” and “Learning Roadmap” pages.
   - Explore additional features: Resume Builder, AI Career Coach, Market Dashboard, and more.



## Data Structure

| Field              | Description                                 |
|--------------------|---------------------------------------------|
| job_id             | Unique job identifier                       |
| job_title          | Title of the job/posting                    |
| company            | Company name                                |
| location           | Location/city                               |
| category           | Job category                                |
| description        | Job description (raw text)                  |
| salary_min,max     | Parsed salary range                         |
| experience_min,max | Required/minimum experience                 |
| skills             | Extracted/standardized skills (list)        |
| skills_str         | Skills as a single string (for TF-IDF)      |



## Google Gemini API

CareerSight AI uses Gemini AI to produce advanced learning roadmaps, career chat responses, and more. The system will automatically use a real Gemini API key if provided, or fallback to built-in “mock” responses in offline mode.

- Set your Gemini API key with:
  ```sh
  export GEMINI_API_KEY=your_google_gemini_api_key
  ```
- Or edit the `GEMINI_API_KEY` in the notebook for out-of-the-box functionality.

***

## Customization

- **Change Port:**  
  Edit the `port=5000` parameter in `app.run(...)` to use another port number.
- **Data Source:**  
  Place your Naukri LDJSON file in the Jupyter directory, or update paths in the loader cell.
- **Skill Extraction:**  
  Extend `extract_skills_from_text()` with more skill patterns or keywords.

***

## Deployment

- **For Jupyter (Demo/Education):**  
  Run all notebook cells in order. The web app starts in a background thread and provides a live analytic dashboard at `localhost:5000`.
- **For Production:**  
  Adapt `app.py` and `requirements.txt` for deployment to Heroku, AWS, GCP, Azure, IBM Cloud, or your own Linux server.
- **For Security:**  
  Set a random `app.secret_key` and never share your Google API credentials in public code.

***

## License

MIT License

***

## Contacts & Credits

- Project Lead: Abishek
- AI/Backend: Google Gemini, Flask, Scikit-learn
- UI/UX: Jinja2, HTML, CSS (custom, no frameworks)
- Data Source: Real/simulated Naukri.com jobs

***

> “CareerSight AI — Your data-driven career companion. Built for the Indian tech ecosystem, ready for the world.”

***

**For technical help or further contributions, please contact or submit issues on GitHub.**
