## PART 1 ==> Choosing the topic
#TASK:
- Make a basic website with the freedom of choosing ant topic of your choice. 
- The website should have the basic UI functionalities and if possible add a model layer on top of it.
- Create a repository of the whole project and push it all on github, if possible add an issue on the repo.
- Create proper documentation of the whole journey of your thought-process and the planning/steps you took.

#MENTOR RULES: 
- Use any ai tools that you want.
- Restricted to using python since that's all that we know as of now.

#CONSTRAINTS:
- Solo task over the week no evaluation criteria its just a starter task to nudge us in the right direction so the model doesnt have to be perfect.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
- The above was the things we were told and I worded them out in a prompt and fed it to Claude. With this provided claude provided me starter topic as:
  Topic: Iris species classifier. I’m choosing it over an exam-score predictor because that one needs a fake dataset, which makes the model meaningless. Iris ships inside scikit-learn, so you skip all data wrangling and spend the week on structure, Git, and documentation, which is what the task is really about.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#MY COURSE OF ACTION FOR CHOOSING THE TOPIC:
- I told claude the present few issues and bits and pieces of what was going in my college right now:
      Okay so recently the 300 students across 3 batches have been divided in groups based on their performances but each group has similar things they are working on I'll givr you the idea from my group i.e. the group 1 the top 10 to 15 percentile. We are told that we have 2 major goals to achieve before the end of semester: 
      1) 200 problems solved on codeforces (emerged from problem solving and python side of zenith) - we are given 3 problems daily to achieve that task by our problem solving teacher and few videos/leetcode by our python teacher/co-founder
      2) a real end to end project (from fullstack side of things) - there has been minimal to no work on this end yet maybe we will be told what to do soon or perhaps we are expected to go on about it ourselves
    
    
      Another thing is whenever there are events there is a lot of miscommunication/communication gap among students like for example the 24 hour open source eval thing the teachers conduting it didnt know that we dont even know the basics of pull request and all on github and were expected to already know which resulted in a teacher teaching that amidst of that chaos. Also events like these clash with our exams etc at times
    
    
      The chaotic whatsapp thread example is very true the students majority of time spam stuff on groups even official making important things being lost in the spams
    
    
      From the student side friction whenever there is a open to all or mandatory thing coming up and you have to make teams of 4 or 3 among students it gets very chaotic and many end up even 3 days later saying in general whatsapp groupss that "im available for this and this project if anyone needs a teammate msg me".
    
      Also thing is most examples you gave kike resources deadlines etc most of it is resolved only with the already existing LMS of zenith - website with student/teacher portals. These were all that came to mind for now ill add on if i rmr more issues
    

- After this prompt and claude's recommendation of few potential topics, I gave a feedback as how Zenith already has a LMS that solves a lot of issues but at the end we zoned in on the topic of a "team-matcher website" which emerged out as rally.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
## PART 2 ==> WHAT CHANGED ON THE SUGGESTED AI PLAN
#FEEDBACK I GAVE ON THE FIRST PLAN (WHAT CHANGED)
- I did not want a full profile per event. I asked for one main centered profile per student for the website plus a short description to be added when an event happens, describing what one brings to the table for others to see.
- I asked whether a demo without a database would have enough to show, AI response:
        ``` Python ships with sqlite3, so there’s no server and no setup. Use it. A CSV breaks as soon as you need to join profiles to events. What makes the demo look good is a seed script that loads 25-30 fake students with varied skills, plus 2-3 sample events. Without that, a matcher with 1 user has nothing to match.```
- I asked it to add a separate teacher portal where they can themselves add an event with it's description and the size of the team etc, AI response:
        ``` A real teacher portal means authentication and roles, and that is where week-long projects die. The thin version is a single “Create Event” form on a separate Streamlit page. It writes to the same events table the students already read from. You’ve already budgeted that table, so the extra cost is about half a day.```
- Teacher portal therefore only has a thin version due to the time constraint and misses these:
            (1) No real login
            (2) No editing or deleting events. Create and list only
            (3) No notifications.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
## PART 3 ==> THE BROADER PLAN
- I asked for a step-by-step plan for the whole week. The project became Rally: teachers post Zenith events, students find teammates for them.

#DATA MODEL:
- students: name, batch, skills, languages, availability style, last_updated
- events: title, description, team_size, date
- event_entries: student_id, event_id, short event note

#SCOPE CUTS:
- No real login. A Student/Teacher switch in the sidebar, plus a teacher PIN from config.
- The teacher side only creates and lists events. No edit or delete.
- No notifications.
- Event notes are shown as free text and not parsed.
- Matching uses structured profile fields only.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
## PART 4 ==>  DAY WISE STEP BY STEP PLAN I GOT AS THE RESPONSE FROM PART 3

