# web scraper for UoM lecture recordings
# informed by https://realpython.com/python-web-scraping-practical-introduction/#interact-with-html-forms

import os
import requests
import mechanicalsoup
browser = mechanicalsoup.Browser()

username = # lol not giving you these
password = #
course_dict = {
    "10071" : "Mathematics 1",
    "10101" : "Dynamics",
    "10121" : "Quantum Physics and Relativity",
    # "10180" : "First Year Laboratory",
    "10191" : "Introduction to Astrophysics and Cosmology",
    "10302" : "Vibrations and Waves",
    "10342" : "Electricity and Magnetism",
    "10352" : "Properties of Matter",
    "10372" : "Mathematics 2",
    "10461" : "Physics in Everyday Life",
    "10471" : "Random Processes in Physics",
    "10622" : "Physics of Energy Sources",
    "10632" : "Introduction to the Physics of Living Processes",
    "10672" : "Advanced Dynamics",
    "10692" : "Physics of the Solar System",
    "20101" : "Introduction to Quantum Mechanics",
    "20141" : "Electromagnetism",
    "20161" : "Introduction to Programming for Physicists",
    "20171" : "Mathematics of Waves and Fields",
    # "20180" : "Second Year Laboratory",
    "20252" : "Fundamentals of Solid State Physics",
    "20312" : "Wave Optics",
    "20352" : "Thermal and Statistical Physics",
    "20401" : "Lagrangian Dynamics",
    "20431" : "Physics of Living Processes",
    "20491" : "Galaxies",
    "20612" : "Introduction to Photonics",
    "20672" : "Complex Variables and Vector Spaces",
    "20682" : "Additional Laboratory Project",
    "20692" : "High Energy Astrophysics",
    "20762" : "Computational Physics",
    "20811" : "Professional Skills",
    "20872" : "Theory Computing Project",
    "30101" : "Applications of Quantum Physics",
    "30121" : "Introduction to Nuclear and Particle Physics",
    "30141" : "Electromagnetic Radiation",
    "30151" : "Thermal Physics of Bose and Fermi Gases",
    "30180" : "Third Year Laboratory",
    "30201" : "Mathematical Fundamentals of Quantum Mechanics",
    "30392" : "Cosmology",
    "30441" : "Electrodynamics",
    "30471" : "Introduction to Non-linear Physics",
    "30491" : "Interstellar Medium",
    "30511" : "Nuclear Fusion and Astrophysical Plasmas",
    "30611" : "Lasers and Photonics",
    "30632" : "Physics of Medical Imaging",
    "30672" : "Mathematical Methods for Physics",
    "30762" : "Object-Oriented Programming in C++",
    "30880" : "BSc Dissertation",
    "40181" : "MPhys Projects",
    "40202" : "Advanced Quantum Mechanics",
    "40222" : "Particle Physics",
    "40322" : "Nuclear Physics",
    "40352" : "Solid State Physics",
    "40411" : "Soft Matter Physics",
    "40421" : "Nuclear Structure and Exotic Nuclei",
    "40422" : "Applied Nuclear Physics",
    "40451" : "Superconductors and Superfluids",
    "40481" : "Quantum Field Theory",
    "40521" : "Frontiers of Particle Physics I",
    "40571" : "Advanced Statistical Physics",
    "40580" : "Laboratory For Students Returning From A Year Abroad",
    "40591" : "Radio Astronomy",
    "64611" : "Frontiers of Photon Science",
    "40622" : "Nuclear Forces and Reactions",
    "40631" : "Laser Photomedicine",
    "40652" : "Physics of Fluids",
    "40682" : "Gauge Theories",
    "30692" : "Stars and Stellar Evolution",
    "40712" : "Semiconductor Quantum Structures",
    "40722" : "Frontiers of Particle Physics II",
    "40732" : "Biomaterials Physics",
    "40752" : "Frontiers of Solid State Physics",
    "40771" : "Gravitation",
    "40772" : "Early Universe ",
    "40992" : "Galaxy Formation",
    "41702" : "Physics and Reality",
    "46111" : "Laser Technology",
    "46611" : "Radio to Terahertz Receiver Systems",
    
    "10180" : "Special Topics in Physics",
    "31692" : "Exoplanets",
    "40642" : "Atomic Physics",
}

## login page
domain_url = "https://video.manchester.ac.uk"
login_url = domain_url + "/lectures/"
login_page = browser.get(login_url)
login_html = login_page.soup

form = login_html.select("form")[0]
form.select("input")[0]["value"] = username
form.select("input")[1]["value"] = password

## courses page
courses_page = browser.submit(form, login_page.url)
courses_html = courses_page.soup

course_list = courses_html.select(".series") # CSS class="series" for lecture course links
course_urls = [ domain_url+link.get("href") for item in course_list for link in item.find_all("a") ]
course_numbers = [ link.get_text()[4:9] for item in course_list for link in item.find_all("a") ]
course_names = [ course_dict[number] for number in course_numbers ]

###
# FOR DEBUG
# course_urls = [ course_urls[-1] ]
# course_names = [ course_names[-1] ]
###

## individual course page
for course_url, course_name in zip(course_urls, course_names):
    course_page = browser.get(course_url)
    course_html = course_page.soup
    
    episode_list = course_html.select(".episode") # CSS class="episode" for individual lecture links
    episode_urls = [ domain_url+link.get("href") for item in episode_list for link in item.find_all("a") ]
    # episode_dates = [ link.get_text()[-6:] for item in episode_list for link in item.find_all("a") ]
    
    path = "/Volumes/Seagate Expansion Drive/University Notes/"
    for (dirs, subdirs, files) in os.walk(path):
        for subdir in subdirs:
            if course_name in subdir and "University Notes/Yr " in dirs:
                path = dirs + "/" + subdir + "/"
                
                if not os.path.isdir(path + "Lecture Recordings/"):
                    os.mkdir(path + "Lecture Recordings/")
                path = path + "Lecture Recordings/"
    
    ## individuals lecture episodes
    
    ###
    # FOR DEBUG
    # episode_urls = [ episode_urls[-1] ]
    # episode_dates = [ episode_dates[-1] ]
    ###
    
    # for episode_url, episode_date in zip(episode_urls, episode_dates):
    for episode_url in episode_urls:
        episode_page = browser.get(episode_url)
        episode_html = episode_page.soup
        # episode_date += "-" + episode_html.find("span", class_="added").get_text()[-4:] # CSS class="added" for lecture date (to add year)
        episode_date_full_text =  episode_html.find("span", class_="added").get_text() # CSS class="added" for lecture date
        episode_date = episode_date_full_text[17:19] + "-" + episode_date_full_text[13:16] + "-" + episode_date_full_text[-4:]
        
        # save files
        filename = path + episode_date + ".mp4"
        if not os.path.isfile(filename):
            print("downloading " + filename)
            dl_button_url = domain_url + episode_html.find(id="downloadButton").get("href")
            r = requests.get(dl_button_url)
        
            print("writing " + filename)
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024*1024): 
                    if chunk: 
                        f.write(chunk)
            print("written " + filename)
        else:
            print(filename + " already written")

