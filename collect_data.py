# import glassdoor webscraper
import glassdoor_webscraper as gws

#This line will open a new chrome window and start the scraping.
df = gws.get_jobs("data-science", 5, False)

# write result to csv
df.to_csv("glassdoor_jobs.csv", index=False)