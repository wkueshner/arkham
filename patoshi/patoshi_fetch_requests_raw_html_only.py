import requests
from bs4 import BeautifulSoup
import csv
import time

def get_block_info(block_number):
    url = f'http://satoshiblocks.info/?bn={block_number}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        try:
            div_content_html = soup.select_one('body > table > tbody > tr > td:nth-child(1) > div:nth-child(2) > div:nth-child(2)').decode_contents()
            parts = div_content_html.split('</a>', 1)
            
            if len(parts) > 1:
                entity_html = parts[0] + '</a>'
                ExtraNonce_html = parts[1]
                
                entity = BeautifulSoup(entity_html, 'html.parser').get_text().strip()
                ExtraNonce = BeautifulSoup(ExtraNonce_html, 'html.parser').get_text().strip()
                
                if not entity or not ExtraNonce:
                    return "Not found", "Not found"
                return entity, ExtraNonce
            else:
                return "Not found", "Not found"
        except Exception as e:
            print(f"Error processing block number {block_number}: {str(e)}")
            return "Error", "Error"
    else:
        return "Request failed", "Request failed"

def main():
    with open('block_info_requests.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['block_number', 'entity', 'ExtraNonce'])
        
        for block_number in range(50000):
            entity, ExtraNonce = get_block_info(block_number)
            writer.writerow([block_number, entity, ExtraNonce])
            print(f"Processed block number {block_number}")
            time.sleep(0.1)  # slight delay to avoid overwhelming the server

if __name__ == '__main__':
    main()
