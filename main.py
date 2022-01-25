#Forgetmenot flora
# Webscraping flashcard creator for memorization of botanical speciemens and their information
import requests
import pdfkit
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
# print(path_wkhtmltopdf)
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)



#end goal

# 1-6 photos in a cllage (own photos)
#multiple photo selection for collage taking 2/3 size of factsheet
# 1-leaf, 2-habit, 3-flower, 4-flower, 5-fruit, 6-seed
#if not own photos -> option to import
# modifiable to add more photos

# species name (formatted - italics), comon name, family, genus
# family key for genus (colour ability -> red for summary) (save and optional reuse)
# genus key for species (maybe description and notes too) (colour ability -> red for summary) (source from other sites e.g. wiki / inat (traditional/medicvinal use, similar species))
# summary recap of genus
    # genera key from genus page
    # select 

# optional additional info for threatened species https://www.environment.nsw.gov.au/threatenedspeciesapp/profile.aspx?id=10244 / +conservation status (optional)
#distribution map / habitat / occurance / flowering time
#google scholar search / fun facts section optional
#css bootstrap template for photos?

#Features to add

#picture selection

# autoprint option?
# sourcing from multiple websites - inaturalist, wikipedia
# selecting parts of keys
# better naming, common name etc

#sound effects -> reward

def main():
    #take in txt file of plant names, followed by any special characters indicating initial informaiton to be retrieved
    #for each plant name, verify existence on provided database
    #If exists,
        #scrape key
        #scrape photos
        #create image file containing info

    with open('plants.txt') as p:
        for line in p:
            plantName = line.split()

            # print(plantName)

            plantNameSeperated = ''
            plantNameSeperated2 = ''

            #prepare string for URL creation
            for idx,word in enumerate(plantName):
                
                if idx < len(plantName)-1:
                    plantNameSeperated = plantNameSeperated + word + '~'
                    plantNameSeperated2 = plantNameSeperated2 + word + '_'
                else:
                    plantNameSeperated = plantNameSeperated + word
                    plantNameSeperated2 = plantNameSeperated2 + word
            

            url = "https://plantnet.rbgsyd.nsw.gov.au/cgi-bin/NSWfl.pl?page=nswfl&lvl=sp&name=" + plantNameSeperated
            url2 = "https://en.wikipedia.org/wiki/" + plantNameSeperated2
            print(url)
            print(url2)

            
            try:
                page = requests.get(url)
                # print(page.text)
            except Exception as e:
                print("No such page!")
                # print(e)
                break

            try:
                page2 = requests.get(url2)
                # print(page.text)
            except Exception as e:
                print("No such page!")
                # print(e)
                break
                

            
            foundFlag = 0
            DescriptionText = '<h1>' + ' '.join(plantName) + '</h1>' + '\n' 
            

            #scraping plantnet HTML data
            if page != None:
                for line in page.text.split(' '):
                    # print(line)
                    while True:
                        # add habitat and distribution

                    
                        if "<p><b>Description:</b>" in line:
                            foundFlag = 1
                        if foundFlag == 1:
                            if "APNI*" in line:
                                foundFlag = 0
                                break
                            if foundFlag == 1:
                                if "src" in line:
                                    line = line.lstrip('src="..')
                                    line = 'src="https://plantnet.rbgsyd.nsw.gov.au' + line
                                if "href" in line:
                                    line = line.lstrip('href="')
                                    line = 'href="https://plantnet.rbgsyd.nsw.gov.au' + line
                                    
                                DescriptionText = DescriptionText + line + ' '
                        break
                
                
            #scraping wikipedia data
            #scraping plantnet HTML data
            if page2 != None:
                for line in page2.text.split(' '):
                    # print(line)
                    while True:
                        # add habitat and distribution
                    
                        if "Gallery" in line:
                            foundFlag = 1
                        if foundFlag == 1:
                            if "See_also" in line:
                                foundFlag = 0
                                break
                            if foundFlag == 1:
                                if "href" in line:
                                    line = line.lstrip('href="')
                                    line = 'href="https://en.wikipedia.org' + line
                                if "src" in line:
                                    line = line.lstrip('src="/')
                                    line = 'src="https:/' + line
                                    
                                DescriptionText = DescriptionText + line + ' '
                        break
                

            name = '_'.join(plantName)              


            with open(name + ".txt", 'w+') as newFile:
                newFile.writelines(DescriptionText)
                newFile.close
            
            
            ready = input("Please edit description information in " + str(name) + ".txt, and enter 'y' when complete!")
            while ready != 'y':
                ready = input("Please edit description information in " + str(name) + ".txt, and enter 'y' when complete!")

            with open(name + ".html", 'w+') as newFileHTML:
                with open(name + ".txt") as editedFile:
                    editedTxt = editedFile.readlines()
                    editedFile.close
                newFileHTML.writelines(editedTxt)
                newFileHTML.close()

            pdfkit.from_file(name + ".html", name + '.pdf')
            
        p.close
                        
      
            
            
                
main()