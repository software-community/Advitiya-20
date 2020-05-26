# ADVITIYA-20

&nbsp;&nbsp;&nbsp;&nbsp;This repository contains the code for the website of one of the greatest and grandest Science & Technology Festival across India. 'ADVITIYA' is the annual Science & Technology festival of IIT Ropar. At ADVITIYA, students from various schools and colleges participate in various events categorized under different genres to learn, expo their talents and win prizes. At ADVITIYA-20, prizes worth 10 lakhs were to be won.<br> &nbsp;&nbsp;&nbsp;&nbsp;Apart from the events, ADVITIYA-20 also provided training, with certification, to various students enrolled in different Workshops. ADVITIYA-20 also organized Techno School Program, an event for the school students enrolled in classes 9th and 12th. The best young minds across the country were recognized and rewarded. Selected students were invited to tour the vast IIT Ropar Campus.<br>
&nbsp;&nbsp;&nbsp;&nbsp; ADVITIYA-20, in collaboration with The Indian Army, exhibited various modern artillery used by the Indian Army<br>
&nbsp;&nbsp;&nbsp;&nbsp; There was also an exhibition and an interactive session by the Indian Space Research Organisation(ISRO) scientists.<br>
&nbsp;&nbsp;&nbsp;&nbsp; Various cutural events including a show by the India's infamous mentalist Ms. Suhani Shah attracted huge crowd. Apart from this, a great comedy show was put in by the famous artist Anubhav Singh Bassi. ADVITIYA-20 ended on a high note as the participants, locals, IIT Ropar Community, all danced and enjoyed to the DJ and EDM shows put in by DJ Ojo and the EDM artist DJ Ravator. 


## How to run locally
- #### Create and activate Virtual environment
    - Install python virtualenv
        >```sudo pip3 install virtualenv```
    - Create a virtualenv
        - navigate to a folder of your choice
        - Run the command:
            > ```virtualenv Advitiya-20```
    - Activate virtualenv
        - Navigate to the folder where you created the virtualenv 'Advitiya-20'
        - Run the command:
            > ```source "Advitiya-20/bin/activate"```
- #### Clone this repository locally
    - Run the command:
        > ```git clone 'https://github.com/software-community/Advitiya-20.git'```
    - Navigate to this git repository
- #### Install Dependencies
    - Run the command:
        > ```pip3 install -r "requirements.txt"```
- #### Create and add details to '.env' file
    - Create a file named '.env'
    - Copy the contents from '.env.dev' and paste them here.
    - Fill in the values to the environment variables in '.env'
- #### Migrate and start the development server
    - Run the following commands:
        - > ```python manage.py migrate```
        - > ```python manage.py runserver```
- #### Open browser and go to ```http://localhost:8000```