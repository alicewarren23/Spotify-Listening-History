# SpotifyHistory

The aim of this project is to create an interactive dashboard displaying my all-time spotify listening history, broken down by song, artist, genre, album etc.. 
This pipeline at the moment is connecting an ITFFF app from my spotify to a google sheet which automously adds a new row with relevent data everytime a song is played, however the app automatically creates a new google sheet after 2000 rows and therefore I have a script to convert the data from the google sheet to a CSV and then another to move the new CSV data into a google sheet (with unlimited row) which then connects directly to google looker studio. 