#AI RESPONSE:
```diff
#Step-by-step plan (Sat Nov 7 → Fri Nov 13)
#
#Sat: Foundation
#
#Create the repo, venv, requirements.txt, JOURNEY.md, and a .gitignore that excludes the .db file.
#Write the scope sentence: “A Streamlit app where teachers post Zenith events and students find teammates for them.”
#Log this conversation as entry #1 and commit.
#
#Sun: Data layer (db.py, no UI)
#
#Create the tables students, events, event_entries.
#Add typed functions: add_student, create_event, add_entry, get_entries(event_id).
#Write seed.py with 25-30 fake students and 3 events. Commit.
#
#Mon: Matching logic (matcher.py, no UI)
#
#Score two students by skill complementarity and availability overlap.
#Greedy grouping into teams of N, where N comes from the event’s team_size.
#Write 3-4 plain pytest tests with known inputs. This is the “model” piece and your cleanest portfolio signal.
#
#Tue: Student pages
#
#Page for profile creation/edit.
#Page to browse events, add an event note, and see suggested teammates with their last_updated dates.
#
#Wed: Teacher page and polish
#
#“Create Event” form (title, description, team size, date), with a PIN gate.
#Add an About section explaining how matching works.
#
#Thu: Documentation and issue
#
#Write the README with a screenshot and run instructions.
#Finalize JOURNEY.md.
#Open the issue: “Replace PIN with proper role-based authentication”.
#
#Fri: Buffer and demo.
#
#Risk to watch: Monday is the heaviest day. If matching slips, ship a simple version, which is rank by shared availability and display the top 5. A working basic matcher beats a half-built clever one. 
```

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
## PART 5 ==> WHAT I GATHERED FROM THE EVENT

#HABITS I SET:
- Keep logic separate from UI (the UI only calls logic functions).
- Commit after every working step with a real message.
- Log each AI prompt, output, change and breakage.

#DAY BY DAY BRIEF:
- For each day I went back to the chat and asked for that day's steps in more detail.

- _Sat: Foundation:_
 Repo, venv, requirements.txt, .gitignore (excluding the .db), one scope sentence. My system python3 was 3.15, so I made the venv with Homebrew python@3.13 instead. (3.13 has full Apple Silicon wheel coverage, so pip install streamlit pytest just works.)

Errors/Walls: 
  gh: command not found - github cli was not installed - brew install gh, then, gh auth login

- _Sun: Data layer:_
 db.py with the three tables and typed functions, plus seed.py with fake students and events.

Errors/Walls:
  In db.py VS code put a line through context manager. I thought my code was broken but it still ran, I got to know that apparently that's a warning not an error.

- _Mon: Matching logic_
 matcher.py scoring pairs on skill complementarity and availability overlap, greedy grouping into teams of team_size, and a few pytest tests.

Errors/Walls:
  Skills parse wrong -	DB stores a JSON list string, and split(",") leaves brackets and quotes	- json.loads(fix)

- _Tue: Student pages_
 Commits: student identity picker in the sidebar, profile create/edit form with shared option lists, from_student adapter and suggest_teammates with tests, and the event browse page with the join form and suggested teammates 

Errors/Walls:
  SyntaxError on matcher.py: I put the TYPE_CHECKING block above from __future__ import annotations. Python needs the __future__ import first, so 3 test files failed at collection. I moved the block below the regular imports and all 32 tests passed.

- _Wed: Teacher page and polish_
 Teacher event creation behind the PIN gate, and an About page explaining the matching logic. I also fixed a bug where a profile with no skills broke the score, and now give those profiles a neutral skill score.

Errors:
  1. file layout mismatch the AI thought everything was in the root folder but teacher.py is actually inside ui/ kept the same render_teacher name and put config.py and validation.py alongside db.py
  2. export command printed nothing so i thought it broke turns out it just stays quiet when it works checked it with echo $RALLY_TEACHER_PIN
  3. teacher page was blank app.py had no branch for the teacher role so nothing rendered added an else branch calling teacher.render_teacher()
  4. about text didnt match the code cause the AI wrote it from a description named group_students which doesnt even exist instead of form_teams and said it starts from the best pair when it actually starts from the lowest student_id checked matcher.py and rewrote it
  5. empty skills bug in score_pair two empty skill sets gave jaccard 0 so complementarity came out as 1.0 which is a perfect score changed it to a neutral 0.5 and added a test
  6. confusing test counts running pytest on tests/test_matcher.py showed 7 passed while the full run showed 36 not a bug one just runs that single file and the other runs everything

- _Thu: Docs and wrap-up_
 Screenshot of the working app, a fix so a non-ASCII PIN is handled and a clean error shows when the PIN is unset, the final README, and a markdown link fix in the README

