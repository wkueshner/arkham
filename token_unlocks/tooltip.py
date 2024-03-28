import csv
import re

with open('test.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Now we use the XPath to find the tooltip element
    tooltip_text = "Apr 12, 2027\nUTC + 00:00\nAvailable Supply\n3,907,143,091.91 OP\n$15.32b\nUnlocked Supply\n1,851,543,871.67 OP\n$7.26b\nAllocations\nRetroactive Public Goods Funding\nTBD\n506,806,140.93 OP\n$1.99b\nUser Airdrops\nTBD\n570,141,831.24 OP\n$2.23b\nSeed Fund\nTBD\n231,928,233.98 OP\n$909.16m\nPartner Fund\nTBD\n231,928,233.98 OP\n$909.16m\nGovernance Fund\nTBD\n136,837,658.06 OP\n$536.40m\nUnallocated Ecosystem Fund\nTBD\n377,957,122.05 OP\n$1.48b\nCore Contributors\n790,542,417.92 OP\n$3.10b\nInvestors\n707,327,426.56 OP\n$2.77b\nRetroactive Public Goods Funding\n41,000,000.00 OP\n$160.72m\nGovernance Fund\n66,755,054.00 OP\n$261.68m\nUser Airdrops\n245,918,973.19 OP\n$964.00m"

    # Replace "TBD" with "(TBD)" before splitting
    tooltip_text_modified = tooltip_text.replace("\nTBD", " (TBD)")
    lines = tooltip_text_modified.split('\n')
    
    # Extract column names based on the specified line indices
    headers = ['Date', lines[2], lines[5]]
    additional_headers = [lines[i] for i in range(9, len(lines), 3)]
    headers.extend(additional_headers)
    csvwriter.writerow(headers)
    header_written = True
    
    # Write the data row
    data_row = [lines[0], lines[3], lines[6]]
    additional_data = [lines[i] for i in range(10, len(lines), 3)]
    data_row.extend(additional_data)
    csvwriter.writerow(data_row)

