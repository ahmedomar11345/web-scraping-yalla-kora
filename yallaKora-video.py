import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime

def display_welcome_message():
    print("""
    **************************************************
    *      Welcome to the Match Tracker Program!     *
    *      This program helps you get match details  *
    *      for any date you want.                    *
    **************************************************
    """)

def display_goodbye_message():
    print("""
    **************************************************
    *       Thank you for using Match Tracker!       *
    *            Have a great day!                   *
    **************************************************
    """)

def format_time_12h(time_str):
    """
    Convert time string to 12-hour format with AM/PM.
    """
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.strftime("%I:%M %p")
    except ValueError:
        return "N/A"

def get_match_info(championships):
    matches_details = []
    for championship in championships:
        championship_title = championship.find('h2').text.strip()
        all_matches = championship.find_all("div", {"class": "liItem"})
        for match in all_matches:
            team_A = match.find('div', {'class': 'teamA'}).text.strip()
            team_B = match.find('div', {'class': 'teamB'}).text.strip()

            match_result = match.find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}" if match_result else "N/A"

            match_time = match.find('div', {'class': 'MResult'}).find('span', {'class': 'time'})
            match_time = match_time.text.strip() if match_time else "N/A"
            match_time = format_time_12h(match_time)

            tour = match.find('div', {'class': 'topData'}).find('div', {'class': 'date'})
            tour = tour.text.strip() if tour else "N/A"

            match_status = match.find('div', {'class': 'topData'}).find('div', {'class': 'matchStatus'}).find('span')
            match_status = match_status.text.strip() if match_status else "N/A"

            match_info = {
                "Championship": championship_title,
                "Team A": team_A,
                "Team B": team_B,
                "Match Time": match_time,
                "Score": score,
                "Round": tour,
                "Match Status": match_status
            }
            matches_details.append(match_info)
    
    return matches_details

def create_html_file(matches_details, date):
    """
    Create an HTML file to display match details in a table.
    """
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", f"match_details_{date.replace('/', '_')}.html")
    
    # HTML template with CSS for styling
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تفاصيل المباريات - {date}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }}
            h1 {{
                text-align: center;
                color: #333;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            th, td {{
                padding: 12px 15px;
                text-align: right;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #007BFF;
                color: white;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
            .no-matches {{
                text-align: center;
                color: #777;
                font-size: 18px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>تفاصيل المباريات - {date}</h1>
    """

    if matches_details:
        html_content += """
        <table>
            <thead>
                <tr>
                    <th>البطولة</th>
                    <th>الفريق الأول</th>
                    <th>الفريق الثاني</th>
                    <th>موعد المباراة</th>
                    <th>النتيجة</th>
                    <th>الجولة</th>
                    <th>حالة المباراة</th>
                </tr>
            </thead>
            <tbody>
        """
        for match in matches_details:
            html_content += f"""
                <tr>
                    <td>{match['Championship']}</td>
                    <td>{match['Team A']}</td>
                    <td>{match['Team B']}</td>
                    <td>{match['Match Time']}</td>
                    <td>{match['Score']}</td>
                    <td>{match['Round']}</td>
                    <td>{match['Match Status']}</td>
                </tr>
            """
        html_content += """
            </tbody>
        </table>
        """
    else:
        html_content += '<div class="no-matches">لا توجد مباريات لهذا التاريخ.</div>'

    html_content += """
    </body>
    </html>
    """

    with open(desktop_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print(f"تم إنشاء ملف HTML في: {desktop_path}")

def main():
    display_welcome_message()
    time.sleep(2)

    date = input("الرجاء إدخال التاريخ بالصيغة التالية MM/DD/YYYY: ")
    print("جاري جلب البيانات...")
    time.sleep(1)

    url = f'https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}#days'
    page = requests.get(url)
    if page.status_code != 200:
        print(f"فشل تحميل الصفحة. الرجاء التحقق من اتصالك بالإنترنت. رمز الخطأ: {page.status_code}")
        return

    soup = BeautifulSoup(page.content, "lxml")
    championships = soup.find_all("div", {"class": "matchCard"})

    matches_details = get_match_info(championships)
    create_html_file(matches_details, date)

    display_goodbye_message()

if __name__ == "__main__":
    main()