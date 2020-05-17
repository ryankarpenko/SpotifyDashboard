# SpotifyDashboard
Dashboard of audio features and usage statistics for my personal Spotify data from April 2019 to March 2020.

LINK: https://app.powerbi.com/view?r=eyJrIjoiMTUyNjQyZjYtYzZhMy00YzMxLWFkMjYtODAxYWJjYTQxOTFkIiwidCI6ImY0M2EwZDVjLTdlMTItNDNhYy04ZWIyLWNmZTEwMjkwZGFhYSJ9

While the Spotify API can provide basic summary user statistics such as top 10 artists of the year etc., it cannot give detailed user data on individual played tracks. Instead, granular data for the last year can be mmanually requested from Spotify. This data is essentially a list of tracks with a track name, artist name, date/time played, and number of milliseconds played. To get more information on these tracks (including the track id's), I used the Spotify API to search for the track (similar to how you search in the app), then programmatically determined which search result was correct to get the id. Finally, I queried the API again for artist and album info, as well as for audio features such as "instrumentalness" and "energy".

The dashboard contains the following visualizations of my Spotify data:

1: Audio Features by Playlist

One of my favorite activites on Spotify is to make playlists with a specific sound in mind. This page allows you to compare the audio features of several of my playlists. For example, you might compare how the energy differs between a noir jazz playlist and a hip hop playlist. Each feature value is a weighted average based on the length of each song in the playlist. Most of the playlists have decently descriptive names, but others might not be as clear. On the page is a link to my personal Spotify profile, containing a selection of these playlists.

2: Audio Features by Month

Here you can find a line graph of the weighted mean of audio features for each month in the dataset. the values don't vary drastically from month to month, but it interesting to see, for example, acousticness go up over time while energy goes down. Also note that on pages 1, 2, and 5, the feature descriptions are taken directly from Spotify's official API documentation.

3: Top 100 By Season

This page contains three tables - my top 100 tracks, artists, and albums - for each season of the year. I aggregated them by season so that the results would be more stable. Additionally, I feel that these seasons are of particular relevance in my life. For example, spring 2019 was exam period during my master's, and during summer 2019 I was writing my thesis and listening to a tremendous amount of jazz. The changes in my track/artist/album lists reflect these periods of my life.

4: Most Distinctive Artists By Month

For each artist, I calculated how much I listened to them in a given month relative to the rest of the year. This shows me which artist uniquely defined each month of my year. Some of them are the result of new albums that I listened to several times and then never again. Others are special cases, such as JAY-Z putting all of his music catalog on Spotify in December. And others still are exactly what I'm looking for: I went to a Sons of Kemet concert in July and wanted to familiarize myself with their back catalog, and in January I finally discovered James Blake's run of 2010 EP's. As you can tell, this page is very interesting to me.

5: Custom Scatter Plot - Audio Features

While pages 3 and 4 are interesting as summaries of my listening habits, they don't offer much exploration by slicing, etc. I wanted to add some more of that to the dashboard, and so I created this plot which allows you to select the audio features for the x and y axes. This took some trickery to implement in Power BI, and there were far too many data points to show any relationships clearly. Each point is a track that I listened to during the year, so the sample is only representative of my music tastes. And the points that are shown are a random sample of the total tracks. But regardless, there are some interesting correlations that can be found.
