from deadline import find_links_deadline, find_article_deadline
from hollywoodreporter import find_links_hollywoodreporter, find_article_hollywoodreporter
from indiwire import find_links_indiwire, find_article_indiwire
from variety import find_article_variety, find_links_variety
from processing import process_links

# Process Deadline articles
deadline_links = find_links_deadline()
process_links(find_article_deadline, deadline_links)

# Process Hollywood Reporter articles
hollywoodreporter_links = find_links_hollywoodreporter()
process_links(find_article_hollywoodreporter, hollywoodreporter_links)

# Process Indiwire
indiwire_links = find_links_indiwire()
process_links(find_article_indiwire, indiwire_links)

# Process variety
variety_links = find_links_variety()
process_links(find_article_variety, variety_links)


