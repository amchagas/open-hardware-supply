JRA position

Open hardware supply – Assessing the documentation of academic papers describing open source hardware. 


Open Source Hardware is a term hardware, released under open source licenses. Which means that all their designs, build instructions, bill of materials and code needed to run it are made freely available in online repositories, such as GitHub. Within this larger domain, many science and education designs are being shared as academic papers.   

One of the issues in open source hardware is that even though best practices and guides on how to release designs are available, they are not always known and/or followed by open source hardware practitioners, leading to different levels of openness and reproducibility within the community. Our project is investigating how well academics are documenting their designs and how reproducible those designs are. To do that, we have developed the following data mining and analysis pipeline:
  

   1. Using a webscraper (using Python) and Google Scholar (GS), we collect bibliographic data on papers that contain “open hardware” as a keyword (currently we have ~1000 papers, of which we estimate half are describing hardware. The other half is either citing open hardware papers, or is about general issues on open hardware development)
    
      1.1 The reason for using GS is that the results for keyword search comprise the entire body of an article (while other databases like the Web of Science only searches on Title, Abstract and authors fields).
        
   2. This first dataset is not structured in a way that is amenable to systematic analysis, therefore, we use the Web of Science (WoS) to match GS data and pull structured data from WoS. 
   3. With structured WoS data we use Unpaywall API to get information about whether papers are open access or not, and under which open access terms they are released (gold, green, hybrid, etc).
   4. We store the data openly on a Zotero database. Currently we are manually checking a percentage of the papers, and using the “open-o-meter” as our guideline for scoring the quality of the documentation released with the publications. Given the database we have and the manual checks, we can statistically investigate which journals have the best documented papers, which ones are open access, if there is a tendency based on specific knowledge domains (eg are life science papers carrying better documentation than engineering ones?)
   5. Once our analyses are done, we are going to write down our findings in an academic paper, and provide suggestions on how open hardware developers, journals and funding agencies can create/follow guidelines to improve documentation of open hardware designs, increasing the reproducibility of designs and improvement in bringing the field forward.

  

Right now, this project requires support of someone who knows Python for the following tasks, all under supervision and feedback from current project leads:
    1. Manual analysis of papers, using the open-o-meter. This will allow the person working on the project to get a better grasp on how to look for Open Hardware documentation, what needs to be observed and how to translate that into code that could help streamline analysis.
    2. Create scripts that will download PDFs and find keywords and/or URLs in each document, as well as the location where the keywords/URLs appeared. For example, did the keyword “github” appeared on this pdf? If so, was it under “introduction” section, or references? Or both, etc…
        1. This will help streamline manual analysis of papers, as it will give users an estimated of where to look for information and repositories
    3. Create scripts that could give the probability of a certain paper being one that describes hardware. 
    4. Review current data analysis pipeline, and automate a couple of the steps.


This is a paid opportunity for 8 weeks (@225£ per week) supported by DISCUS. Interested people should email Andre Maia Chagas a.maia-chagas@sussex.ac.uk and Alexandre Hannud Abdo <alexandre.hannudabdo@u-pem.fr, with a CV and their possible starting date. The selected person is expected to be able to meet online or in person twice a week to check in on project progress. As stated before, the project will lead to an academic publication, to which the person selected will be, in principle, a co-author>

