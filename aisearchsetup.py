from aisearchhelper import *

# create index definition in Azure AI Search
create_index('tenderindex_00x')

# upload documents to index
# if no owner is specified then default owner is ameetk
upload_document("documentpath")
upload_document("documentpath","ownername")

# search for a query in the index
print (single_vector_search("query")) # if search has to be done without filtering by owner
print (single_vector_search_with_filter("query","ameetk")) # if search has to be filtered by owner
