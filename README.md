# IMDB-Project

🎬 IMDb 2024 Data Dashboard
A data science mini-project to scrape, clean, and visualize IMDb movie data from 2024 using Python, MySQL, and Streamlit.

📌 Project Overview
This dashboard allows users to explore IMDb movie data from 2024 across multiple genres with interactive filters and visualizations.

✅ Features
🔝 Top 10 Movies by Rating and Votes
📊 Genre Distribution
⏱️ Average Duration by Genre
📈 Voting Trends by Genre
🔸 Rating Distribution
🏆 Top-Rated Movies per Genre
🥧 Most Popular Genres (by Total Votes)
🎬 Duration Extremes
🌡️ Genre-wise Ratings (Heatmap)
📉 Correlation: Ratings vs Votes
📁 Files

README.md: Project documentation (this file)
🛠️ How to Run Locally
Clone this repo
Install dependencies:
pip install -r requirements.txt
Run the Streamlit app:
streamlit run app.py
🔗 Data Source
IMDb
👨‍💻 Tech Stack
Python (Pandas, Seaborn, Matplotlib)
Selenium (for scraping - not included here)
MySQL (for data storage)
Streamlit (for visualization)

Here i have uploaded my IMDB movie filteration and visualisation using Selenium, webdriver for extracting web page from website.
Then we try to click load more button to show after 50 movies using def function, try & except also.
Next step to extract the path from the movie page's click on inspect to get the HTML using xpath copy to include in our selenium code.
We run that, then it takes somemore time, then we get the output as 1000 to 5000 movies as per our internet connectivity.
Then we clean it using import RE package, as per mentioned in the documentation. Finally cleaned movies including movie name,ratings,voting,duration & genres.
Connect with sql using install pymysql, sqlalchemy.
Create a proper environment for streamlit, get knowledge from video.
One another page with install streamlit, seaborn, matplotlib, pyplot.express, again get data from sql to run through streamlit.
With proper coding to show the presentation in easily understandable sliding, barchart, scatter chart and so on. Run the streamlit to show the final output.
