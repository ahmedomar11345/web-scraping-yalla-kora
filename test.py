import requests  # Imports the requests library for making HTTP requests.
from bs4 import BeautifulSoup  # Imports BeautifulSoup from the bs4 library for parsing HTML.
import csv  # Imports the csv library for handling CSV file operations.

date = input("Please enter the Date in the following format MM/DD/YYYY: ")  # Prompts the user to enter a date.
page = requests.get(f'https://www.yallakora.com/Match-Center/?data={date}')  # Sends a GET request to the specified URL with the user-provided date.

def main(page):  # Defines the main function that processes the page content.
    src = page.content  # Gets the content of the page.
    soup = BeautifulSoup(src, "lxml")  # Parses the page content with BeautifulSoup using the lxml parser.
    matches_details = []  # Initializes an empty list to store match details.
    championships = soup.find_all("div",{"class":"matchCard"})  # Finds all match cards on the page.

    def get_match_info(championships):  # Defines a function to extract match information from championship data.
        championship_title = championships.contents[1].find('h2').text.strip()  # Extracts and cleans the championship title.
        all_matches = championships.contents[3].find_all("div",{"class":"liItem"})  # Finds all match items within the championship.
        number_of_matches = len(all_matches)  # Determines the number of matches.

        for i in range(number_of_matches):  # Loops through each match.
            team_A = all_matches[i].find('div',{'class': 'teamA'}).text.strip()  # Extracts and cleans the name of Team A.
            team_B = all_matches[i].find('div',{'class': 'teamB'}).text.strip()  # Extracts and cleans the name of Team B.

            match_result = all_matches[i].find('div',{'class': 'MResult'}).find_all('span',{'class': 'score'})  # Finds match scores.
            if match_result:  # Checks if match result exists.
                score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"  # Formats and cleans the match score.
            else:
                score = "N/A"  # Sets score to "N/A" if no result is found.

            match_time = all_matches[i].find('div',{'class': 'MResult'}).find('span',{'class': 'time'}).text.strip()  # Extracts and cleans the match time.
            tour = all_matches[i].find('div',{'class': 'topData'}).find('div',{'class': 'date'}).text.strip()  # Extracts and cleans the tour date.
            match_status = all_matches[i].find('div',{'class':'topData'}).find('div',{'class':'matchStatus'}).find('span').text.strip()  # Extracts and cleans the match status.

            matches_details.append({"نوع البطولة": championship_title,  # Appends match details to the list.
                                    "الفريق الاول": team_A,
                                    "الفريق الثاني": team_B,
                                    "ميعاد المباراة": match_time,
                                    "النتيجة": score,
                                    "الجولة": tour,
                                    "حالة المباراة": match_status})

    for i in range(len(championships)):  # Loops through each championship to get match information.
        get_match_info(championships[i])

    if matches_details:  # Checks if there are any match details to write to a file.
        Keys = matches_details[0].keys()  # Gets the keys from the first dictionary in the list.
        with open('match_details.csv', 'w', encoding='utf-8-sig', newline='') as output_file:  # Opens a new CSV file for writing.
            dict_writer = csv.DictWriter(output_file, fieldnames=Keys)  # Creates a CSV DictWriter object.
            dict_writer.writeheader()  # Writes the header row to the CSV file.
            dict_writer.writerows(matches_details)  # Writes all match details to the CSV file.
            print("File created")  # Prints a message indicating that the file has been created.
    else:
        print("No match details found.")  # Prints a message if no match details were found.

main(page)  # Calls the main function with the page content.
