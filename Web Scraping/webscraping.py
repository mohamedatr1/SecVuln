import pandas as pd
from bs4 import BeautifulSoup
import requests


def get_web_data():
    print("______Connecting to website______")
   
    html_content = """
    <table>
        <tr><th>Location</th><th>Sales</th></tr>
        <tr><td>Riyadh</td><td>500</td></tr>
        <tr><td>Cairo</td><td>300</td></tr>
        <tr><td>Dubai</td><td>700</td></tr>
        <tr><td>Riyadh</td><td>450</td></tr>
    </table>
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('tr')[1:]
    
    extracted_data = []
    for row in rows:
        cols = row.find_all('td')
        extracted_data.append({
            'location': cols[0].text,
            'sales': int(cols[1].text)
        })
    return extracted_data


raw_data = get_web_data()
df = pd.DataFrame(raw_data)


average_sales = df.groupby("location")["sales"].sum()
mean_sales = df.groupby("location")["sales"].mean()


print("\n--- Sales Analysis Report ---")
print(average_sales)
print("\n--- Statistical Mean ---")
print(mean_sales)


average_sales.to_csv("Web Scraping/final_sales_report.csv")
print("\n[+] Report saved: final_sales_report.csv")