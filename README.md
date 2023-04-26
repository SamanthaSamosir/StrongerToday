## Overview
  StrongerToday is a Python-based application that provides daily motivational quotes or prompts to help users stay inspired and focused on   their goals. The app has a minimalist user interface, making it easy to use for people of all ages and backgrounds. Users can also choose to receive daily      quotes via email to keep them motivated throughout the day. This documentation includes features, installations, API integration, etc.
  
## Features
   1. User authentication: User able to create a personal account, and use proper charaters/numbers.
   3. Courier API: The app utilizes the Courier to send notification via email.
   4. Forismatic API: App able to generate quotes or word encouragement.

## Installation
   1. Download and install Pycharm, XAMPP (for the MySQL connection), and Navicat (for the DBMS).
   2. Create a new project in the Pycharm by cloning my `https://github.com/SamanthaSamosir/StrongerToday.git`. Install all libraries that are needed.
   3. Create a new database `strongtoday` and table `users` at Navicat or phpmyadmin.
   4. Prepare for the Courier API and Formastic API, use your own API KEY for the Courier API. Formastic API doesn't need API KEY.
   5. Read and follow all comments inside of the code. Run the program.
   
## How to Use The App
   Please watch the uploaded video: `https://www.facebook.com/100084127461354/videos/243146718371654/`

## Courier API Integration
   First, create a Courier account. Then, obtained the test/prod API KEY. Write the script (check out more inside the main.py). I use {body} for the content of the messages, and {recipientName} for the user's name.

## Forismatic API
   Use http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en" to request response.


 
